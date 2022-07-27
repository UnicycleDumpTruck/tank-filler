"""Sphinx configuration."""
project = "Tank Filler"
author = "Jeff Highsmith"
copyright = "2022, Jeff Highsmith"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
