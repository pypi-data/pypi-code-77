from flask import request, g, session, current_app

from zm_user.conf import Config
from zm_user.tools.jsonify import jsonify_fail
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

page_size = 20


class ZmUser(object):
    def __init__(self, db, app,
                 set_before_request=True,
                 is_test=False,
                 need_init=False,
                 activated_email_url="",
                 prefix_url="/api"):
        """

        :param db:
        :param app:
        :param set_before_request: 是否设置before_request钩子
        :param activated_email_url :激活邮箱后跳转的链接，一般是网站首页
        """
        self.db = db
        Config.zm_user_db = db
        Config.activated_email_url = activated_email_url
        from zm_user.models.base import Base

        # 声明 用户 Model
        from zm_user.models.user import User
        self.User = User

        # 声明 角色 Model
        from zm_user.models.role import Role
        self.Role = Role

        # 声明 权限 Model
        from zm_user.models.permission import Permission
        self.Permission = Permission

        # 声明 平台 Model
        from zm_user.models.platform import Platform
        self.Platform = Platform

        # from zm_user.models.platform_user import PlatformUser
        # self.PlatformUser = PlatformUser

        if need_init:
            # 当需要初始化的时候再加载可以初始化的接口
            from zm_user.views.bb import bb_bp
            self.bb_bp = bb_bp
            app.register_blueprint(bb_bp, url_prefix='{}/bb'.format(prefix_url))

        from zm_user.views.user import user_bp
        self.user_bp = user_bp
        app.register_blueprint(user_bp, url_prefix='{}/user'.format(prefix_url))

        from zm_user.views.role import role_bp
        self.role_bp = role_bp
        app.register_blueprint(role_bp, url_prefix='{}/role'.format(prefix_url))

        from zm_user.views.unit import unit_bp
        self.unit_bp = unit_bp
        app.register_blueprint(unit_bp, url_prefix='{}/unit'.format(prefix_url))

        from zm_user.views.platform import platform_bp
        self.platform_bp = platform_bp
        app.register_blueprint(platform_bp, url_prefix='{}/platform'.format(prefix_url))

        if set_before_request and app is not None:
            @app.before_request
            def before_request():
                params = {}
                if request.args:
                    params.update(request.args.to_dict(flat=True))
                if request.is_json and request.get_data() and request.json:
                    if type(request.json) == type([]):
                        for x in request.json:
                            params.update(x)
                    else:
                        params.update(request.json)
                if request.form:
                    params.update(request.form.to_dict(flat=True))
                # 所有的请求参数
                g.params = params
                ip = request.remote_addr
                try:
                    _ip = request.headers["X-Real-IP"]
                    if _ip is not None:
                        ip = _ip
                except Exception as e:
                    pass
                g.env = str(request.user_agent)
                g.ip = ip
                # 当前第几页
                # ant design 页码是从1开始的
                if "pageNo" in params:
                    page = params.get('pageNo', '1')
                    g.page = int(page) - 1
                    g.page_size = int(params.get('pageSize', page_size))
                else:
                    page = params.get('page', '0')
                    g.page = int(page) if page else 0
                    # 每页面默认取出数量：20
                    g.page_size = int(params.get('page_size', page_size))
                    # 为了防止过分访问，限制最大50
                    g.page_size = 20 if g.page_size < 1 or g.page_size > 50 else g.page_size
                    g.page = 0 if g.page < 0 else g.page

                g.user = None
                user_id = session.get('user_id', None)
                if user_id:
                    user = User._q(User.id == user_id)
                    if user:
                        g.user = user
                g.url_root = request.url_root
                if not g.user and is_test and request.headers.has_key("user_id"):
                    # 在请求头上拿到token
                    user_id = request.headers["user_id"]
                    user = User._q(User.id == user_id)
                    if user:
                        g.user = user
                if not g.user and request.headers.has_key("bb_token"):
                    bb_token = request.headers["bb_token"]
                    if bb_token:
                        s = Serializer(current_app.config["SECRET_KEY"])
                        try:
                            user_id = s.loads(bb_token)["user_id"]
                            user = User._q(User.id == user_id)
                            if user:
                                g.user = user
                        except Exception:
                            return jsonify_fail(code=4101, msg="登录已过期")
