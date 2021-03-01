#! /usr/bin/env python3
"""
@author  : MG
@Time    : 2021/1/26 下午10:13
@File    : import_data.py
@contact : mmmaaaggg@163.com
@desc    : 用于将办公室与家里的数据通过邮件方式进行同步
"""
import logging
import os

import pandas as pd

from vnpy_extra.db.orm import database
from vnpy_extra.utils.get_email import download_email_attachment

logger = logging.getLogger()


@database.atomic()
def email_attachment_2_tables(email_title, password):
    attachment_dic = download_email_attachment(email_title, password=password)
    data_len = len(attachment_dic)

    for num, (file_name, io) in enumerate(attachment_dic.items(), start=1):
        table_name, _ = os.path.splitext(file_name)
        df = pd.read_csv(io)
        fields = list(df.columns)
        fields_str = "`" + "`,`".join(fields) + "`"
        values_str = ",".join(["%s" for _ in fields])
        sql_str = f"""replace into {table_name} ({fields_str}) values({values_str})"""
        for row in df.to_dict(orient='record'):
            if 'id_name' in fields and pd.isna(row['id_name']):
                # some dirty data has to be clean
                continue
            database.execute_sql(
                sql_str,
                [None if pd.isna(row[_]) else row[_] for _ in fields])

        logger.info("%d/%d) %s 同步完成 %d 条数据", num, data_len, table_name, df.shape[0])


@database.atomic()
def csv_2_tables(dir_path):
    file_name_list = os.listdir(dir_path)
    data_len = len(file_name_list)
    for num, file_name in enumerate(file_name_list, start=1):
        table_name, ext = os.path.splitext(file_name)
        if ext != '.csv':
            continue
        df = pd.read_csv(os.path.join(dir_path, file_name))
        fields = list(df.columns)
        fields_str = "`" + "`,`".join(fields) + "`"
        values_str = ",".join(["%s" for _ in fields])
        sql_str = f"""replace into {table_name} ({fields_str}) values({values_str})"""
        for row in df.to_dict(orient='record'):
            if 'id_name' in fields and pd.isna(row['id_name']):
                # some dirty data has to be clean
                continue
            database.execute_sql(
                sql_str,
                [None if pd.isna(row[_]) else row[_] for _ in fields])

        logger.info("%d/%d) %s 同步完成 %d 条数据", num, data_len, table_name, df.shape[0])


if __name__ == "__main__":
    csv_2_tables(r'C:\Users\zerenhe-lqb\Downloads\data.tar')
