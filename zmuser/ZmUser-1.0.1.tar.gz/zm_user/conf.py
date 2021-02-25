class Config(object):
    zm_user_db = None
    activated_email_url = ""

    DEFAULT_PERMISSIONS = [
        {
            'roleId': 'admin',
            'permissionId': 'unit',
            'permissionName': '单位',
        },
        {
            'roleId': 'admin',
            'permissionId': 'role',
            'permissionName': '角色',
        },
        {
            'roleId': 'admin',
            'permissionId': 'platform',
            'permissionName': '平台',
        },
        {
            'roleId': 'admin',
            'permissionId': 'user',
            'permissionName': '账户',
        },
        {
            'roleId': 'admin',
            'permissionId': 'user',
            'permissionName': '用户管理',
        }]
