from flask import Blueprint, g

from zm_user.models.role import Role
from zm_user.models.user import User
from zm_user.tools.jsonify import jsonify_fail, jsonify_success, jsonify_list_page
from zm_user.tools.params import get_params
from zm_user.tools.permission import permission_check_root
from zm_user.tools.string_help import str_to_int, str_to_bool, is_none_str

role_bp = Blueprint('role_bp', __name__)


@role_bp.route('/add', methods=['post'])
@get_params({'name': '请输入名称', 'level': "请设置管理员等级"})
@permission_check_root()
def add():
    role = Role._q(Role.name == g.name)
    if role:
        return jsonify_fail(msg="该角色名称已经存在")
    role = Role()
    role.name = g.name
    role.level = str_to_int(g.level)
    if role.level < 1:
        return jsonify_fail(msg="管理员等级 不能小于1")
    role.is_variable = str_to_bool(g.params.get('is_variable', True), True)
    role.to_new()
    return jsonify_success(msg="创建成功")


@role_bp.route('/update', methods=['post'])
@get_params({'name': '请输入名称', 'id': '无指定ID', 'level': "请设置管理员等级"})
@permission_check_root()
def update():
    role = Role._q(Role.id == g.id)
    if not role:
        return jsonify_fail(msg="无指定的修改角色")
    if not role.is_variable:
        return jsonify_fail(msg="该角色无法修改")
    old_role = Role._q(Role.name == g.name)
    if old_role and old_role != role:
        return jsonify_fail(msg="该角色名称已经存在")
    role.name = g.name
    role.level = str_to_int(g.level)
    if role.level < 1:
        return jsonify_fail(msg="管理员等级 不能小于1")
    role.is_variable = str_to_bool(g.params.get('is_variable', True), True)
    role.to_save()
    return jsonify_success(msg="修改成功")


@role_bp.route('/variable', methods=['post'])
@get_params({'id': '无指定ID'})
@permission_check_root()
def variable():
    # 设置可以修改
    role = Role._q(Role.id == g.id)
    if not role:
        return jsonify_fail(msg="无指定的修改角色")
    if role.level < 1:
        return jsonify_fail(msg="该角色无法修改")
    role.is_variable = True
    role.to_save()
    return jsonify_success(msg="修改成功")


@role_bp.route('/delete', methods=['post'])
@get_params({'id': '无指定ID'})
@permission_check_root()
def delete():
    role = Role._q(Role.id == g.id)
    if not role:
        return jsonify_fail(msg="无制定的修改角色")
    if not role.is_variable or role.level < 1:
        return jsonify_fail(msg="该角色无法修改")

    role.to_delete()
    return jsonify_success(msg="删除成功")


@role_bp.route('/all', methods=['get'])
@permission_check_root()
def alist():
    # 角色列表，不分页
    level = 0
    manager_id = g.params.get('manager_id', '')
    if not is_none_str(manager_id) and len(manager_id) > 0:
        manager = User._q(User.id == manager_id)
        if manager:
            level = manager.role.level
    role_list = Role._q_all(Role.level > level)
    return jsonify_success(data=[role.to_json() for role in role_list])


@role_bp.route('/all_page', methods=['get'])
@permission_check_root()
def list_page():
    # 角色列表，分页
    role_list, total = Role._q_page()
    return jsonify_list_page(data=[role.to_json() for role in role_list], total=total)
