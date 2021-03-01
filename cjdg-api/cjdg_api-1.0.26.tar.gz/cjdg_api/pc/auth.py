'''
@说明    :超导角色组相关功能
@时间    :2019/12/25 下午1:02:11
@作者    :任秋锴
@版本    :1.0
'''
import requests
from loguru import logger


class cjdgAuthRole:
    def __init__(self, token):
        self.token = token
        self.headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Length": "0",
            "Cookie": f"accessToken={self.token}",
            "Host": "bms.chaojidaogou.com",
            "Origin": "http://bms.chaojidaogou.com",
            "Pragma": "no-cache",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }

    def request(self, api_name, method="GET", **kwargs):
        host_name = "http://bms.chaojidaogou.com/shopguide/"
        url = f"{host_name}{api_name}"
        kwargs["headers"] = self.headers
        response = requests.request(method=method, url=url, **kwargs)
        if response.status_code == 200:
            return self.response(response.json())
        else:
            logger.error({
                "msg": "status code 不正确。",
                "status_code": response.status_code,
            })

    def response(self, response_raw):
        return response_raw

    def get(self, group_id):
        api_name = "groupfindGroupDynamicAttr.jhtml"
        data = {
            "usergroup.groupId": group_id
        }
        kwargs = {}
        kwargs["data"] = data
        return self.request(api_name=api_name, method="POST", **kwargs)

    def list(self, role_name=None, page=1, rows=20):
        api_name = "authroleroleList.jhtml"
        data = {
            "ARole.name": role_name,
            "page": page,
            "rows": rows
        }

        kwargs = {}
        kwargs["data"] = data
        return self.request(api_name=api_name, method="POST", **kwargs)

    def save(self, role_name, role_id=0, for_del_userids=None, for_add_userids=None):
        api_name = "authrolesaveRole.jhtml"
        data = {
            "ARole.name": role_name,
            "ARole.id": role_id,
            "ARole.comment": "接口创建",
            "ARole.defaultFlag": 0,
            "ARole.defaultBackRole": 0,
        }
        if for_add_userids:
            data["for_add_userids"] = for_add_userids
        if for_del_userids:
            data["for_del_userids"] = for_del_userids
        logger.debug(data)
        kwargs = {}
        kwargs["data"] = data
        return self.request(api_name=api_name, method="POST", **kwargs)

    def delete(self, role_id):
        api_name = "authroledelRole.jhtml"
        data = {
            "ARole.id": role_id,
        }

        kwargs = {}
        kwargs["data"] = data
        return self.request(api_name=api_name, method="POST", **kwargs)

    def all(self):
        return self.list(rows=1000)

    def add_data(self):
        return self.list(rows=1000)

    def publish(self, auth_role_id):
        api_name = f"assignmentpublishAuthFactByRoleId.jhtml"
        kwargs = {}
        kwargs["params"] = dict(
            roleIdStr=auth_role_id
        )
        return self.request(api_name=api_name, **kwargs)


class cjdgAuthAssignment(cjdgAuthRole):
    def __init__(self, token):
        super().__init__(token)

    def save(self, role_id, resouce_id, resource_value_type_id, resource_value_id):
        api_name = "assignmentsave.jhtml"
        data = {
            "resouceId": resouce_id,
            "roleIdStr": role_id,
            "resourceValueTypeId": resource_value_type_id,
            "resourceValueId": resource_value_id,
        }
        kwargs = {}
        kwargs["data"] = data
        return self.request(api_name=api_name, method="POST", **kwargs)

    def save_shop(self, role_id, resource_value_id):
        return self.save(
            role_id=role_id,
            resouce_id=15,
            resource_value_type_id=155,
            resource_value_id=resource_value_id,
        )


def testcase1():
    # 测试流程是否正常
    auth_role_id = 7830179
    token = "83148a1ec454577f21ecad4a260e8aee_csb"
    ar = cjdgAuthRole(token)
    logger.debug(ar.all())


def testcase2():
    # 测试流程是否正常
    auth_role_id = 7830179
    token = "0ce3f7dbaa706b6a043fa8f82dba0f4c_mendale_web"
    ar = cjdgAuthRole(token)
    logger.debug(ar.save(role_name="任秋锴的测试", for_add_userids=316864745))


def testcase3():
    # 测试流程是否正常
    auth_role_id = 7843476
    token = "83148a1ec454577f21ecad4a260e8aee_csb"
    ar = cjdgAuthRole(token)
    logger.debug(ar.save(role_name="任秋锴的测试x", role_id=auth_role_id))


def testcase4():
    # 测试流程是否正常
    auth_role_id = 7843476
    token = "83148a1ec454577f21ecad4a260e8aee_csb"
    ar = cjdgAuthAssignment(token)
    logger.debug(ar.save_shop(role_id=7843476,
                              resource_value_id="1806710118@,1806710275@,1806710381@,1806710382@,1806710431@,1806711195@,1806713456@,1806713464@,1806713465@,1806747897@,1806748723@,1806748769@,1806750427@,1806752242@,1806756497@,1806756498@,1806756499@,1806781296@,1806781312@,1806781314@"))


if __name__ == "__main__":
    testcase2()
