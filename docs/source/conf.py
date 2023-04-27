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


# We CANNOT enable 'sphinxcontrib.spelling' because ReadTheDocs.org does not support PyEnchant.
try:
    import sphinxcontrib.spelling  # noqa: F401

    enable_spell_check = True
except ImportError:
    enable_spell_check = False

# Try to enable copy button
try:
    import sphinx_copybutton  # noqa: F401

    enable_copy_button = True
except ImportError:
    enable_copy_button = False

# source code directory, relative to this file, for sphinx-autobuild
sys.path.insert(0, os.path.abspath("../.."))

# specify the master_doc 
master_doc = 'index'
source_suffix = '.rst'


class Mock(MagicMock):
    __subclasses__ = []  # type: ignore

    @classmethod
    def __getattr__(cls, name):
        return MagicMock()

# Mock modules that requires C modules
# Note: because of that we cannot test examples using CI
# 'torch', 'torch.nn', 'torch.nn.functional',
# DO not mock modules for now, we will need to do that for read the docs later
MOCK_MODULES: List[str] = ['torch', 'torch.nn']
sys.modules.update((mod_name, Mock()) for mod_name in MOCK_MODULES)


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'RL4LMs'
copyright = '2023, RL4LMs Team'
author = 'RL4LMs Team'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx_rtd_theme', 
              'sphinx.ext.todo', 
              'sphinx.ext.viewcode', 
              'sphinx.ext.autodoc',
              'sphinx.ext.napoleon',
              'sphinx.ext.autosummary', 
              'sphinx.ext.autosectionlabel'
             ]

todo_include_todos = True

if enable_spell_check:
    extensions.append("sphinxcontrib.spelling")

if enable_copy_button:
    extensions.append("sphinx_copybutton")

templates_path = ['_templates']
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# Fix for read the docs
on_rtd = os.environ.get("READTHEDOCS") == "True"
if on_rtd:
    html_theme = "default"
else:
    html_theme = "sphinx_rtd_theme"

html_static_path = ['_static']
html_logo = "_static/img/RL4LMs_logo.png"

# -- Extension configuration -------------------------------------------------

autodoc_member_order = 'bysource'

autodoc_default_options = {
    'members': None,  # Include all public members.
    'undoc-members': True,  # Include members that do not have docstrings.
    'show-inheritance': True,
    'special-members': '__call__, __init__',
}
