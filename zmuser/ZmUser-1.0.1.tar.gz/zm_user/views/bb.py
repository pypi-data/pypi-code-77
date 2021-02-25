from flask import Blueprint

from zm_user.models.role import Role
from zm_user.models.user import User

bb_bp = Blueprint('bb_bp', __name__)


@bb_bp.route('/init_user', methods=['get'])
def init_user():
    role = Role._q(Role.level == 0)
    if not role:
        role = Role()
        role.name = "超级管理员"
        role.level = 0
        role.is_variable=False
        role.to_save()

        role2 = Role()
        role2.name = "项目管理员"
        role2.level = 100
        role2.is_variable = False
        role2.to_save()

        role3 = Role()
        role3.name = "普通管理员"
        role3.level = 100
        role3.is_variable = False
        role3.to_save()
    user = User._q(User.role_id == role.id)
    if not user:
        user = User()
        user.role_id = role.id
        user.name = "超级管理员"
        user.phone = "19999999999"
        user.email = "1@qq.com"
        user.is_activated_email = True
        user.is_activated_phone = True
        user.to_new()
    print(user.role)
    return "success"
