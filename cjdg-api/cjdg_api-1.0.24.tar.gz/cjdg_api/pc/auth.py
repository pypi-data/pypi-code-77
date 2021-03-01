'''
@说明    :超导角色组相关功能
@时间    :2019/12/25 下午1:02:11
@作者    :任秋锴
@版本    :1.0
'''
import requests
from loguru import logger
from requests import api


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
            "for_add_userids": for_add_userids,
            "for_del_userids": for_add_userids,
        }

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

    def publish(self, auth_role_id):
        api_name = f"assignmentpublishAuthFactByRoleId.jhtml?roleIdStr={auth_role_id}"
        kwargs = {}
        kwargs["params"] = dict(
            roleIdStr=auth_role_id
        )
        return self.request(api_name=api_name, **kwargs)


def testcase1():
    # 测试流程是否正常
    auth_role_id = 7830179
    token = "83148a1ec454577f21ecad4a260e8aee_csb"
    ar = cjdgAuthRole(token)
    logger.debug(ar.all())


def testcase2():
    # 测试流程是否正常
    auth_role_id = 7830179
    token = "83148a1ec454577f21ecad4a260e8aee_csb"
    ar = cjdgAuthRole(token)
    logger.debug(ar.save(role_name="任秋锴的测试"))


def testcase3():
    # 测试流程是否正常
    auth_role_id = 7843476
    token = "83148a1ec454577f21ecad4a260e8aee_csb"
    ar = cjdgAuthRole(token)
    logger.debug(ar.save(role_name="任秋锴的测试x", role_id=auth_role_id))


if __name__ == "__main__":
    testcase3()
