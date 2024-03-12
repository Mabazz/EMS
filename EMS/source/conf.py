# Configuration file for the Sphinx documentation builder.

import os
import sys

# Set the absolute path to your project root directory
project_root = r'C:\\Users\\marti\\Documents\\EMS'

# Add the project root to the Python path
sys.path.insert(0, project_root)

# Add the 'ems_prog' and 'ems_server' subdirectories to the Python path
sys.path.insert(0, os.path.join(project_root, 'ems_prog'))

# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'EMS'
copyright = '2024, Mabazz'
author = 'Mabazz'
release = '2024'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon']
napoleon_google_docstring = True

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# Choose_theme
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Customize theme

# Autodoc settings
autodoc_default_flags = ['members', 'undoc-members', 'show-inheritance']
autodoc_member_order = 'bysource'