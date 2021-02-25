import logging
import time
import json
import socket
from flask import abort, Response
from datetime import datetime, timedelta
from pymongo.cursor import Cursor
from bson.objectid import ObjectId
from flask import abort, Response

logging.basicConfig(
    level=logging.WARNING,
    format='[%(asctime)s] [%(levelname)s] %(message)s'
)


def handle_date(date: str, date_type='start') -> datetime:
    try:
        if not date:
            date_data = None
        elif date.isdigit():
            date_time = date[:10]
            date_data = datetime.fromtimestamp(int(date_time))
        else:
            date_data = datetime.strptime(date, "%Y-%m-%d")
            if date_type == 'end' and date_data:
                date_data += timedelta(hours=23, minutes=59, seconds=59)
        return date_data
    except Exception as err:
        handle_abnormal(
            message='日期字符串解析异常',
            status=400,
            other={'prompt': str(err)}
        )


def handle_db_to_list(db_cursor: Cursor) -> list:
    """
    将db列表数据，转换为list（原db的id是ObjectId类型，转为json会报错）
    :param db_cursor:db列表数据（find()获取）
    :return:转换后的列表
    """
    if not isinstance(db_cursor, Cursor):
        handle_abnormal(
            message='类型必须是 %s (获取类型为 %s)' % (Cursor, type(db_cursor)),
            status=500,
        )
    result = []
    for db in db_cursor:
        result.append(handle_db_dict(db_dict=db))
    return result


def handle_db_dict(db_dict: dict) -> dict:
    try:
        db_dict['id'] = str(db_dict['_id'])
        del db_dict['_id']
        # 创建时间和更新时间如果不存在，则设置为当前时间
        db_dict['creation_time'] = db_dict.get(
            'creation_time', datetime.today())
        db_dict['update_time'] = db_dict.get('update_time', datetime.today())
        # 将日期格式的时间，转化为13位时间戳
        db_dict['creation_time'] = int(time.mktime(
            db_dict['creation_time'].timetuple())) * 1000
        db_dict['update_time'] = int(time.mktime(
            db_dict['update_time'].timetuple())) * 1000
        return db_dict
    except Exception as err:
        handle_abnormal(
            message='MongoDB 数据字典解析异常',
            status=500,
            other={'prompt': str(err)}
        )


def handle_db_id(data_dict: dict) -> dict:
    if not isinstance(data_dict, dict):
        handle_abnormal(
            message='类型错误，预期 %s ,却得到 %s' % (dict, type(id)),
            status=400,
        )
    try:
        if data_dict.__contains__('_id') and isinstance(data_dict['_id'], str):
            data_dict['_id'] = ObjectId(str(data_dict['_id']))
        elif data_dict.__contains__('id'):
            if isinstance(data_dict['id'], str):
                data_dict['_id'] = ObjectId(str(data_dict['id']))
            else:
                data_dict['_id'] = data_dict['id']
            del data_dict['id']
        # 处理批量操作时，字符串类型ID问题
        if isinstance(data_dict['_id'], dict):  # id是列表
            for key, value in data_dict['_id'].items():
                if isinstance(value, list):  # 查找ID是列表
                    for i in range(len(value)):
                        if isinstance(value[i], str):  # 是字符串
                            data_dict['_id'][key][i] = ObjectId(str(value[i]))
        return data_dict
    except Exception as err:
        handle_abnormal(
            message='MongoDB _id 格式解析异常',
            status=400,
            other={'prompt': str(err)}
        )


def handle_db_remove(find_dict: dict) -> dict:
    try:
        if not find_dict.__contains__('remove_time'):
            # 设置搜索条件为不存在remove_time字段的文件
            find_dict['remove_time'] = {'$exists': False}
        # 返回设置后的搜索条件
        return find_dict
    except Exception as err:
        handle_abnormal(
            message='MongoDB 移除数据处理异常',
            status=500,
            other={'prompt': str(err)}
        )


def handle_abnormal(message: str, status: int, header: dict = {'Content-Type': 'application/json'}, other: dict = {}, is_raw: bool = False):
    logging.warning(message)
    host_name = socket.gethostname()
    return_body = {
        'message': message,
        'server_time': int(datetime.today().strftime('%Y%m%d%H%M%S')) * 1000,
        'host_name': host_name,
        'host_ip': socket.gethostbyname(host_name),
    }
    return_body.update(other)
    if is_raw:
        return return_body, status, header
    else:
        abort(Response(json.dumps(return_body), status, header))
