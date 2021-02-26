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

class CountCloudProductCallTimesRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Ft', '2018-07-13', 'CountCloudProductCallTimes')
		self.set_method('POST')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_BucUid(self):
		return self.get_query_params().get('BucUid')

	def set_BucUid(self,BucUid):
		self.add_query_param('BucUid',BucUid)

	def get_BucName(self):
		return self.get_query_params().get('BucName')

	def set_BucName(self,BucName):
		self.add_query_param('BucName',BucName)

	def get_BucEmpId(self):
		return self.get_query_params().get('BucEmpId')

	def set_BucEmpId(self,BucEmpId):
		self.add_query_param('BucEmpId',BucEmpId)

	def get_CloudProductsJsonString(self):
		return self.get_body_params().get('CloudProductsJsonString')

	def set_CloudProductsJsonString(self,CloudProductsJsonString):
		self.add_body_params('CloudProductsJsonString', CloudProductsJsonString)

	def get_ClearCloudCache(self):
		return self.get_body_params().get('ClearCloudCache')

	def set_ClearCloudCache(self,ClearCloudCache):
		self.add_body_params('ClearCloudCache', ClearCloudCache)

	def get_ClearProductCache(self):
		return self.get_body_params().get('ClearProductCache')

	def set_ClearProductCache(self,ClearProductCache):
		self.add_body_params('ClearProductCache', ClearProductCache)