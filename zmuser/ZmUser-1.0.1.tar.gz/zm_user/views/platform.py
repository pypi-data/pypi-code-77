from flask import Blueprint, g

from zm_user.models.platform import Platform
from zm_user.models.user import User
from zm_user.tools.jsonify import jsonify_fail, jsonify_success, jsonify_list_page
from zm_user.tools.params import get_params
from zm_user.tools.permission import permission_check_root
from zm_user.tools.string_help import is_none_str

platform_bp = Blueprint('platform_bp', __name__)


@platform_bp.route('/add', methods=['post'])
@get_params({'name': '请输入项目名称'})
@permission_check_root()
def add():
    platform = Platform._q(Platform.name == g.name)
    if platform:
        return jsonify_fail(msg="该项目名称已经存在")
    platform = Platform()
    platform.name = g.name
    platform.to_save()
    return jsonify_success(msg="创建成功")


@platform_bp.route('/update', methods=['post'])
@get_params({'name': '请输入项目名称', 'id': '无指定ID'})
@permission_check_root()
def update():
    platform = Platform._q(Platform.id == g.id)
    if not platform:
        return jsonify_fail(msg="无制定的修改角色")

    old_platform = Platform._q(Platform.name == g.name)
    if old_platform and old_platform != platform:
        return jsonify_fail(msg="该项目名称已经存在")
    platform.name = g.name
    platform.to_save()
    return jsonify_success(msg="修改成功")


@platform_bp.route('/delete', methods=['post'])
@get_params({'id': '无指定ID'})
@permission_check_root()
def delete():
    platform = Platform._q(Platform.id == g.id)
    if not platform:
        return jsonify_fail(msg="无制定单位")
    platform.to_delete()
    return jsonify_success(msg="删除成功")


@platform_bp.route('/all', methods=['get'])
@permission_check_root()
def alist():
    # 列表，不分页
    manager_id = g.params.get('manager_id', '')
    if not is_none_str(manager_id) and len(manager_id) > 0:
        manager = User._q(User.id == manager_id)
        if manager:
            return jsonify_success(data=[platform.to_json() for platform in manager.platform_list])

    platform_list = Platform._q_all()
    return jsonify_success(data=[platform.to_json() for platform in platform_list])


@platform_bp.route('/all_page', methods=['get'])
@permission_check_root()
def list_page():
    # 列表，分页
    platform_list, total = Platform._q_page()
    return jsonify_list_page(data=[platform.to_json() for platform in platform_list], total=total)
