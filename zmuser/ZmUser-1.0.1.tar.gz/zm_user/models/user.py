import base64
import datetime
import uuid

from flask import session, current_app, g
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import Column, Boolean, ForeignKey, String, Integer, TIMESTAMP, LargeBinary
from sqlalchemy.orm import relationship, backref
from werkzeug.security import generate_password_hash

from zm_user import Config
from zm_user.models.base import Base
from zm_user.models.platform_user import platform_user
from zm_user.tools.string_help import is_none_str


class User(Base):
    # 用户表
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, comment="自增ID")
    # 用户姓名
    name = Column(String(50), nullable=False, comment='用户姓名')
    # 用户密码
    password = Column(String(255), nullable=False, comment='用户密码')
    # 用户头像
    avatar = Column(LargeBinary, comment='用户头像')
    # 手机号
    phone = Column(String(11), comment='手机号')
    # 邮箱
    email = Column(String(50), comment='邮箱')
    # 邮箱激活码
    email_activation_code = Column(String(50), comment='邮箱激活码')
    # 手机号是否激活
    is_activated_phone = Column(Boolean, default=False, comment='手机号是否激活，0: 否，1: 是')
    # 邮箱是否激活
    is_activated_email = Column(Boolean, default=False, comment='邮箱是否激活，0: 否，1: 是')
    # 所属角色
    role_id = Column(Integer, ForeignKey('role.id'), comment='关联角色id')
    # 和用户是多对一
    role = relationship("Role", backref="user_list")
    # 是否冻结
    is_freeze = Column(Boolean, default=False, comment='是否冻结，冻结后无法登录，0: 否，1: 是')
    # 所关联的平台
    platform_list = relationship("Platform", backref='user_list', secondary=platform_user)
    # 是否需要修改初始密码
    is_need_update_password = Column(Boolean, default=True, comment='初始密码是否修改过，默认True')
    # 最后退出时间
    logout_time = Column(TIMESTAMP, comment="最后退出时间")
    search_text = Column(String(500),
                         nullable=False,
                         comment='搜索专用')
    # 该用户绑定在哪个 manager下的
    manager_id = Column(Integer, ForeignKey('user.id'), comment='所属管理者id')
    # 所有的子账号
    son_list = relationship('User', backref=backref('manager', remote_side=[id]))

    def get_avatar(self):
        if self.avatar:
            return "data:image/png;base64,"+base64.b64encode(self.avatar).decode("utf-8")

    def set_search_text(self):
        self.search_text = "{}{}{}".format(
            self.name,
            self.phone,
            self.email,
        )

    def to_new(self):
        if is_none_str(self.password):
            self.password = "123456"
            self.password = generate_password_hash(self.password)
        self.is_need_update_password = True
        self.email_activation_code = str(uuid.uuid4()).replace('-', '')
        super(User, self).to_new()

    def login_success(self):
        # 登录成功的 事件
        session['user_id'] = str(self.id)
        # 也支持token
        # 第一个参数是内部的私钥，这里写在共用的配置信息里了，如果只是测试可以写死
        # 第二个参数是有效期(秒)
        s = Serializer(current_app.config["SECRET_KEY"], expires_in=3600)
        # 接收用户id转换与编码
        bb_token = s.dumps({"user_id": self.id}).decode("ascii")
        return bb_token

    def logout(self):
        session['user_id'] = None
        # TODO 清除bb_token
        self.logout_time = datetime.datetime.now()

    def is_root(self):
        return self.role is not None and self.role.level == 0

    def to_json(self):
        res = self.base_to_json()
        res.update({
            'phone': self.phone,
            'email': self.email,
            'name': self.name,
            'is_activated_phone': self.is_activated_phone,
            'is_activated_email': self.is_activated_email,
            'manager_id': self.manager_id,
            'is_freeze': self.is_freeze,
            'is_root': self.is_root(),
            'is_need_update_password': self.is_need_update_password,
            'role': {
                'permissions': Config.DEFAULT_PERMISSIONS
            },
            "platform_names": "",
            "platform_id_list": []
        })
        print("role", self.role)
        if self.role:
            res.update({
                'role_name': self.role.name,
                'role_id': str(self.role.id)
            })
        if self.platform_list and len(self.platform_list) > 0:
            res.update({
                'platform_id_list': [str(platform.id) for platform in self.platform_list],
                'platform_names': ",".join([platform.name for platform in self.platform_list]),
            })
        if self.manager:
            res.update({
                'manager_name': self.manager.name,
                'manager_id': str(self.manager.id)
            })
        if g.user == self:
            res.update({
                'avatar': self.get_avatar()
            })
        print("platform_list->", self.platform_list)
        return res
