# Configuration file for the Sphinx documentation builder.
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'PyQtMainWindow Project Template'
copyright = '2024'
author = 'Bico'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinxcontrib.plantuml',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'PySide6': ('https://doc.qt.io/qtforpython-6/', None),
}

# PlantUML configuration
plantuml = 'java -jar {}'.format(os.path.join(os.path.dirname(__file__), 'plantuml/plantuml.jar'))
plantuml_output_format = 'svg' 