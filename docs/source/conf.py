"""Configuration file for the Sphinx documentation builder.

https://www.sphinx-doc.org/en/master/usage/configuration.html

"""

import os
from datetime import date
from pathlib import Path

from pkg_resources import get_distribution

ROOT_DIR = Path(__file__).parent.parent.parent
DOC_SRC = ROOT_DIR / "docs" / "source"

# -- Project information -----------------------------------------------------
project = "f-lib"
copyright = f"{date.today().year}, Kyle Finley"  # noqa: A001, DTZ011
author = "Kyle Finley"
version = get_distribution(project).version
release = ".".join(version.split(".")[:2])  # short X.Y version


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
add_function_parentheses = True
add_module_names = True
default_role = None
exclude_patterns = []
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinxcontrib.apidoc",
    "sphinxcontrib.jquery",
]
highlight_language = "default"
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),  # link to python docs
}
language = "en"
master_doc = "index"
needs_extensions = {}
nitpicky = True
primary_domain = "py"
pygments_style = "one-dark"  # syntax highlighting style
pygments_dark_style = "one-dark"  # syntax highlighting style
source_suffix = {".rst": "restructuredtext"}
templates_path = ["_templates"]  # template dir relative to this dir


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_codeblock_linenos_style = "inline"
html_css_files = [  # files relative to html_static_path
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/fontawesome.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/solid.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/brands.min.css",
]
html_short_title = f"{project} v{release}"
html_show_copyright = True
html_show_sphinx = False
html_static_path = ["_static"]  # dir with static files relative to this dir
html_theme = "furo"  # theme to use for HTML and HTML Help pages
html_theme_options = {
    "dark_css_variables": {
        "font-stack--monospace": "Inconsolata, monospace",
    },
    "light_css_variables": {
        "font-stack--monospace": "Inconsolata, monospace",
    },
}
html_title = f"{project} v{version}"


# -- Options for sphinx-apidoc -----------------------------------------------
# https://www.sphinx-doc.org/en/master/man/sphinx-apidoc.html#environment
os.environ["SPHINX_APIDOC_OPTIONS"] = "members"


# -- Options of sphinx.ext.autodoc -------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#configuration
autoclass_content = "class"
autodoc_class_signature = "separated"
autodoc_default_options = {
    "exclude-members": ", ".join(["model_config", "model_fields"]),  # noqa: FLY002
    "member-order": "bysource",
    "members": True,
    "show-inheritance": True,
}
autodoc_preserve_defaults = True
autodoc_type_aliases = {}
autodoc_typehints = "signature"


# -- Options for sphinx.ext.napoleon  ----------------------------------------
# https://www.sphinx-doc.org/en/3.x/usage/extensions/napoleon.html#configuration
napoleon_attr_annotations = True
napoleon_google_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_type_aliases = autodoc_type_aliases
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = False
napoleon_use_rtype = True


# -- Options for sphinx.ext.todo ---------------------------------------------
# https://www.sphinx-doc.org/page/usage/extensions/todo.html
todo_include_todos = True


# -- Options for sphinxcontrib.apidoc  ----------------------------------------
apidoc_excluded_paths = []
apidoc_extra_args = [f"--templatedir={DOC_SRC / '_templates' / 'apidocs'}"]
apidoc_module_dir = str(ROOT_DIR / "f_lib")
apidoc_module_first = True
apidoc_output_dir = "apidocs"
apidoc_separate_modules = True
apidoc_toc_file = "index"


# -- Options for sphinx_copybutton ---------------------------------
# https://sphinx-copybutton.readthedocs.io/en/latest/index.html
copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True
copybutton_remove_prompts = True
copybutton_line_continuation_character = "\\"
