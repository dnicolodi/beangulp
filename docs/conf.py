project = 'beangulp'
copyright = '2021, Beancount Contributors'
author = 'Beancount Contributors'

release = '0.1'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.extlinks',
    'sphinx.ext.githubpages',
    'sphinx_rtd_theme',
]

nitpicky = True
source_suffix = '.rst'
master_doc = 'index'

templates_path = ['_templates']

exclude_patterns = ['_build']

html_theme = 'sphinx_rtd_theme'
html_show_copyright = False
html_title = project

html_theme_options = {
    'display_version': True,
}

html_static_path = ['_static']
html_css_files = ['extra.css']

extlinks = {
    'issue': ('https://github.com/beancount/beangulp/issues/%s', '#'),
    'pull': ('https://github.com/beancount/beangulp/pull/%s', '#'),
}

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None)
}

napoleon_google_docstring = True
napoleon_use_param = False

# The type hints are rather ugly in some cases. There may be a way to
# make them nicer, for the time being simply do not show them.
autodoc_typehints = 'none'
autodoc_member_order = 'bysource'
