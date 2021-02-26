from html import escape
from datetime import datetime

from atlassian import Confluence
from jinja2 import Environment, PackageLoader, select_autoescape

from .html_coverage import HTMLData
from .models import Module


def make_table(rows):
    # TODO: use templating
    table = "<table><tbody><tr><th>Name</th><th>Status (OK/Total)</th><th>Status (%)</th></tr>"
    for name, status, prc_status in rows:
        table += (
            '<tr><td><pre>{}</pre></td><td style="text-align: right;">{}</td>'
            '<td style="text-align: right;">{:.2f}%</td></tr>'
        ).format(name, status, prc_status)
    table += "</tbody></table>"
    return table


def make_report_rows(module, indent=0):
    rows = []
    for (item_name, value) in module.modules.items():
        if isinstance(value, Module):
            ok, total, prc_ok = value.stats
            name = " " * indent + escape(item_name.split("::")[-1])
            rows.append((name, "{}/{}".format(ok, total), prc_ok))
            rows.extend(make_report_rows(value, indent + 4))
    return rows


def get_confluence_setup(config, feature_prefix):
    track_config = config.inicfg.config.sections["pytest_track"]
    api = Confluence(
        url=track_config["confluence_url"],
        username=track_config["confluence_username"],
        password=track_config["confluence_password"],
    )
    parent_id = track_config["confluence_{}_parent_page_id".format(feature_prefix)]
    page_title = track_config["confluence_{}_page_title".format(feature_prefix)]
    return api, parent_id, page_title


def upload_to_confluence(config, body: str, feature_prefix: str):
    api, parent_id, page_title = get_confluence_setup(config, feature_prefix)
    page_title = page_title.format(datetime.now())  # allow dates in names
    response = api.update_or_create(parent_id, page_title, body=body)
    links = response["_links"]
    page_url = "{}{}".format(links["base"], links["webui"])
    print("Page available at {}".format(page_url))


def upload_track_report(report, config):
    rows = make_report_rows(report.tests)
    body = "<p>{}</p>".format(make_table(rows))
    upload_to_confluence(config, body, feature_prefix="report")


def make_html_coverage_page():
    pass


def upload_html_coverage_report(html_data: HTMLData, config):
    html_data.stats(should_print=False)

    loader = PackageLoader("pytest_track")
    env = Environment(
        loader=loader,
        autoescape=select_autoescape(["html"]),
    )
    template = env.get_template("html_coverage.html")
    body = template.render({"data": html_data})
    upload_to_confluence(config, body, feature_prefix="coverage")
