from localstack.utils.aws import aws_models
bfXRi=super
bfXRU=None
bfXRx=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  bfXRi(LambdaLayer,self).__init__(arn)
  self.cwd=bfXRU
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.bfXRx.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,bfXRx,env=bfXRU):
  bfXRi(RDSDatabase,self).__init__(bfXRx,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,bfXRx,env=bfXRU):
  bfXRi(RDSCluster,self).__init__(bfXRx,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,bfXRx,env=bfXRU):
  bfXRi(AppSyncAPI,self).__init__(bfXRx,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,bfXRx,env=bfXRU):
  bfXRi(AmplifyApp,self).__init__(bfXRx,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,bfXRx,env=bfXRU):
  bfXRi(ElastiCacheCluster,self).__init__(bfXRx,env=env)
class TransferServer(BaseComponent):
 def __init__(self,bfXRx,env=bfXRU):
  bfXRi(TransferServer,self).__init__(bfXRx,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,bfXRx,env=bfXRU):
  bfXRi(CloudFrontDistribution,self).__init__(bfXRx,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,bfXRx,env=bfXRU):
  bfXRi(CodeCommitRepository,self).__init__(bfXRx,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
