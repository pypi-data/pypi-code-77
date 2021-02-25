import base64
from io import BytesIO

import psycopg2
from flask import Blueprint, g, redirect, request
from sqlalchemy import or_
from werkzeug.security import check_password_hash, generate_password_hash

from zm_user import Config
from zm_user.models.platform import Platform
from zm_user.models.role import Role
from zm_user.models.user import User
from zm_user.tools.jsonify import jsonify_fail, jsonify_success, jsonify_list_page
from zm_user.tools.params import get_params
from zm_user.tools.permission import permission_check_root, permission_check_login
from zm_user.tools.string_help import str_to_int, str_to_bool, is_none_str, is_phone, is_email

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/login', methods=['post'])
@get_params({'phone': '请输入账号', 'password': '请输入密码'})
def login():
    # 登录
    user = User._q(or_(User.phone == g.phone, User.email == g.phone))
    if not user:
        return jsonify_fail(code=10005, msg="该账号还未注册")
    if not check_password_hash(user.password, g.password):
        return jsonify_fail(code=10005, msg="密码错误")
    if not user.is_activated_email:
        return jsonify_fail(code=10005, msg="邮箱未激活，无法登录")
    if user.is_freeze:
        return jsonify_fail(code=10005, msg="该账号已经被冻结，无法登录")
    res = user.to_json()
    res.update({
        "bb_token": user.login_success()
    })
    return jsonify_success(msg="登录成功", data=res)


@user_bp.route('/logout', methods=['post'])
@permission_check_login()
def logout():
    # 退出登录
    g.user.logout()
    g.user.to_save()
    return jsonify_success(msg="退出成功")


@user_bp.route('/info', methods=['get'])
@permission_check_login()
def info():
    # 获取用户自己的详情
    return jsonify_success(data=g.user.to_json())


@user_bp.route('/detail', methods=['get'])
@get_params({'id': '无指定用户'})
@permission_check_root()
def detail():
    # 获取制定用户的详情
    user = User._q(User.id == g.id)
    if not user:
        return jsonify_fail(code=10005, msg="无指定用户")
    return jsonify_success(data=user.to_json())


@user_bp.route('/freeze', methods=['post'])
@get_params({'id': '无指定用户'})
@permission_check_root()
def freeze():
    # 冻结，冻结后禁止登录
    user = User._q(User.id == g.id)
    if not user:
        return jsonify_fail(code=10005, msg="无指定用户")
    if user.is_root():
        return jsonify_fail(code=10005, msg="root用户无法冻结")
    user.is_freeze = True
    user.to_save()
    return jsonify_success(msg="冻结成功")


@user_bp.route('/unfreeze', methods=['post'])
@get_params({'id': '无指定用户'})
@permission_check_root()
def unfreeze():
    # 解除冻结
    user = User._q(User.id == g.id)
    if not user:
        return jsonify_fail(code=10005, msg="无指定用户")
    if user.is_root():
        return jsonify_fail(code=10005, msg="root用户无法操作")
    user.is_freeze = False
    user.to_save()
    return jsonify_success(msg="解除冻结成功")


def set_user_info(user):
    db = Config.zm_user_db
    with db.session.no_autoflush:
        manager_id = g.params.get('manager_id', "")
        if not is_none_str(manager_id) and len(manager_id) > 0:
            manager = User._q(User.id == manager_id)
            if manager:
                user.manager_id = manager.id
                user.manager = manager

        platform_id_list = g.params.get('platform_id_list', "")
        if not is_none_str(platform_id_list) and len(platform_id_list) > 0:
            p_list = Platform._q_all(Platform.id.in_(platform_id_list))
            if user.manager:
                for p in p_list:
                    if p not in user.manager.platform_list:
                        return jsonify_fail(msg="{}平台不在范围内".format(p.name))
            user.platform_list = list(p_list)

        role_id = g.params.get('role_id', "")
        if not is_none_str(role_id) and len(role_id) > 0:
            print("role_id", role_id)
            role = Role._q(Role.id == role_id)
            if role:
                if role.level == 0:
                    return jsonify_fail(msg="无法设置为root用户")
                if user.manager and user.manager.role.level >= role.level:
                    return jsonify_fail(msg="所选角色等级过高")
                user.role_id = role_id
                user.role = role

    return True


@user_bp.route('/add', methods=['post'])
@get_params({'phone': '请输入手机号',
             'name': '请输入用户名',
             'email': '请输入邮箱',
             })
@permission_check_root()
def add():
    # 新增用户
    if not is_phone(g.phone):
        return jsonify_fail(msg="请输入正确的手机号")
    if not is_email(g.email):
        return jsonify_fail(msg="请输入正确的邮箱")
    user = User._q(or_(User.phone == g.phone))
    if user:
        return jsonify_fail(code=10005, msg="该手机号已经注册")
    user = User._q(or_(User.email == g.email))
    if user:
        return jsonify_fail(code=10005, msg="该邮箱已经注册")

    user = User()
    user.phone = g.phone
    user.email = g.email
    user.name = g.name
    res = set_user_info(user)
    if res == True:
        user.to_new()
        return jsonify_success(msg="创建成功")
    return res


@user_bp.route('/update', methods=['post'])
@get_params({'phone': '请输入手机号', 'name': '请输入用户名',
             'email': '请输入邮箱', 'id': '无指定ID'})
@permission_check_root()
def update():
    # 更新用户
    user = User._q(User.id == g.id)
    if not user:
        return jsonify_fail(msg="无指定用户")
    if not is_phone(g.phone):
        return jsonify_fail(msg="请输入正确的手机号")
    if not is_email(g.email):
        return jsonify_fail(msg="请输入正确的邮箱")
    old_user = User._q(or_(User.phone == g.phone))
    if old_user and old_user != user:
        return jsonify_fail(code=10005, msg="该手机号已经注册")
    old_user = User._q(or_(User.email == g.email))
    if old_user and old_user != user:
        return jsonify_fail(code=10005, msg="该邮箱已经注册")

    user.phone = g.phone
    user.email = g.email
    user.name = g.name
    res = True
    if not user.is_root():
        res = set_user_info(user)
    if res == True:
        user.to_save()
        return jsonify_success(msg="修改成功")
    return res


@user_bp.route('/activated_email', methods=['get'])
@get_params({'key': '激活码错误'})
def activated_email():
    # 邮箱激活
    user = User._q(User.email_activation_code == g.key).first()
    if user:
        user.is_activated_email = True
        user.to_save()
    if is_none_str(Config.activated_email_url):
        raise Exception("没有指定 activated_email_url")
    return redirect(Config.activated_email_url)


@user_bp.route('/update_avatar', methods=['post'])
@permission_check_login()
def update_avatar():
    f = request.files.get("file")
    g.user.avatar = BytesIO(f.read()).getvalue()
    g.user.to_save()
    return jsonify_success(data=g.user.get_avatar())


@user_bp.route('/update_pwd', methods=['post'])
@get_params({'old_pwd': '请输入旧密码', 'new_pwd': '请输入新密码'})
@permission_check_login()
def update_pwd():
    # 修改密码
    if not check_password_hash(g.user.password, g.old_pwd):
        return jsonify_fail(msg="原密码不正确")
    if len(g.new_pwd) < 6:
        return jsonify_fail(msg="新密码不能少于6位数")

    g.user.password = generate_password_hash(g.new_pwd)
    g.user.is_need_update_password = False
    g.user.to_save()
    return jsonify_success(msg="成功")


@user_bp.route('/init_pwd', methods=['post'])
@get_params({'id': '无制定用户'})
@permission_check_login()
def init_pwd():
    user = User._q(User.id == g.id)
    if not user:
        return jsonify_fail(msg="无指定用户")
    if user.is_root():
        return jsonify_fail(code=10005, msg="root用户无法操作")
    user.password = generate_password_hash("123456")
    user.is_need_update_password = True
    user.to_save()
    return jsonify_success(msg="密码初始化成功")


@user_bp.route('/delete', methods=['post'])
@get_params({'id': '无指定ID'})
@permission_check_root()
def delete():
    # 删除用户
    user = User._q(User.id == g.id)
    if not user:
        return jsonify_fail(code=10005, msg="无指定用户")
    if user.is_root():
        return jsonify_fail(code=10005, msg="root用户无法操作")
    user.to_delete()
    return jsonify_success(msg="删除成功")


@user_bp.route('/all', methods=['get'])
@permission_check_root()
def alist():
    # 用户列表，不分页
    user_list = User._q_all()
    return jsonify_success(data=[user.to_json() for user in user_list])


@user_bp.route('/all_page', methods=['get'])
@permission_check_root()
def all_page():
    # 用户列表，分页
    manager_id = g.params.get('manager_id', '')
    if is_none_str(manager_id):
        user_list, total = User._q_page(User.manager_id == None)
    else:
        user_list, total = User._q_page(User.manager_id == manager_id)
    return jsonify_list_page(data=[user.to_json() for user in user_list], total=total)
