"""Packaging settings."""
from pathlib import Path

from setuptools import find_packages, setup

ROOT_PATH = Path(__file__).absolute().parent
README_PATH = ROOT_PATH / "README.md"

INSTALL_REQUIRES = [
    'importlib-metadata; python_version < "3.8"',
    'typing_extensions; python_version < "3.8"'
]


def local_scheme(version: str) -> str:  # pylint: disable=unused-argument
    """Skip the local version (eg. +xyz) to upload to Test PyPI"""
    return ""


setup(
    name='f-lib',
    description='A library of useful functions and classes for python projects.',
    long_description=README_PATH.read_text(),
    long_description_content_type="text/markdown",
    author='Kyle Finley',
    author_email='kyle@finley.sh',
    license='Apache License 2.0',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Utilities',
        'Typing :: Typed'
    ],
    python_requires='>=3.7',
    project_urls={
        'Documentation': 'https://f-lib.readthedocs.io/',
        'Source': 'https://github.com/ITProKyle/f-lib',
        'Tracker': 'https://github.com/ITProKyle/f-lib/issues',
    },
    keywords=['aws', 'devops', 'library'],
    packages=find_packages(exclude=('tests')),
    install_requires=INSTALL_REQUIRES,
    setup_requires=['setuptools_scm'],
    use_scm_version={"local_scheme": local_scheme},
    options={
        'bdist_wheel': {
            'python_tag': 'py3'
        }
    }
)
