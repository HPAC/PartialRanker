# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
sys.path.insert(0, os.path.abspath('../../partial_ranker'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Partial Ranker'
copyright = '2024, Aravind Sankaran'
author = 'Aravind Sankaran'
release = '0.2'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "sphinx.ext.duration",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "nbsphinx", #pip install nbsphinx
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

#html_theme = "default"


# pip install sphinx_rtd_theme
html_theme = "sphinx_rtd_theme"
html_theme_options = {
    'collapse_navigation': False,
    'sticky_navigation': False,
}

# pip install git+https://github.com/bashtage/sphinx-material.git
#html_theme = 'sphinx_material'

html_static_path = ['_static']
