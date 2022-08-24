# -*- coding: utf-8 -*-
import sys
import os
import sphinx_bootstrap_theme

ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(1, ROOT)
sys.path.insert(1, os.path.join(ROOT, "..", "src"))

# -- General configuration ------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["sphinx.ext.autodoc", "htmlhidden"]
autoclass_content = "both"

# The suffix of source filenames.
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# General information about the project.
project = "Python interface to chemfiles"
copyright = "2015-2017, Guillaume Fraux — BSD license"


def version():
    import chemfiles

    full_version = chemfiles.__version__.split("-")
    release = full_version[0]
    version = ".".join(release.split(".")[0:2])
    if len(full_version) > 1:
        # Developement release
        release += "-dev"
        version += "-dev"
    return (version, release)


version, release = version()

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "bootstrap"
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()

# Add any paths that contain templates here, relative to this directory.
templates_path = [os.path.join(ROOT, "templates")]

html_theme_options = {
    "navbar_site_name": "Navigation",
    "navbar_pagenav": False,
    "source_link_position": None,
    "bootswatch_theme": "flatly",
    "bootstrap_version": "3",
}

html_sidebars = {"**": ["sidebar-toc.html", "searchbox.html"]}

# Output file base name for HTML help builder.
htmlhelp_basename = "chemfiles.py"
