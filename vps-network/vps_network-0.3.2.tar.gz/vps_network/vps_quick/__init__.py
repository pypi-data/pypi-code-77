"""
快速测试 ping, traceroute, speed
"""

import logging
import os
import sys
from typing import Optional, List

import click
from rich.logging import RichHandler

from ..vps_api import NetworkApi
from ..vps_api.dt import PingForm, TraceForm, SpeedForm
from ..vps_ping import do_multi_ping
from ..vps_speed import (
    do_speed_test_wrap,
    get_cn_server_list,
    get_oversea_server_list,
    get_cc_server_list,
    ServerInfo,
)
from ..vps_trace import TraceResult, do_traceroute_v2_wrapper

__all__ = ["init_quick_cli"]


def cli_do_ping(
    hosts: dict,  # dict of ip to CC
    log: logging.Logger,
    ping_count: int,
    interval: float,
    timeout: int,
    job_id: Optional[str],
    api: NetworkApi,
):
    log.info(f"ping 测试 {hosts}....")
    ping_result = do_multi_ping(
        hosts, count=ping_count, interval=interval, timeout=timeout
    )

    ping_form = PingForm(job_id=job_id, results=ping_result)
    ret = api.ping_report(ping_form)
    if ret is not None and ret.errno == 0:
        log.info("上报 Ping 测试结果成功")
    else:
        log.error(f"上报 Ping 结果失败: {ret}")


def cli_do_trace(
    hosts: List[str],
    trace_count: int,
    interval: float,
    timeout: int,
    trace_hops: int,
    job_id: Optional[str],
    api: NetworkApi,
    log: logging.Logger,
):
    log.info(f"开始执行 traceroute {hosts} ...")
    trace_results: List[TraceResult] = []
    for host in hosts:
        p = do_traceroute_v2_wrapper(
            host=host,
            count=trace_count,
            interval=interval,
            timeout=timeout,
            max_hops=trace_hops,
        )
        if p is None:
            continue
        trace_results.append(p)

    trace_form = TraceForm(job_id=job_id, results=trace_results)
    ret = api.trace_report(trace_form)
    if ret.errno == 0:
        log.info("上报 Traceroute 测试结果成功")
    else:
        log.error(f"上报 traceroute 结果失败: {ret}")


def cli_do_speed_test(
    server_list: List[ServerInfo],
    job_id: Optional[str],
    api: NetworkApi,
    speed_disable: Optional[str],
    log: logging.Logger,
):
    all_list = server_list

    # do speed test
    speed_result = []
    for item in all_list:
        log.info(f"速度测试: {item.name} {item.sponsor} {item.host}")
        v = do_speed_test_wrap(server=str(item.id), disable=speed_disable)
        if v is None:
            log.error(f"速度测试: {item.name}({item.host=}, {item.id=}) 失败")
        else:
            log.info(f"速度测试: {item.name} 已完成")
            speed_result.append(v)

    speed_form = SpeedForm(job_id=job_id, results=speed_result)
    ret = api.speed_report(speed_form)
    if ret.errno == 0:
        log.info("上报速度测试结果成功")
    else:
        log.error(f"上报速度测试结果失败: {ret}")


def init_quick_cli(main: click.Group):
    @main.command()
    @click.option(
        "--app-key",
        type=str,
        required=True,
        help="上报数据的APPKey",
        default=lambda: os.environ.get("BENCH_APP_KEY", "").strip(),
        show_default="BENCH_APP_KEY",
    )
    @click.option(
        "--job-id",
        type=str,
        help="测试任务的ID",
        default=lambda: os.environ.get("VPS_JOB_ID", None),
    )
    @click.option("--out-dir", type=str, help="测试结果写入到目标目录")
    @click.option("--cc", type=str, help="测试目标国家,没有设置则随机选择 国内 和 海外")
    @click.option("--limit", type=int, help="要测试多少个服务器", default=16)
    @click.option("--ping-count", type=int, help="Ping 测试发送数据包的数量", default=8)
    @click.option("--trace-hops", type=int, help="Traceroute 最大跳", default=32)
    @click.option("--trace-count", type=int, help="Traceroute 发送数据包的数量", default=2)
    @click.option(
        "--interval", type=float, help="Ping/Trace 测试发送数据包的间隔时间", default=0.05
    )
    @click.option("--timeout", type=int, help="Ping/Trace 测试超时时间", default=3)
    @click.option(
        "--speed-disable",
        type=click.Choice(["up", "dl"], case_sensitive=False),
        help="禁止 上传/下载 测试, 不允许同时禁止",
    )
    @click.option("--no-ping-test", is_flag=True, help="禁止 Ping 测试")
    @click.option("--no-trace-test", is_flag=True, help="禁止 Traceroute 测试")
    @click.option("--no-speed-test", is_flag=True, help="禁止 Speed 测试")
    def quick(
        app_key: str,
        job_id: Optional[str],
        out_dir: Optional[str],
        cc: Optional[str],
        limit: Optional[int],
        ping_count: int,
        trace_hops: int,
        trace_count: int,
        interval: float,
        timeout: int,
        speed_disable: Optional[str],
        no_ping_test: bool,
        no_trace_test: bool,
        no_speed_test: bool,
    ):
        """
        VPS 网络快速测试
        """
        logging.basicConfig(  # noqa
            level="NOTSET",
            format="%(message)s",
            datefmt="[%X]",
            handlers=[RichHandler()],
        )

        log = logging.getLogger("rich")
        if len(app_key) == 0:
            log.error("没有配置 app key")
            sys.exit(2)

        job_id = None if job_id in ("", None) else job_id.strip()

        api = NetworkApi(app_key, out_dir=out_dir)

        # get server list
        log.info("开始获取服务器列表...")
        if cc is None:
            cn_list = get_cn_server_list(None, limit)
            oversea_list = get_oversea_server_list(None, limit)
            server_list = cn_list + oversea_list
        else:
            server_list = get_cc_server_list(cc, limit)

        if len(server_list) == 0:
            log.error("获取服务器列表失败")
            sys.exit(1)

        log.info(f"获取服务器列表成功: {server_list}")

        host_cc_dict = dict()
        for item in server_list:
            host_cc_dict[item.host.split(":")[0]] = item.cc

        if not no_ping_test:
            cli_do_ping(
                hosts=host_cc_dict,
                log=log,
                ping_count=ping_count,
                interval=interval,
                timeout=timeout,
                job_id=job_id,
                api=api,
            )

        hosts = []
        for item in server_list:
            hosts.append(item.host.split(":")[0])

        if not no_trace_test:
            cli_do_trace(
                hosts=hosts,
                trace_count=trace_count,
                interval=interval,
                timeout=timeout,
                trace_hops=trace_hops,
                job_id=job_id,
                api=api,
                log=log,
            )

        if not no_speed_test:
            cli_do_speed_test(
                server_list=server_list,
                job_id=job_id,
                api=api,
                speed_disable=speed_disable,
                log=log,
            )
