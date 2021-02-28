from localstack.utils.aws import aws_models
MXtEF=super
MXtEA=None
MXtEf=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  MXtEF(LambdaLayer,self).__init__(arn)
  self.cwd=MXtEA
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.MXtEf.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,MXtEf,env=MXtEA):
  MXtEF(RDSDatabase,self).__init__(MXtEf,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,MXtEf,env=MXtEA):
  MXtEF(RDSCluster,self).__init__(MXtEf,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,MXtEf,env=MXtEA):
  MXtEF(AppSyncAPI,self).__init__(MXtEf,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,MXtEf,env=MXtEA):
  MXtEF(AmplifyApp,self).__init__(MXtEf,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,MXtEf,env=MXtEA):
  MXtEF(ElastiCacheCluster,self).__init__(MXtEf,env=env)
class TransferServer(BaseComponent):
 def __init__(self,MXtEf,env=MXtEA):
  MXtEF(TransferServer,self).__init__(MXtEf,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,MXtEf,env=MXtEA):
  MXtEF(CloudFrontDistribution,self).__init__(MXtEf,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,MXtEf,env=MXtEA):
  MXtEF(CodeCommitRepository,self).__init__(MXtEf,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
