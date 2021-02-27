from localstack.utils.aws import aws_models
gncAl=super
gncAE=None
gncAL=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  gncAl(LambdaLayer,self).__init__(arn)
  self.cwd=gncAE
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.gncAL.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,gncAL,env=gncAE):
  gncAl(RDSDatabase,self).__init__(gncAL,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,gncAL,env=gncAE):
  gncAl(RDSCluster,self).__init__(gncAL,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,gncAL,env=gncAE):
  gncAl(AppSyncAPI,self).__init__(gncAL,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,gncAL,env=gncAE):
  gncAl(AmplifyApp,self).__init__(gncAL,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,gncAL,env=gncAE):
  gncAl(ElastiCacheCluster,self).__init__(gncAL,env=env)
class TransferServer(BaseComponent):
 def __init__(self,gncAL,env=gncAE):
  gncAl(TransferServer,self).__init__(gncAL,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,gncAL,env=gncAE):
  gncAl(CloudFrontDistribution,self).__init__(gncAL,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,gncAL,env=gncAE):
  gncAl(CodeCommitRepository,self).__init__(gncAL,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
