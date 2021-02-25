import panel as pn


def url_link_button(url, label="Visit auth URL"):
    html_pane = pn.pane.HTML(f"""
    <a id="log-in-link" class="nav-link" href="{url}" target="_blank">
        {label}
    </a>""",
    style={"cursor": "pointer",
            "border": "1px solid #ddd",
            "border-radius": "4px",
            "padding": "5px",
            "background-color": "#ff9900"
            })
    return html_pane