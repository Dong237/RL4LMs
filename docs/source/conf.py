# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import sphinx_rtd_theme
from typing import Dict, List
from unittest.mock import MagicMock

# We CANNOT enable 'sphinxcontrib.spelling' because ReadTheDocs.org does not support
# PyEnchant.
# try:
#     import sphinxcontrib.spelling  # noqa: F401

#     enable_spell_check = True
# except ImportError:
#     enable_spell_check = False

# # Try to enable copy button
# try:
#     import sphinx_copybutton  # noqa: F401

#     enable_copy_button = True
# except ImportError:
#     enable_copy_button = False

# source code directory, relative to this file, for sphinx-autobuild
sys.path.insert(0, os.path.abspath("../.."))


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'RL4LMs'
copyright = '2023, RL4LMs Team'
author = 'RL4LMs Team'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx_rtd_theme', 'sphinx.ext.todo', 'sphinx.ext.viewcode', 'sphinx.ext.autodoc', 'sphinx.ext.autosummary', 'sphinx.ext.autosectionlabel']
todo_include_todos = True

templates_path = ['_templates']
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']


# -- Extension configuration -------------------------------------------------

autodoc_member_order = 'bysource'

autodoc_default_options = {
    'members': None,  # Include all public members.
    'undoc-members': True,  # Include members that do not have docstrings.
    'show-inheritance': True,
    'special-members': '__call__, __init__',
}
