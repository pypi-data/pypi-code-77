import requests
import json

from tasq_cli.settings import SERVER, TOKEN
from tasq_cli import settings
from tasq_cli.server import make_request

logger = None

def make_request(url, post_data={}):
    logger.info(f'request {url=} {post_data=}')
    full_url = SERVER + url
    headers={'Authorization': f'BEARER {TOKEN}'}
    if post_data:
        r = requests.post(
            full_url,
            headers={'Authorization': f'BEARER {TOKEN}'},
            data = post_data
        )
    else:
        r = requests.get(
            full_url,
            headers=headers
        )
    if not 200 <= r.status_code < 400:
        r.raise_for_status()
    return r

def run_job(args):
    global logger
    logger = settings.get_logger()
    url = f'/jobs'
    tag = args.tag
    data = {
        "name": "",
        "include_model": False,
        "tags": [f"{tag}"],
        "exclude_tags": [],
        "max_resources": None,
        "for_qualification": False,
        "project_id": args.project_id,
        "project_resource_ids": []
    }
    r = make_request(url, post_data=data)
    data = r.json()['data']
    del data['relationships']
    print(data)
    return


def list_jobs(args):
    global logger
    logger = settings.get_logger()
    url = f'/jobs/?filter[project]={args.project_id}&sort=-id&page[size]=100'
    r = make_request(url)
    data = r.json()['data']
    for j in data:
        del(j['relationships'])
    print(json.dumps(data))
    return


def run_job(args):
    global logger
    logger = settings.get_logger()
    url = f'/jobs'
    tag = args.tag
    data = {
        "name": "",
        "include_model": False,
        "tags": [f"{tag}"],
        "exclude_tags": [],
        "max_resources": None,
        "for_qualification": False,
        "project_id": args.project_id,
        "project_resource_ids": []
    }
    r = make_request(url, post_data=data)
    data = r.json()['data']
    del data['relationships']
    print(data)
    return

def export_job(args):
    global logger
    logger = settings.get_logger()
    type = 'target'
    if args.raw:
        type='raw'
    url = f'/jobs/{args.job_id}/download/?export_type={type}&all_judgements=false'
    r = make_request(url)
    data = r.json()
    print(data)
    return
