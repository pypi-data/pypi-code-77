#!/usr/bin/env python3
#-*-coding:utf-8-*-

import sys
import logging
import psycopg2
import psycopg2.extras

logging.getLogger().setLevel(logging.INFO)
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(format=LOG_FORMAT)


class DbModel:

    db_clusters = {
        "host": "10.192.225.199",
        "user": "fadmin",
        "password": "fadmin123",
        "database": "farm_history",
        "port": {
            "Linux_Factory": 5501,
            "Linux_Factory_Dev": 5502,
            "Linux_Factory_Rebase": 5503,
            "Linux_Factory_Upstream_Kernel": 5504,
            "Linux_Factory_On_Demand": 5505,
        },
    }

    class Result:
        def __init__(self, result_header, result_body):
            self.result_header = result_header
            self.result_body = result_body

    class Info:
        def __init__(self):
            self.info = {}
            self.info_ret = {}

        def add_query(self, platform, case_list):
            self.info[platform] = case_list
            self.info_ret[platform] = {}
            for per_case in case_list:
                self.info_ret[platform].setdefault(per_case, {})
                self.info_ret[platform][per_case]["regression"] = 0
                self.info_ret[platform][per_case]["lastpass"] = 0

    def __init__(self, build_plan):
        self.build_plan = build_plan
        self.conn = psycopg2.connect(
            host=DbModel.db_clusters["host"],
            port=DbModel.db_clusters["port"][self.build_plan],
            user=DbModel.db_clusters["user"],
            password=DbModel.db_clusters["password"],
            database=DbModel.db_clusters["database"]
        )
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def close(self):
        self.cur.close()
        self.conn.close()

    def log_into_db(self, result):
        if result.result_header[0] != self.build_plan:
            logging.info("Reject non match data.")
            return

        logging.info("Start to inject data to database.")
        sql = "SELECT * FROM lf_history_meta WHERE scope='{}'".format(result.result_header[2])
        self.cur.execute(sql)
        data = self.cur.fetchone()
        if data:
            if result.result_header[0] == self.build_plan and result.result_header[1] == data["head"]: # means a resubmit for current dev job
                ifBackup2lastpass_1 = False
            else:
                ifBackup2lastpass_1 = True
        else:
            ifBackup2lastpass_1 = True

        for per_result in result.result_body:
            if ifBackup2lastpass_1:
                if per_result[2] == 0:
                    sql = "INSERT INTO lf_history_ss (scope,platform,testcase,lastpass,lastpass_1) VALUES ('{}', '{}', '{}', {}, 0) ON CONFLICT (scope,platform,testcase) DO UPDATE SET lastpass={}, lastpass_1=lf_history_ss.lastpass".format(result.result_header[2], per_result[0], per_result[1], result.result_header[1], result.result_header[1])
            else:
                if per_result[2] == 0:
                    sql = "INSERT INTO lf_history_ss (scope,platform,testcase,lastpass,lastpass_1) VALUES ('{}', '{}', '{}', {}, 0) ON CONFLICT (scope,platform,testcase) DO UPDATE SET lastpass={}".format(result.result_header[2], per_result[0], per_result[1], result.result_header[1], result.result_header[1])
            self.cur.execute(sql)

            sql = "INSERT INTO lf_history (build_plan,build_number,scope,platform,testcase,result) VALUES ('{}', {}, '{}', '{}', '{}', {}) ON CONFLICT (build_number,platform,scope,testcase) DO UPDATE SET result={}".format(*(result.result_header + per_result + per_result[-1:]))
            self.cur.execute(sql)

        sql = "INSERT INTO lf_history_meta (scope,head,head_1) VALUES ('{}', {}, {}) ON CONFLICT (scope) DO UPDATE SET head={}, head_1=lf_history_meta.head where lf_history_meta.head!={}".format(result.result_header[2], result.result_header[1], 0, result.result_header[1], result.result_header[1])
        self.cur.execute(sql)

        self.conn.commit()
        logging.info("End to inject data to database.")

    def get_from_db(self, info_header, info_body):
        logging.info("Start to fetch data.")
        sql = "SELECT * FROM lf_history_meta WHERE scope='{}'".format(info_header[2])
        self.cur.execute(sql)
        data = self.cur.fetchone()
        if data:
            if info_header[0] == self.build_plan and info_header[1] == data["head"]: # means a resubmit for current dev job
                index = data["head_1"]
                ss_index_column = "lastpass_1"
            else:
                index = data["head"]
                ss_index_column = "lastpass"

            # get regression
            sql = "SELECT platform, testcase, result FROM lf_history WHERE scope='{}' AND build_number={} AND testcase in {}".format(info_header[2], index, tuple(set(sum(info_body.info.values(), []))) + ('',))
            self.cur.execute(sql)
            data = self.cur.fetchall()
            for per_record in data:
                try:
                    info_body.info_ret[per_record["platform"]][per_record["testcase"]]
                    if per_record["result"] == 0:
                        info_body.info_ret[per_record["platform"]][per_record["testcase"]]["regression"] = 1
                except:
                    pass

            # get last pass
            sql = "SELECT * FROM lf_history_ss WHERE scope='{}' AND testcase in {}".format(info_header[2], tuple(set(sum(info_body.info.values(), []))) + ('',))
            self.cur.execute(sql)
            data = self.cur.fetchall()
            for per_record in data:
                try:
                    info_body.info_ret[per_record["platform"]][per_record["testcase"]]
                    info_body.info_ret[per_record["platform"]][per_record["testcase"]]["lastpass"] = per_record[ss_index_column]
                except:
                    pass
            logging.info("End to fetch data.")
            return(info_body.info_ret)
        else:
            logging.info("End to fetch data.")
            return(info_body.info_ret)


if __name__ == "__main__":
    db_model = DbModel("Linux_Factory_Dev")

    # simulate query
    info_header = (
        "Linux_Factory_Dev",
        36,
        "daily"
    )

    info_body = DbModel.Info()
    for p in ("I.MX8MM", "I.MX6QSD"):
        case_list = []
        if p == "I.MX8MM":
            case_list.append("CASE-0")
            case_list.append("CASE-1")
            case_list.append("CASE-2")
        if p == "I.MX6QSD":
            case_list.append("CASE-1")
            case_list.append("CASE-2")
            case_list.append("CASE-3")
        info_body.add_query(p, case_list)

    logging.info(db_model.get_from_db(info_header, info_body))

    # simulate insert
    result_header = (
        "Linux_Factory_Dev",
        36,
        "daily"
    )
    result_body = []
    for i in range(0, 2500):
        result_body.append(
            (
                "I.MX8MM",
                "CASE-{}".format(i),
                0
            )
        )
    for i in range(1, 2500):
        result_body.append(
            (
                "I.MX6QSD",
                "CASE-{}".format(i),
                1
            )
        )

    result = DbModel.Result(result_header, result_body)
    db_model.log_into_db(result)

    # cleanup
    db_model.close()
    logging.info("Done.")
