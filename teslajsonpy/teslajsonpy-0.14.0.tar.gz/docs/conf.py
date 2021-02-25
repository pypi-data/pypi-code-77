# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.abspath("../"))
# sys.path.insert(0, os.path.abspath('.'))

_root = Path(__file__).parent.parent.absolute()


# -- Project information -----------------------------------------------------

project = "teslajsonpy"
copyright = "2021, Sergey Isachenko"
author = "Sergey Isachenko"

# The full version, including alpha/beta/rc tags
release = "0.12.2"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.graphviz",
    "autoapi.sphinx",
    "sphinx_rtd_theme",
    "sphinx.ext.napoleon",
    "m2r2",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
html_theme_options = dict(
    collapse_navigation=False,
    navigation_depth=False,
    style_external_links=True,
)
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# autoapi
master_doc = "index"
napoleon_include_special_with_doc = True
autoapi_type = "python"
autoapi_dirs = [str(_root / project)]
autoapi_keep_files = True
autoapi_python_class_content = "both"
autoapi_options = ["private-members=true"]
autoapi_modules = {"teslajsonpy": None}
graphviz_output_format = "svg"

today_fmt = "%Y-%m-%d"
source_suffix = [".rst", ".md"]


if __name__ == "__main__":
    print(f"{project} v{release}\n©{copyright}")
