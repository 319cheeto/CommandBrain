#!/usr/bin/env python3
"""
Setup script for CommandBrain
Install with:  pip install .
Then use:      cb ssh
"""

from setuptools import setup
import os

def read_readme():
    path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    return "CommandBrain - Smart Linux Command Reference Tool"

setup(
    name="commandbrain",
    version="2.0.0",
    description="Smart Linux command reference tool with offline search",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Joshua Sears",
    python_requires=">=3.6",
    py_modules=["commandbrain", "data"],
    entry_points={
        'console_scripts': [
            'cb=commandbrain:main',
            'commandbrain=commandbrain:main',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    keywords="linux commands reference cli tool terminal cybersecurity education",
    project_urls={
        "Source": "https://github.com/319cheeto/CommandBrain",
    },
)
