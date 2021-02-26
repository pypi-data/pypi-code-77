import os

import click
from dbfread import DBF


@click.command()
@click.argument("filepath")
@click.option("-e", "--encoding", default="gb18030")
@click.option("-o", "--output")
@click.option("-t", "--title")
def cli(filepath, encoding, output, title):
    table = DBF(filepath, encoding=encoding, char_decode_errors="ignore")
    base_filename = os.path.basename(filepath)
    if base_filename.endswith(".dbf"):
        base_filename = base_filename[:-4]
    if output is None:
        output = base_filename + ".html"
    if title is None:
        title = base_filename
    content = """
    <!DOCTYPE html>
    <html lang="zh">
    <head>
    <meta charset="UTF-8">
    <title>
    """
    content += title
    content += """</title>
    <style>
        .dbf-table {
            margin: 20px;
            border-radius: 5px;
            font-size: 12px;
            border: none;
            border-collapse: collapse;
            max-width: 100%;
            white-space: nowrap;
            word-break: keep-all;
        }

        .dbf-table th {
            text-align: left;
            font-size: 20px;
        }

        .dbf-table tr {
            display: table-row;
            vertical-align: inherit;
            border-color: inherit;
        }

        .dbf-table tr:hover td {
            background: #00d1b2;
            color: #F8F8F8;
        }

        .dbf-table td, .dbf-table th {
            border-style: none;
            border-top: 1px solid #dbdbdb;
            border-left: 1px solid #dbdbdb;
            border-bottom: 3px solid #dbdbdb;
            border-right: 1px solid #dbdbdb;
            padding: .5em .55em;
            font-size: 15px;
        }

        .dbf-table td {
            border-style: none;
            font-size: 15px;
            vertical-align: center;
            border-bottom: 1px solid #dbdbdb;
            border-left: 1px solid #dbdbdb;
            border-right: 1px solid #dbdbdb;
            height: 30px;
        }

        .dbf-table tr:nth-child(even) {
            background: #F8F8F8;
        }
    </style>
    </head>
    <body>
    <table class="dbf-table">
    <tr>
    """
    for field in table.field_names:
        content += "<th>" + field + "</th>\n"
    content += "</tr>\n"

    for dic in table.records:
        content += "<tr>"
        for item in dic.values():
            content += "<td>" + str(item) + "</td>\n"
        content += "</tr>\n"
    content += "</table></body></html>"
    with open(output, "w") as f:
        f.write(content)
