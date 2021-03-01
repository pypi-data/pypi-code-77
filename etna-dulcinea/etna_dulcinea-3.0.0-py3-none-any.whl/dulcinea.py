#!/usr/bin/env python3

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import json
import os
import shutil
from typing import Any, Dict, List, Optional
from uuid import uuid4

from panza.jobs import new_job_workspace
from panza.cache import Cache
from panza.config import PanzaConfiguration, AdditionalDockerDaemonConfiguration
from quixote import Fetcher
from quixote.fetch.copy import copy
from quixote.inspection import Scope

from dulcinea import metadata, colored_output, simple_output


def create_argument_parser():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-c", "--context-file", type=str)
    info_parser_group = arg_parser.add_mutually_exclusive_group()
    info_parser_group.add_argument("-i", "--info-file", type=str)
    info_parser_group.add_argument("--auto-info", action='store_true')
    arg_parser.add_argument("-r", "--root-dir", type=str, default="/tmp")
    arg_parser.add_argument("--docker-bridge-ip", type=str, default="10.9.8.7/24")
    arg_parser.add_argument("--override-deliveries", type=str)
    arg_parser.add_argument("--integrate", action='store_true', help=argparse.SUPPRESS)
    arg_parser.add_argument("--keep-artifacts", action='store_true', help='Keep artifacts even after a successful run')
    arg_parser.add_argument("--no-colors", action='store_true', help='Disable colorized output')
    arg_parser.add_argument("--version", action='version', version='%(prog)s {}'.format(metadata.__version__))
    arg_parser.add_argument("moulinette_directory", type=str)
    return arg_parser


def load_context_file(path: Optional[str]) -> Dict[str, Any]:
    ctx = {}
    if path is not None:
        with open(path, 'r') as context_file:
            ctx = json.load(context_file)
    return ctx


def load_info(cmd_args, arg_parser) -> List[Dict]:
    if cmd_args.info_file:
        with open(cmd_args.info_file, 'r') as info_file:
            return json.load(info_file)
    elif cmd_args.auto_info:
        if cmd_args.override_deliveries is None:
            arg_parser.error("cannot use '--auto-info' without '--override-deliveries'")
        return sorted(
            [{"group_id": entry} for entry in os.listdir(cmd_args.override_deliveries)
             if os.path.isdir(f"{cmd_args.override_deliveries}/{entry}")],
            key=lambda d: d["group_id"]
        )
    else:
        arg_parser.error("missing either '--info-file' or '--auto-info'")


def generate_output_lines(scope, indent=0):
    for entry in scope.entries:
        if isinstance(entry, Scope):
            sub_entries = [e for e in generate_output_lines(entry, indent + 2 * (not entry.hidden))]
            if sub_entries:
                if entry.hidden is False:
                    yield " " * indent + entry.name
                for sub_entry in sub_entries:
                    yield sub_entry
        else:
            assert isinstance(entry, dict)
            if "requirements" in entry:
                ok, req = entry["requirements"]
                if not ok:
                    yield " " * indent + "requirement failed: " + str(req)
            elif "assertion_failure" in entry:
                yield " " * indent + "assertion failed: " + entry["assertion_failure"]
            elif "information" in entry:
                yield " " * indent + "information: " + entry["information"]


def generate_output(scope) -> str:
    return "\n".join(generate_output_lines(scope))


def has_any_failure(scope) -> bool:
    for entry in scope.entries:
        if isinstance(entry, Scope):
            if has_any_failure(entry):
                return True
        else:
            if "requirements" in entry:
                ok, _ = entry["requirements"]
                if not ok:
                    return True
            elif "assertion_failure" in entry:
                return True
    return False


def has_crashed(result: Dict[str, Any]) -> bool:
    return "error" in result


def any_unexpected_status(results) -> bool:
    for name, result in results:
        if has_crashed(result):
            return True
        job_result = result["result"]
        if has_any_failure(job_result):
            if name.startswith("OK"):
                return True
        else:
            if name.startswith("KO"):
                return True
    return False


@dataclass
class JobRunner:
    moulinette_directory: str
    run_directory: str
    context: Dict[str, Any]
    cache: Cache
    override_deliveries_directory: Optional[str]
    panza_config: PanzaConfiguration

    def create_workspace(self, info, tag):
        job_name = f"{info['module_id']}-{info['activity_id']}-{info['group_id']}_{tag}"
        return new_job_workspace(self.panza_config, self.moulinette_directory, job_name)

    def build_environment(self, workspace, info):
        environment_name = f"dulcinea-{info['module_id']}-{info['activity_id']}"
        return workspace.build_job_environment(environment_name)

    def fetch_data(self, handle, info):
        if self.override_deliveries_directory is not None:
            handle.blueprint.fetchers = [Fetcher(lambda: copy(self.override_deliveries_directory))]
        return handle.fetch_data(context={**info, **self.context}, cache=self.cache)

    def execute_job(self, workspace, info) -> Dict[str, Any]:
        return workspace.execute_job(context={**info, **self.context})


def run_jobs(runner, output, infos) -> List:
    defaults = {
        "leader": "login_x",
        "request_date": datetime.now(timezone.utc).astimezone().strftime('%Y-%m-%dT%H:%M:%S%z'),
        "module_id": 1,
        "activity_id": 1,
    }

    results = []

    with output.progress(len(infos) * 3) as progress:
        for n, info in enumerate(infos):
            try:
                if "group_id" not in info:
                    output.logger.warning(f"missing mandatory field 'group_id' in {info}, skipping")
                    continue
                for k, v in defaults.items():
                    info.setdefault(k, v)

                output.horizontal_rule(f"[bold bright_green]Running job with group ID {info['group_id']}")

                workspace = runner.create_workspace(info, tag=n)
                workspace = runner.build_environment(workspace, info)
                progress.advance()
                workspace = runner.fetch_data(workspace, info)
                progress.advance()
                result = runner.execute_job(workspace, info)
                progress.advance()
                results.append((str(info['group_id']), result))
            except Exception as e:
                print(f"Cannot execute job for delivery {info['group_id']}: {str(e)}")
                results.append((str(info['group_id']), {"error": f"Cannot execute job: {str(e)}"}))

    return results


def print_results(output, results):
    output.print("\n[bold]RESULTS[/]")
    for name, result in results:
        output.print(f"\nResult for group {name}")
        if has_crashed(result):
            output.print("Status: [bold red]CRASH")
            output.print(result["error"], raw=True)
        else:
            job_result = result["result"]
            if not has_any_failure(job_result):
                output.print("Status: [green]OK[/], all tests passed")
            else:
                output.print("Status: [red]KO")
            output.print(generate_output(job_result), raw=True)


def main():
    arg_parser = create_argument_parser()
    args = arg_parser.parse_args()

    context = load_context_file(args.context_file)
    infos = load_info(args, arg_parser)
    output = simple_output.Output() if args.no_colors else colored_output.Output()

    run_dir = f"{args.root_dir}/dulcinea-{uuid4()}"
    output.logger.debug("Using run_dir=%s", run_dir)

    panza_config = PanzaConfiguration(
        root_directory=f"{run_dir}/workspaces",
        additional_docker_daemon=AdditionalDockerDaemonConfiguration(
            network_bridge_mask=args.docker_bridge_ip,
        )
    )
    cache = Cache.create_at(f"{run_dir}/fetcher_cache", max_entries=32, exist_ok=False)

    runner = JobRunner(args.moulinette_directory, run_dir, context, cache, args.override_deliveries, panza_config)

    results = run_jobs(runner, output, infos)

    got_unexpected_statuses = any_unexpected_status(results)
    if got_unexpected_statuses or args.keep_artifacts:
        output.logger.debug(f"Keeping run directory {run_dir}")
    else:
        shutil.rmtree(run_dir)

    print_results(output, results)

    if args.integrate and got_unexpected_statuses:
        output.print("Some jobs resulted in an unexpected status, integration failed")
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
