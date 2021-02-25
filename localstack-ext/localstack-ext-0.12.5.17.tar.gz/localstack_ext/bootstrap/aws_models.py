from localstack.utils.aws import aws_models
BYDzL=super
BYDzG=None
BYDzh=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  BYDzL(LambdaLayer,self).__init__(arn)
  self.cwd=BYDzG
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.BYDzh.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,BYDzh,env=BYDzG):
  BYDzL(RDSDatabase,self).__init__(BYDzh,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,BYDzh,env=BYDzG):
  BYDzL(RDSCluster,self).__init__(BYDzh,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,BYDzh,env=BYDzG):
  BYDzL(AppSyncAPI,self).__init__(BYDzh,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,BYDzh,env=BYDzG):
  BYDzL(AmplifyApp,self).__init__(BYDzh,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,BYDzh,env=BYDzG):
  BYDzL(ElastiCacheCluster,self).__init__(BYDzh,env=env)
class TransferServer(BaseComponent):
 def __init__(self,BYDzh,env=BYDzG):
  BYDzL(TransferServer,self).__init__(BYDzh,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,BYDzh,env=BYDzG):
  BYDzL(CloudFrontDistribution,self).__init__(BYDzh,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,BYDzh,env=BYDzG):
  BYDzL(CodeCommitRepository,self).__init__(BYDzh,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
