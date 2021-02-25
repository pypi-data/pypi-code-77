""" The StalledJobAgent hunts for stalled jobs in the Job database. Jobs in "running"
    state not receiving a heart beat signal for more than stalledTime
    seconds will be assigned the "Stalled" state.
"""

from __future__ import print_function, absolute_import
from __future__ import division

__RCSID__ = "$Id$"

import six
from DIRAC import S_OK, S_ERROR, gConfig
from DIRAC.AccountingSystem.Client.Types.Job import Job
from DIRAC.Core.Base.AgentModule import AgentModule
from DIRAC.Core.Utilities.Time import fromString, toEpoch, dateTime, second
from DIRAC.Core.Utilities.ClassAd.ClassAdLight import ClassAd
from DIRAC.ConfigurationSystem.Client.Helpers import cfgPath
from DIRAC.ConfigurationSystem.Client.PathFinder import getSystemInstance
from DIRAC.WorkloadManagementSystem.Client.WMSClient import WMSClient
from DIRAC.WorkloadManagementSystem.Client.JobMonitoringClient import JobMonitoringClient
from DIRAC.WorkloadManagementSystem.Client.PilotManagerClient import PilotManagerClient
from DIRAC.WorkloadManagementSystem.DB.JobDB import JobDB
from DIRAC.WorkloadManagementSystem.DB.JobLoggingDB import JobLoggingDB
from DIRAC.WorkloadManagementSystem.Client import JobStatus, JobMinorStatus


class StalledJobAgent(AgentModule):
  """
The specific agents must provide the following methods:
- initialize() for initial settings
- beginExecution()
- execute() - the main method called in the agent cycle
- endExecution()
- finalize() - the graceful exit of the method, this one is usually used
for the agent restart
"""

  def __init__(self, *args, **kwargs):
    """ c'tor
    """
    AgentModule.__init__(self, *args, **kwargs)

    self.jobDB = None
    self.logDB = None
    self.matchedTime = 7200
    self.rescheduledTime = 600
    self.submittingTime = 300
    self.stalledJobsTolerantSites = []

  #############################################################################
  def initialize(self):
    """Sets default parameters
    """
    self.jobDB = JobDB()
    self.logDB = JobLoggingDB()
    self.am_setOption('PollingTime', 60 * 60)
    if not self.am_getOption('Enable', True):
      self.log.info('Stalled Job Agent running in disabled mode')
    return S_OK()

  #############################################################################
  def execute(self):
    """ The main agent execution method
    """

    self.log.verbose('Waking up Stalled Job Agent')

    wms_instance = getSystemInstance('WorkloadManagement')
    if not wms_instance:
      return S_ERROR('Can not get the WorkloadManagement system instance')
    wrapperSection = cfgPath('Systems', 'WorkloadManagement', wms_instance, 'JobWrapper')

    stalledTime = self.am_getOption('StalledTimeHours', 2)
    failedTime = self.am_getOption('FailedTimeHours', 6)
    self.stalledJobsTolerantSites = self.am_getOption('StalledJobsTolerantSites', [])
    self.stalledJobsToleranceTime = self.am_getOption('StalledJobsToleranceTime', 0)

    self.submittingTime = self.am_getOption('SubmittingTime', self.submittingTime)
    self.matchedTime = self.am_getOption('MatchedTime', self.matchedTime)
    self.rescheduledTime = self.am_getOption('RescheduledTime', self.rescheduledTime)

    self.log.verbose('StalledTime = %s cycles' % (stalledTime))
    self.log.verbose('FailedTime = %s cycles' % (failedTime))

    watchdogCycle = gConfig.getValue(cfgPath(wrapperSection, 'CheckingTime'), 30 * 60)
    watchdogCycle = max(watchdogCycle, gConfig.getValue(cfgPath(wrapperSection, 'MinCheckingTime'), 20 * 60))

    # Add half cycle to avoid race conditions
    stalledTime = int(watchdogCycle * (stalledTime + 0.5))
    failedTime = int(watchdogCycle * (failedTime + 0.5))

    result = self._markStalledJobs(stalledTime)
    if not result['OK']:
      self.log.error('Failed to detect stalled jobs', result['Message'])

    # Note, jobs will be revived automatically during the heartbeat signal phase and
    # subsequent status changes will result in jobs not being selected by the
    # stalled job agent.

    result = self._failStalledJobs(failedTime)
    if not result['OK']:
      self.log.error('Failed to process stalled jobs', result['Message'])

    result = self._failSubmittingJobs()
    if not result['OK']:
      self.log.error('Failed to process jobs being submitted', result['Message'])

    result = self._kickStuckJobs()
    if not result['OK']:
      self.log.error('Failed to kick stuck jobs', result['Message'])

    return S_OK('Stalled Job Agent cycle complete')

  #############################################################################
  def _markStalledJobs(self, stalledTime):
    """ Identifies stalled jobs running or completing without update longer than stalledTime.
    """
    stalledCounter = 0
    aliveCounter = 0
    # This is the minimum time we wait for declaring a job Stalled, therefore it is safe
    checkTime = dateTime() - stalledTime * second
    checkedStatuses = [JobStatus.RUNNING, JobStatus.COMPLETING]
    # Only get jobs whose HeartBeat is older than the stalledTime
    result = self.jobDB.selectJobs({'Status': checkedStatuses},
                                   older=checkTime, timeStamp='HeartBeatTime')
    if not result['OK']:
      return result
    if not result['Value']:
      return S_OK()
    jobs = sorted(result['Value'])
    self.log.info('%d %s jobs will be checked for being stalled, heartbeat before %s' %
                  (len(jobs), ' & '.join(checkedStatuses), str(checkTime)))

    for job in jobs:
      delayTime = stalledTime
      # Add a tolerance time for some sites if required
      site = self.jobDB.getJobAttribute(job, 'site')['Value']
      if site in self.stalledJobsTolerantSites:
        delayTime += self.stalledJobsToleranceTime
      # Check if the job is really stalled
      result = self.__checkJobStalled(job, delayTime)
      if result['OK']:
        self.log.verbose('Updating status to Stalled for job %s' % (job))
        self.__updateJobStatus(job, JobStatus.STALLED)
        stalledCounter += 1
      else:
        self.log.verbose(result['Message'])
        aliveCounter += 1

    self.log.info('Total jobs: %d, Stalled jobs: %d, %s jobs: %d' %
                  (len(jobs), stalledCounter, '+'.join(checkedStatuses), aliveCounter))
    return S_OK()

  #############################################################################
  def _failStalledJobs(self, failedTime):
    """ Changes the Stalled status to Failed for jobs long in the Stalled status
    """
    # Only get jobs that have been Stalled for long enough
    result = self.jobDB.selectJobs({'Status': JobStatus.STALLED})
    if not result['OK']:
      return result
    jobs = result['Value']

    failedCounter = 0
    minorStalledStatuses = (JobMinorStatus.STALLED_PILOT_NOT_RUNNING, 'Stalling for more than %d sec' % failedTime)

    if jobs:
      self.log.info('%d jobs Stalled will be checked for failure' % len(jobs))

      for job in jobs:
        setFailed = False
        # Check if the job pilot is lost
        result = self.__getJobPilotStatus(job)
        if not result['OK']:
          self.log.error('Failed to get pilot status', result['Message'])
          continue
        pilotStatus = result['Value']
        if pilotStatus != "Running":
          setFailed = minorStalledStatuses[0]
        else:
          # Verify that there was no sign of life for long enough
          result = self.__getLatestUpdateTime(job)
          if not result['OK']:
            self.log.error('Failed to get job update time', result['Message'])
            continue
          elapsedTime = toEpoch() - result['Value']
          if elapsedTime > failedTime:
            setFailed = minorStalledStatuses[1]

        # Set the jobs Failed, send them a kill signal in case they are not really dead and send accounting info
        if setFailed:
          self.__sendKillCommand(job)
          self.__updateJobStatus(job, JobStatus.FAILED, minorStatus=setFailed)
          failedCounter += 1
          result = self.__sendAccounting(job)
          if not result['OK']:
            self.log.error('Failed to send accounting', result['Message'])

    recoverCounter = 0

    for minor in minorStalledStatuses:
      result = self.jobDB.selectJobs({'Status': JobStatus.FAILED, 'MinorStatus': minor, 'AccountedFlag': 'False'})
      if not result['OK']:
        return result
      if result['Value']:
        jobs = result['Value']
        self.log.info('%s Stalled jobs will be Accounted' % (len(jobs)))
        for job in jobs:
          result = self.__sendAccounting(job)
          if not result['OK']:
            self.log.error('Failed to send accounting', result['Message'])
            continue

          recoverCounter += 1
      if not result['OK']:
        break

    if failedCounter:
      self.log.info('%d jobs set to Failed' % failedCounter)
    if recoverCounter:
      self.log.info('%d jobs properly Accounted' % recoverCounter)
    return S_OK(failedCounter)

  #############################################################################
  def __getJobPilotStatus(self, jobID):
    """ Get the job pilot status
    """
    result = JobMonitoringClient().getJobParameter(jobID, 'Pilot_Reference')
    if not result['OK']:
      return result
    pilotReference = result['Value'].get('Pilot_Reference')
    if not pilotReference:
      # There is no pilot reference, hence its status is unknown
      return S_OK('NoPilot')

    result = PilotManagerClient().getPilotInfo(pilotReference)
    if not result['OK']:
      if "No pilots found" in result['Message']:
        self.log.warn(result['Message'])
        return S_OK('NoPilot')
      self.log.error('Failed to get pilot information',
                     'for job %d: ' % jobID + result['Message'])
      return S_ERROR('Failed to get the pilot status')
    pilotStatus = result['Value'][pilotReference]['Status']

    return S_OK(pilotStatus)

  #############################################################################
  def __checkJobStalled(self, job, stalledTime):
    """ Compares the most recent of LastUpdateTime and HeartBeatTime against
    the stalledTime limit.
    """
    result = self.__getLatestUpdateTime(job)
    if not result['OK']:
      return result

    elapsedTime = toEpoch() - result['Value']
    self.log.verbose('(CurrentTime-LastUpdate) = %s secs' % (elapsedTime))
    if elapsedTime > stalledTime:
      self.log.info('Job %s is identified as stalled with last update > %s secs ago' % (job, elapsedTime))
      return S_OK('Stalled')

    return S_ERROR('Job %s is running and will be ignored' % job)

  #############################################################################
  def __getLatestUpdateTime(self, job):
    """ Returns the most recent of HeartBeatTime and LastUpdateTime
    """
    result = self.jobDB.getJobAttributes(job, ['HeartBeatTime', 'LastUpdateTime'])
    if not result['OK']:
      self.log.error('Failed to get job attributes', result['Message'])
    if not result['OK'] or not result['Value']:
      self.log.error('Could not get attributes for job', '%s' % job)
      return S_ERROR('Could not get attributes for job')

    latestUpdate = 0
    if not result['Value']['HeartBeatTime'] or result['Value']['HeartBeatTime'] == 'None':
      self.log.verbose('HeartBeatTime is null for job %s' % job)
    else:
      latestUpdate = toEpoch(fromString(result['Value']['HeartBeatTime']))

    if not result['Value']['LastUpdateTime'] or result['Value']['LastUpdateTime'] == 'None':
      self.log.verbose('LastUpdateTime is null for job %s' % job)
    else:
      latestUpdate = max(latestUpdate, toEpoch(fromString(result['Value']['LastUpdateTime'])))

    if not latestUpdate:
      return S_ERROR('LastUpdate and HeartBeat times are null for job %s' % job)
    else:
      self.log.verbose('Latest update time from epoch for job %s is %s' % (job, latestUpdate))
      return S_OK(latestUpdate)

  #############################################################################
  def __updateJobStatus(self, job, status, minorStatus=None):
    """ This method updates the job status in the JobDB, this should only be
        used to fail jobs due to the optimizer chain.
    """
    self.log.verbose("self.jobDB.setJobAttribute(%s,'Status','%s',update=True)" % (job, status))

    if self.am_getOption('Enable', True):
      result = self.jobDB.setJobAttribute(job, 'Status', status, update=True)
    else:
      result = S_OK('DisabledMode')

    if result['OK']:
      if minorStatus:
        self.log.verbose("self.jobDB.setJobAttribute(%s,'MinorStatus','%s',update=True)" % (job, minorStatus))
        result = self.jobDB.setJobAttribute(job, 'MinorStatus', minorStatus, update=True)

    if not minorStatus:  # Retain last minor status for stalled jobs
      result = self.jobDB.getJobAttributes(job, ['MinorStatus'])
      if result['OK']:
        minorStatus = result['Value']['MinorStatus']

    logStatus = status
    result = self.logDB.addLoggingRecord(job, status=logStatus, minorStatus=minorStatus, source='StalledJobAgent')
    if not result['OK']:
      self.log.warn(result)

    return result

  def __getProcessingType(self, jobID):
    """ Get the Processing Type from the JDL, until it is promoted to a real Attribute
    """
    processingType = 'unknown'
    result = self.jobDB.getJobJDL(jobID, original=True)
    if not result['OK']:
      return processingType
    classAdJob = ClassAd(result['Value'])
    if classAdJob.lookupAttribute('ProcessingType'):
      processingType = classAdJob.getAttributeString('ProcessingType')
    return processingType

  def __sendAccounting(self, jobID):
    """ Send WMS accounting data for the given job
    """
    try:
      accountingReport = Job()
      endTime = 'Unknown'
      lastHeartBeatTime = 'Unknown'

      result = self.jobDB.getJobAttributes(jobID)
      if not result['OK']:
        return result
      jobDict = result['Value']

      startTime, endTime = self.__checkLoggingInfo(jobID, jobDict)
      lastCPUTime, lastWallTime, lastHeartBeatTime = self.__checkHeartBeat(jobID, jobDict)
      lastHeartBeatTime = fromString(lastHeartBeatTime)
      if lastHeartBeatTime is not None and lastHeartBeatTime > endTime:
        endTime = lastHeartBeatTime

      result = JobMonitoringClient().getJobParameter(jobID, 'CPUNormalizationFactor')
      if not result['OK'] or not result['Value']:
        self.log.error(
            'Error getting Job Parameter CPUNormalizationFactor, setting 0',
            result.get(
                'Message',
                'No such value'))
        cpuNormalization = 0.0
      else:
        cpuNormalization = float(result['Value'].get('CPUNormalizationFactor'))

    except Exception as e:
      self.log.exception("Exception in __sendAccounting",
                         "for job=%s: endTime=%s, lastHBTime=%s" % (str(jobID), str(endTime), str(lastHeartBeatTime)),
                         lException=e)
      return S_ERROR("Exception")
    processingType = self.__getProcessingType(jobID)

    accountingReport.setStartTime(startTime)
    accountingReport.setEndTime(endTime)
    # execTime = toEpoch( endTime ) - toEpoch( startTime )
    # Fill the accounting data
    acData = {'Site': jobDict['Site'],
              'User': jobDict['Owner'],
              'UserGroup': jobDict['OwnerGroup'],
              'JobGroup': jobDict['JobGroup'],
              'JobType': jobDict['JobType'],
              'JobClass': jobDict['JobSplitType'],
              'ProcessingType': processingType,
              'FinalMajorStatus': 'Failed',
              'FinalMinorStatus': 'Stalled',
              'CPUTime': lastCPUTime,
              'NormCPUTime': lastCPUTime * cpuNormalization,
              'ExecTime': lastWallTime,
              'InputDataSize': 0.0,
              'OutputDataSize': 0.0,
              'InputDataFiles': 0,
              'OutputDataFiles': 0,
              'DiskSpace': 0.0,
              'InputSandBoxSize': 0.0,
              'OutputSandBoxSize': 0.0,
              'ProcessedEvents': 0
              }

    # For accidentally stopped jobs ExecTime can be not set
    if not acData['ExecTime']:
      acData['ExecTime'] = acData['CPUTime']
    elif acData['ExecTime'] < acData['CPUTime']:
      acData['ExecTime'] = acData['CPUTime']

    self.log.verbose('Accounting Report is:')
    self.log.verbose(acData)
    accountingReport.setValuesFromDict(acData)

    result = accountingReport.commit()
    if result['OK']:
      self.jobDB.setJobAttribute(jobID, 'AccountedFlag', 'True')
    else:
      self.log.error('Failed to send accounting report', 'Job: %d, Error: %s' % (int(jobID), result['Message']))
    return result

  def __checkHeartBeat(self, jobID, jobDict):
    """ Get info from HeartBeat
    """
    result = self.jobDB.getHeartBeatData(jobID)
    lastCPUTime = 0
    lastWallTime = 0
    lastHeartBeatTime = jobDict['StartExecTime']
    if lastHeartBeatTime == "None":
      lastHeartBeatTime = 0

    if result['OK']:
      for name, value, heartBeatTime in result['Value']:
        if name == 'CPUConsumed':
          try:
            value = int(float(value))
            if value > lastCPUTime:
              lastCPUTime = value
          except ValueError:
            pass
        if name == 'WallClockTime':
          try:
            value = int(float(value))
            if value > lastWallTime:
              lastWallTime = value
          except ValueError:
            pass
        if heartBeatTime > lastHeartBeatTime:
          lastHeartBeatTime = heartBeatTime

    return lastCPUTime, lastWallTime, lastHeartBeatTime

  def __checkLoggingInfo(self, jobID, jobDict):
    """ Get info from JobLogging
    """
    logList = []
    result = self.logDB.getJobLoggingInfo(jobID)
    if result['OK']:
      logList = result['Value']

    startTime = jobDict['StartExecTime']
    if not startTime or startTime == 'None':
      # status, minor, app, stime, source
      for items in logList:
        if items[0] == 'Running':
          startTime = items[3]
          break
      if not startTime or startTime == 'None':
        startTime = jobDict['SubmissionTime']

    if isinstance(startTime, six.string_types):
      startTime = fromString(startTime)
      if startTime is None:
        self.log.error('Wrong timestamp in DB', items[3])
        startTime = dateTime()

    endTime = dateTime()
    # status, minor, app, stime, source
    for items in logList:
      if items[0] == 'Stalled':
        endTime = fromString(items[3])
    if endTime is None:
      self.log.error('Wrong timestamp in DB', items[3])
      endTime = dateTime()

    return startTime, endTime

  def _kickStuckJobs(self):
    """ Reschedule jobs stuck in initialization status Rescheduled, Matched
    """

    message = ''

    checkTime = dateTime() - self.matchedTime * second
    result = self.jobDB.selectJobs({'Status': JobStatus.MATCHED}, older=checkTime)
    if not result['OK']:
      self.log.error('Failed to select jobs', result['Message'])
      return result

    jobIDs = result['Value']
    if jobIDs:
      self.log.info('Rescheduling %d jobs stuck in Matched status' % len(jobIDs))
      result = self.jobDB.rescheduleJobs(jobIDs)
      if 'FailedJobs' in result:
        message = 'Failed to reschedule %d jobs stuck in Matched status' % len(result['FailedJobs'])

    checkTime = dateTime() - self.rescheduledTime * second
    result = self.jobDB.selectJobs({'Status': 'Rescheduled'}, older=checkTime)
    if not result['OK']:
      self.log.error('Failed to select jobs', result['Message'])
      return result

    jobIDs = result['Value']
    if jobIDs:
      self.log.info('Rescheduling %d jobs stuck in Rescheduled status' % len(jobIDs))
      result = self.jobDB.rescheduleJobs(jobIDs)
      if 'FailedJobs' in result:
        if message:
          message += '\n'
        message += 'Failed to reschedule %d jobs stuck in Rescheduled status' % len(result['FailedJobs'])

    if message:
      return S_ERROR(message)
    return S_OK()

  def _failSubmittingJobs(self):
    """ Failed Jobs stuck in Submitting Status for a long time.
        They are due to a failed bulk submission transaction.
    """

    # Get old Submitting Jobs
    checkTime = dateTime() - self.submittingTime * second
    result = self.jobDB.selectJobs({'Status': JobStatus.SUBMITTING}, older=checkTime)
    if not result['OK']:
      self.log.error('Failed to select jobs', result['Message'])
      return result

    for jobID in result['Value']:
      result = self.__updateJobStatus(jobID, JobStatus.FAILED)
      if not result['OK']:
        self.log.error('Failed to update job status', result['Message'])
        continue

    return S_OK()

  def __sendKillCommand(self, job):
    """Send a kill signal to the job such that it cannot continue running.

    :param int job: ID of job to send kill command
    """
    ownerDN = self.jobDB.getJobAttribute(job, 'OwnerDN')
    ownerGroup = self.jobDB.getJobAttribute(job, 'OwnerGroup')
    if ownerDN['OK'] and ownerGroup['OK']:
      wmsClient = WMSClient(useCertificates=True, delegatedDN=ownerDN['Value'], delegatedGroup=ownerGroup['Value'])
      resKill = wmsClient.killJob(job)
      if not resKill['OK']:
        self.log.error("Failed to send kill command to job", "%s: %s" % (job, resKill['Message']))
    else:
      self.log.error("Failed to get ownerDN or Group for job:", "%s: %s, %s" %
                     (job, ownerDN.get('Message', ''), ownerGroup.get('Message', '')))

# EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#
