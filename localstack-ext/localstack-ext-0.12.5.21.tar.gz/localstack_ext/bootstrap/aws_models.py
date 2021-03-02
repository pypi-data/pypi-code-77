from localstack.utils.aws import aws_models
FUfwX=super
FUfwW=None
FUfwg=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  FUfwX(LambdaLayer,self).__init__(arn)
  self.cwd=FUfwW
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.FUfwg.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,FUfwg,env=FUfwW):
  FUfwX(RDSDatabase,self).__init__(FUfwg,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,FUfwg,env=FUfwW):
  FUfwX(RDSCluster,self).__init__(FUfwg,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,FUfwg,env=FUfwW):
  FUfwX(AppSyncAPI,self).__init__(FUfwg,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,FUfwg,env=FUfwW):
  FUfwX(AmplifyApp,self).__init__(FUfwg,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,FUfwg,env=FUfwW):
  FUfwX(ElastiCacheCluster,self).__init__(FUfwg,env=env)
class TransferServer(BaseComponent):
 def __init__(self,FUfwg,env=FUfwW):
  FUfwX(TransferServer,self).__init__(FUfwg,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,FUfwg,env=FUfwW):
  FUfwX(CloudFrontDistribution,self).__init__(FUfwg,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,FUfwg,env=FUfwW):
  FUfwX(CodeCommitRepository,self).__init__(FUfwg,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
