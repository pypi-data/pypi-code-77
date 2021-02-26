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

class RpcDubboServiceRouteApiRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Ft', '2018-07-13', 'RpcDubboServiceRouteApi')
		self.set_method('POST')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_RequiredValue(self):
		return self.get_query_params().get('RequiredValue')

	def set_RequiredValue(self,RequiredValue):
		self.add_query_param('RequiredValue',RequiredValue)

	def get_Code(self):
		return self.get_query_params().get('Code')

	def set_Code(self,Code):
		self.add_query_param('Code',Code)

	def get_IntValue(self):
		return self.get_query_params().get('IntValue')

	def set_IntValue(self,IntValue):
		self.add_query_param('IntValue',IntValue)

	def get_proxy_original_security_transport(self):
		return self.get_query_params().get('proxy_original_security_transport')

	def set_proxy_original_security_transport(self,proxy_original_security_transport):
		self.add_query_param('proxy_original_security_transport',proxy_original_security_transport)

	def get_ResultSwitchValue(self):
		return self.get_query_params().get('ResultSwitchValue')

	def set_ResultSwitchValue(self,ResultSwitchValue):
		self.add_query_param('ResultSwitchValue',ResultSwitchValue)

	def get_proxy_original_source_ip(self):
		return self.get_query_params().get('proxy_original_source_ip')

	def set_proxy_original_source_ip(self,proxy_original_source_ip):
		self.add_query_param('proxy_original_source_ip',proxy_original_source_ip)

	def get_JsonObject(self):
		return self.get_query_params().get('JsonObject')

	def set_JsonObject(self,JsonObject):
		self.add_query_param('JsonObject',JsonObject)

	def get_Sleep(self):
		return self.get_query_params().get('Sleep')

	def set_Sleep(self,Sleep):
		self.add_query_param('Sleep',Sleep)

	def get_SwitchValue(self):
		return self.get_query_params().get('SwitchValue')

	def set_SwitchValue(self,SwitchValue):
		self.add_query_param('SwitchValue',SwitchValue)

	def get_JsonObjectList(self):
		return self.get_query_params().get('JsonObjectList')

	def set_JsonObjectList(self,JsonObjectList):
		self.add_query_param('JsonObjectList',JsonObjectList)

	def get_DefaultValue(self):
		return self.get_query_params().get('DefaultValue')

	def set_DefaultValue(self,DefaultValue):
		self.add_query_param('DefaultValue',DefaultValue)

	def get_NumberRange(self):
		return self.get_query_params().get('NumberRange')

	def set_NumberRange(self,NumberRange):
		self.add_query_param('NumberRange',NumberRange)

	def get_Message(self):
		return self.get_query_params().get('Message')

	def set_Message(self,Message):
		self.add_query_param('Message',Message)

	def get_CheckNumberValue(self):
		return self.get_query_params().get('CheckNumberValue')

	def set_CheckNumberValue(self,CheckNumberValue):
		self.add_query_param('CheckNumberValue',CheckNumberValue)

	def get_HttpStatusCode(self):
		return self.get_query_params().get('HttpStatusCode')

	def set_HttpStatusCode(self,HttpStatusCode):
		self.add_query_param('HttpStatusCode',HttpStatusCode)

	def get_StringValue(self):
		return self.get_query_params().get('StringValue')

	def set_StringValue(self,StringValue):
		self.add_query_param('StringValue',StringValue)

	def get_EnumValue(self):
		return self.get_query_params().get('EnumValue')

	def set_EnumValue(self,EnumValue):
		self.add_query_param('EnumValue',EnumValue)

	def get_Success(self):
		return self.get_query_params().get('Success')

	def set_Success(self,Success):
		self.add_query_param('Success',Success)

	def get_OtherParam(self):
		return self.get_query_params().get('OtherParam')

	def set_OtherParam(self,OtherParam):
		self.add_query_param('OtherParam',OtherParam)