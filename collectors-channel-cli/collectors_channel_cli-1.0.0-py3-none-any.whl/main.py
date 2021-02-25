import typer
import os, sys
from dotenv import load_dotenv
from pymongo import MongoClient
import json
from pathlib import Path
from os.path import expanduser

DEFAULT_COLLECTIONS = ['amazon', 'famdvd', 'theoriginals', 'videoperola']

app = typer.Typer()


@app.command()
def find(title, title_type=None, site=None):

    data = []

    if site: 
        data = find_in_site(title, title_type, site)
    else: 
        for site in DEFAULT_COLLECTIONS: 
            data = find_in_site(title, title_type, site, data)

    json_dumped = json.dumps(data, indent=4, ensure_ascii=False)
    typer.echo(json_dumped)


@app.command()
def sites():
    typer.echo(json.dumps(DEFAULT_COLLECTIONS, indent=4))


def find_in_site(title, title_type, site, data = []): 

    client, col = connect_to_mongodb(site)
    result = find_in_mongodb(col, title, title_type)
    close_mongodb_connection(client)

    for item in result: 
        rename_item_id(item)
        data.append(item)

    return data


def rename_item_id(item): 
    id_item = str(item['_id'])
    del item['_id']
    item.update(id = id_item)
    return item


def connect_to_mongodb(site): 
    client = MongoClient(os.environ['MONGO_URL'])
    db = client.movies
    col = db[site]
    return client, col


def close_mongodb_connection(client): 
    if client: 
        client.close()


def find_in_mongodb(col, title, title_type): 
    
    if title_type: 
        db_result = list(col.find({'title': {'$regex': title, '$options': 'i'}, 'title_type': {'$regex': title_type, '$options': 'i'}}))
    else: 
        db_result = list(col.find({'title': {'$regex': title, '$options': 'i'}}))
    
    return list(db_result)


def check_env_file_exists():

    env_file = os.path.join(expanduser("~"), '.cc/my.properties')
    env_file_path = Path(env_file)

    if env_file_path.is_file():
        load_dotenv(env_file)
    else:
        typer.echo(typer.style("Properties file not found at '{}'".format(env_file), fg=typer.colors.RED), err=True)
        sys.exit()


def setup(): 
    check_env_file_exists()
    app()


if __name__ == "__main__":
    setup()
