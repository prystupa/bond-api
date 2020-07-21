"""Setup script for bond-api."""

import pathlib

from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="bond_api",
    version="0.1.2",
    packages=find_packages(),

    author="Eugene Prystupa",
    author_email="eugene.prystupa@gmail.com",
    description="Asynchronous Python wrapper library over Bond Local API",
    long_description=README,
    long_description_content_type="text/markdown",
    keywords="bond local api async",

    install_requires=[
        "aiohttp>=3.6.1"
    ],

    url="https://github.com/prystupa/bond-api",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Topic :: Home Automation"
    ]
)
