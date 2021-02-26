import json
from other.common.file.io import remove_if_exists, write_file

import mysql.connector

_HOST = 'localhost'
_PORT = '3311'
_USER = 'ucode'
_PASSWORD = 'ucode1234'
_DATABASE = 'ucode'


def get_ucode_user_token():
    mydb = mysql.connector.connect(
        host=_HOST,
        port=_PORT,
        user=_USER,
        password=_PASSWORD,
        database=_DATABASE
    )
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute(
        '''
        select t.token from user_token t 
        RIGHT JOIN user u on t.user_id = u.id
        where t.expired_at > NOW() and type='student' and u.is_deleted=0 and t.is_deleted=0
        '''
    )
    users = mycursor.fetchall()
    tokens = [user['token'] for user in users]
    remove_if_exists('other/common/database/variable/ucode_student_user_token.py')
    write_file('other/common/database/variable/ucode_student_user_token.py',
               'UCODE_STUDENT_USER_TOKEN = ' + json.dumps(tokens, indent=2))
    mycursor.close()
    mydb.close()
    return tokens
