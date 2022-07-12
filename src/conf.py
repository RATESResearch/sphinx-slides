# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------
# serve to show the default.

import sys
import requests
import toml
from os import makedirs, environ
from os.path import exists, abspath, join
from dotenv import load_dotenv

def download_files():
    """ Dowload the files listed in the config
    """
    global config
    load_dotenv()
    config = toml.load('spyce.toml')
    makedirs('downloads', exist_ok = True) 
    for filename, url in config['SPHINX']['downloads'].items():
        print(filename, url)
        with open(join("downloads", filename), 'wb') as fout:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            # Write response data to file
            for block in response.iter_content(4096):
                fout.write(block)

def load_settings():
    """ Load the config. The default config is in the spyce.toml file.
    
    Priority:

    1. Environment Variables
    #. .env file
    #. spyce.toml file
    """
    global config
    load_dotenv()
    config = toml.load('spyce.toml')
    for key, value in config['SPHINX']['settings'].items():
        print(key, value)
        if key in environ:
            config['SPHINX']['settings'][key] = environ[key]
        print(key, config['SPHINX']['settings'][key])

def download_file(filename, url):
    """
    Download an URL to a file
    """
    with open(filename, 'wb') as fout:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        # Write response data to file
        for block in response.iter_content(4096):
            fout.write(block)

def download_if_not_exists(filename, url):
    """
    Download a URL to a file if the file
    does not exist already.

    Returns
    -------
    True if the file was downloaded,
    False if it already existed
    """
    if not exists(filename):
        download_file(filename, url)
        return True
    return False

download_files()

#on_rtd = environ.get('READTHEDOCS', None) == 'True'
on_rtd = True

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
sys.path.insert(0, abspath('..'))

# -- Project information -----------------------------------------------------
load_settings()

project = config['SPHINX']['settings']['PROJECT_NAME']
copyright = config['SPHINX']['settings']['COPYRIGHT_YEAR'] \
    + ', ' \
    + config['SPHINX']['settings']['ORGANIZATION']
author = config['SPHINX']['settings']['AUTHOR']
# The full version, including alpha/beta/rc tags
release = config['SPHINX']['settings']['VERSION']

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
'sphinxcontrib.bibtex',
'sphinx.ext.autodoc',
'hieroglyph',
'sphinx.ext.todo',
'sphinxcontrib.plantuml',
'sphinx.ext.intersphinx',
"sphinx_revealjs",
]

# master_doc = 'slides'

intersphinx_mapping = {'rgvflood': ('https://glossary.rgvflood.com/en/latest', None)}

bibtex_bibfiles = ['downloads/references.bib']
# plantuml = 'java -jar /usr/share/plantuml/plantuml.jar'
plantuml = "plantuml"

# Add any paths that contain templates here, relative to this directory.
templates_path = ['downloads']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []
# Display todos by setting to True
todo_include_todos = True

numfig = True
#numfig_format['figure'] = 'Figure %s'
numfig_format = {'figure': 'Figure: %s', 'table': 'Table: %s', 'code-block': 'Listing: %s', 'section': 'Section: %s'}

# -- Options for HTML Slide output ---------------------------------------------------

slide_theme = 'slides2'
#slide_theme_path = ['_static']
#slide_theme_options = {
#    'presenters': [
#        {
#            'name': 'Andrew N.S. Ernest, Ph.D., P.E., BCEE, D.WRE',
#            # 'twitter': '@author',
#            # 'www': 'http://example.com/author',
#            # 'github': 'http://github.com/author/example'
#        },
#    ],
#}
#slide_theme_options = {'custom_css':'custom.css'}

# slide_link_html_to_slides = not on_rtd
# slide_link_html_sections_to_slides = not on_rtd
# slide_relative_path = "./slides/"
#
# slide_link_to_html = True
# slide_html_relative_path = "../"

# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
if on_rtd:
    import sphinx_rtd_theme

    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

else:
    html_theme = 'alabaster'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
#html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = config['SPHINX']['settings']['PROJECT_TITLE']

# A shorter title for the navigation bar.  Default is the same as html_title.
html_short_title = project

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = "downloads/RGVFloodLogo.png"
html_baseurl = "https://docs.rgvflood.com"

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['downloads']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_domain_indices = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
#html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
#html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
#html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None

# Output file base name for HTML help builder.
htmlhelp_basename = project

pdf_documents = [('index', u'rst2pdf', u'Sample rst2pdf doc', u'Your Name'),]
# index - master document
# rst2pdf - name of the generated pdf
# Sample rst2pdf doc - title of the pdf
# Your Name - author name in the pdf

# -- Options for LaTeX output
# --------------------------------------------------

latex_elements = {
# The paper size ('letterpaper' or 'a4paper').
#'papersize': 'letterpaper',

# The font size ('10pt', '11pt' or '12pt').
'pointsize': '12pt',

# Additional stuff for the LaTeX preamble.
'preamble': '\\usepackage{svg}',

'releasename': html_title+'\par Project Deliverable ID',
'extraclassoptions': 'openany,oneside',
'babel': '\\usepackage[american]{babel}',
'maketitle': r''' 
\sphinxmaketitle

    %\renewcommand{\familydefault}{\sfdefault}
    \newcommand\signature[3]{% Role; Name; Department
    %\begin{center}
    {\sffamily
    \vspace{1cm}\par
    \textbf{#1}:\par
        \begin{minipage}{10cm}
        \centering
        \vspace{3cm}\par
        \rule{10cm}{1pt}\par
        \textbf{#2}\par
        #3%
        \end{minipage}
    }
    %\end{center}
    }
    \newcommand\insertdate[1][\today]{\vfill\begin{flushright}#1\end{flushright}}

    {\LARGE\sffamily \textbf{Approval Page}}
    
    \signature{Technical Review By}{William Kirkey, Ph.D.}{Chief of Research and Technology Development}
    
    \signature{Final Approval For Submission}{Andrew N.S. Ernest, Ph.D., P.E., BCEE, D.WRE}{Chief Executive Officer}
        
    \insertdate

''',
}

authors = author + ' ' + config['SPHINX']['settings']['OTHER_AUTHORS']
# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
  ('index', project+'.tex', 'Lower Rio Grande Valley Development Council Flood Infrastructure Fund',
   authors, 
   'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.

# latex_logo = https://raw.githubusercontent.com/RATESResearch/RGVFlood/main/assets/RATESLogo.png
latex_logo = 'downloads/RATESLogo.png'

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# If true, show page references after internal links.
#latex_show_pagerefs = False

# If true, show URL addresses after external links.
#latex_show_urls = False

# Documents to append as an appendix to all manuals.
# latex_appendices = ['downloads/glossary', 'downloads/bibliography']

# If false, no module index is generated.
#latex_domain_indices = True

# if __name__ == "__main__":

#     load_config()
