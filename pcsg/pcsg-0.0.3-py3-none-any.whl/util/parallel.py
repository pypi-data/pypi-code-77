import threading




class ParallelRunner:
    """
    Parallel executor for jobs
    """
    def __init__(self, jobs, progressCallback = None):
        self.lock = threading.Lock ()
        self.jobs = jobs
        self.progressCallback = progressCallback
        self.nextJob = 0
        self.executedJobs = 0

    
    def execute(self, threadCount):
        """
        Execute job list multi threaded.
        """
        threads = []
        # start worker threads
        for i in range (0, threadCount):
            t = threading.Thread (target = self._entry)
            threads.append (t)
            t.start ()

        # join worker threads
        for t in threads:
            t.join ()
            
        # end if sequence
        if self.progressCallback != None:
            lc = self.jobs[0]["description"] if len (self.jobs) > 0 else None
            if lc != None:
                self.progressCallback (lc, len (self.jobs), len (self.jobs))
        return True


    def _entry(self):
        """
        Thread entry function.
        """
        while self._doWork ():
            pass


    def _doWork(self) -> bool:
        """
        Process a single job. Returns true if there is more work.
        """
        # grab a job from queur
        self.lock.acquire ()
        jobId = self.nextJob
        self.nextJob = jobId + 1
        self.lock.release ()

        # abort if no jobs are left
        if jobId >= len (self.jobs):
            return False

        # execute job
        job = self.jobs[jobId]
        lc = job["description"]
        if self.progressCallback != None:
            self.lock.acquire ()
            self.progressCallback (lc, self.executedJobs, len (self.jobs))
            self.lock.release ()
        else:
            print (lc + " (" + str (jobId) + " / " + str (len (self.jobs)) + ")\n")
        if job["runner"] (job) == False:
            return False
        self.executedJobs = self.executedJobs + 1

        # continue on jobs
        return True




def execute (jobs: list, threadCount: int, progressCallback = None):
    """
    Execute workload in a thread pool.
    """
    # execute multi threaded
    if threadCount > 1:
        runner = ParallelRunner (jobs, progressCallback)
        return runner.execute (threadCount)

    # execute single threaded
    jid = 0
    jc = len (jobs)
    lc = None
    for job in jobs:
        lc = job["description"]
        if progressCallback != None:
            progressCallback (lc, jid, jc)
        else:
            print (lc + " (" + str (jid) + " / " + str (jc) + ")")
        if job["runner"] (job) == False:
            return False
        jid = jid + 1
    if jc > 0:
        if progressCallback != None:
            progressCallback (lc, jc, jc)
        else:
            print (lc + " (" + str (jc) + " / " + str (jc) + ")")
    return True
