import os
import sys
from datetime import datetime

# Do not touch these. They use the local Async PRAW over the global Async PRAW.
sys.path.insert(0, ".")
sys.path.insert(1, "..")

from asyncpraw import __version__

copyright = datetime.today().strftime("%Y, Joel Payne")
exclude_patterns = ["_build"]
extensions = ["sphinx.ext.autodoc", "sphinx.ext.intersphinx", "sphinxcontrib_trio"]
html_static_path = ["_static"]
html_theme = "sphinx_rtd_theme"
html_theme_options = {"collapse_navigation": True}
htmlhelp_basename = "Async PRAW"
intersphinx_mapping = {"python": ("https://docs.python.org", None)}
master_doc = "index"
nitpick_ignore = [
    ("py:class", "IO"),
    ("py:class", "asyncprawcore.requestor.Requestor"),
    ("py:class", "asyncpraw.models.redditors.PartialRedditor"),
]
nitpicky = True
project = "Async PRAW"
pygments_style = "sphinx"
release = __version__
source_suffix = ".rst"
suppress_warnings = ["image.nonlocal_uri"]
version = ".".join(__version__.split(".", 2)[:2])


# Use RTD theme locally
if not os.environ.get("READTHEDOCS"):
    import sphinx_rtd_theme

    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]


def skip(app, what, name, obj, skip, options):
    if name in {
        "__call__",
        "__contains__",
        "__getitem__",
        "__init__",
        "__iter__",
        "__len__",
    }:
        return False
    return skip


def setup(app):
    app.connect("autodoc-skip-member", skip)
    app.add_css_file("theme_override.css")
