from flask import Blueprint, g

from zm_user.models.unit import Unit
from zm_user.tools.jsonify import jsonify_fail, jsonify_success, jsonify_list_page
from zm_user.tools.params import get_params
from zm_user.tools.permission import permission_check_root

unit_bp = Blueprint('unit_bp', __name__)


@unit_bp.route('/add', methods=['post'])
@get_params({'name': '请输入单位名称', 'short_name': '请输入单位简称'})
@permission_check_root()
def add():
    role = Unit._q(Unit.name == g.name)
    if role:
        return jsonify_fail(msg="该单位名称已经存在")
    role = Unit()
    role.name = g.name
    role.short_name = g.short_name
    role.to_save()
    return jsonify_success(msg="创建成功")


@unit_bp.route('/update', methods=['post'])
@get_params({'name': '请输入名称', 'id': '无指定ID', 'short_name': '请输入单位简称'})
@permission_check_root()
def update():
    role = Unit._q(Unit.id == g.id)
    if not role:
        return jsonify_fail(msg="无制定的修改角色")

    old_role = Unit._q(Unit.name == g.name)
    if old_role and old_role != role:
        return jsonify_fail(msg="该角色名称已经存在")
    role.name = g.name
    role.short_name = g.short_name
    role.to_save()
    return jsonify_success(msg="修改成功")


@unit_bp.route('/delete', methods=['post'])
@get_params({'id': '无指定ID'})
@permission_check_root()
def delete():
    role = Unit._q(Unit.id == g.id)
    if not role:
        return jsonify_fail(msg="无制定单位")
    role.to_delete()
    return jsonify_success(msg="删除成功")


@unit_bp.route('/all', methods=['get'])
@permission_check_root()
def alist():
    # 列表，不分页
    role_list = Unit._q_all()
    return jsonify_success(data=[role.to_json() for role in role_list])


@unit_bp.route('/all_page', methods=['get'])
@permission_check_root()
def list_page():
    # 列表，分页
    role_list, total = Unit._q_page()
    return jsonify_list_page(data=[role.to_json() for role in role_list], total=total)
