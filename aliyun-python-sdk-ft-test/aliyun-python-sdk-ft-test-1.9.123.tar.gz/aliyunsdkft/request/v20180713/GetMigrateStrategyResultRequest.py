# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest
from aliyunsdkft.endpoint import endpoint_data

class GetMigrateStrategyResultRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Ft', '2018-07-13', 'GetMigrateStrategyResult')
		self.set_method('POST')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_parentName(self):
		return self.get_query_params().get('parentName')

	def set_parentName(self,parentName):
		self.add_query_param('parentName',parentName)

	def get_CurrentPage(self):
		return self.get_query_params().get('CurrentPage')

	def set_CurrentPage(self,CurrentPage):
		self.add_query_param('CurrentPage',CurrentPage)

	def get_BucName(self):
		return self.get_query_params().get('BucName')

	def set_BucName(self,BucName):
		self.add_query_param('BucName',BucName)

	def get_Env(self):
		return self.get_query_params().get('Env')

	def set_Env(self,Env):
		self.add_query_param('Env',Env)

	def get_type(self):
		return self.get_query_params().get('type')

	def set_type(self,type):
		self.add_query_param('type',type)

	def get_BucEmpId(self):
		return self.get_query_params().get('BucEmpId')

	def set_BucEmpId(self,BucEmpId):
		self.add_query_param('BucEmpId',BucEmpId)

	def get_strategyName(self):
		return self.get_body_params().get('strategyName')

	def set_strategyName(self,strategyName):
		self.add_body_params('strategyName', strategyName)

	def get_ApiName(self):
		return self.get_query_params().get('ApiName')

	def set_ApiName(self,ApiName):
		self.add_query_param('ApiName',ApiName)

	def get_flowSpecial(self):
		return self.get_query_params().get('flowSpecial')

	def set_flowSpecial(self,flowSpecial):
		self.add_query_param('flowSpecial',flowSpecial)

	def get_PageSize(self):
		return self.get_query_params().get('PageSize')

	def set_PageSize(self,PageSize):
		self.add_query_param('PageSize',PageSize)

	def get_ProductName(self):
		return self.get_query_params().get('ProductName')

	def set_ProductName(self,ProductName):
		self.add_query_param('ProductName',ProductName)

	def get_BucUid(self):
		return self.get_query_params().get('BucUid')

	def set_BucUid(self,BucUid):
		self.add_query_param('BucUid',BucUid)

	def get_VersionName(self):
		return self.get_query_params().get('VersionName')

	def set_VersionName(self,VersionName):
		self.add_query_param('VersionName',VersionName)

	def get_status(self):
		return self.get_query_params().get('status')

	def set_status(self,status):
		self.add_query_param('status',status)