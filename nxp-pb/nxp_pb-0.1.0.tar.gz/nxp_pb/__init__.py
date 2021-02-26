#!/usr/bin/env python3
#-*-coding:utf-8-*-

import sys
import psycopg2
import psycopg2.extras


class DbModel:

    class ResultData:
        def __init__(self, date, branch, build_name, build_number, country, platform, scope, total_cases, pass_num, fail_num):
            self.data = (
                date,
                branch,
                build_name,
                build_number,
                country,
                platform,
                scope,
                total_cases,
                pass_num,
                fail_num
            )

    def __init__(self, host, port, user, password, database):
        self.conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def close(self):
        self.cur.close()
        self.conn.close()

    def __insert_db(self, component, result_data):
        sql = "INSERT INTO {} (date,branch,build_name,build_number,country,platform,scope,total_cases,pass_num,fail_num) VALUES ('{}', '{}', '{}', {}, '{}', '{}', '{}', {}, {}, {})".format(component, *result_data.data)
        print("SQL: " + sql)

        self.cur.execute(sql)
        self.conn.commit()

    def __update_db(self, component, result_data):
        sql = "UPDATE {} SET total_cases={}, pass_num={}, fail_num={} WHERE date='{}' AND branch='{}' AND build_name='{}' AND build_number={} AND country='{}' AND platform='{}' AND scope='{}'".format(component, *(result_data.data[-3:] + result_data.data[:7]))
        print("SQL: " + sql)

        self.cur.execute(sql)
        self.conn.commit()

    def log_into_db(self, component, result_data):
        sql = "SELECT * FROM {} WHERE date='{}' AND branch='{}' AND build_name='{}' AND build_number={} AND country='{}' AND platform='{}' AND scope='{}'".format(component, *result_data.data[:7])
        print("SQL: " + sql)

        self.cur.execute(sql)
        data = self.cur.fetchone()
        if data:
            print("Record exists, update it.")
            self.__update_db(component, result_data)
        else:
            print("No record, insert it.")
            self.__insert_db(component, result_data)


def main():
    if len(sys.argv[1:]) != 11:
        print("Wrong parameter number.")
        sys.exit(1)

    # result_data = DbModel.ResultData(
        # "03/31/2020",
        # "imx_5.4.y trunk",
        # "Linux_IMX_Regression_Next_Kernel",
        # 160,
        # "CN",
        # "I.MX8MM",
        # "weekend",
        # 100,
        # 99,
        # 1
    # )
    result_data = DbModel.ResultData(*sys.argv[2:])

    db_model = DbModel(
        "10.192.225.199",
        5433,
        "pbadmin",
        "pbadmin123",
        "pb"
    )
    # db_model.log_into_db("bsp", result_data)
    db_model.log_into_db(sys.argv[1], result_data)
    db_model.close()
    print("done")


if __name__ == "__main__":
    main()
