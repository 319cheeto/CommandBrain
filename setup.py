#!/usr/bin/env python3
"""
Setup script for CommandBrain
Makes installation easier with pip install
"""

from setuptools import setup, find_packages
import os

# Read the README for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "CommandBrain - Smart Linux Command Reference Tool"

setup(
    name="commandbrain",
    version="1.0.0",
    description="Smart Linux command reference tool with offline search",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="CommandBrain Development",
    python_requires=">=3.6",
    py_modules=[
        "commandbrain",
        "setup_commandbrain",
        "import_commands",
        "add_kali_tools"
    ],
    entry_points={
        'console_scripts': [
            'commandbrain=commandbrain:main',
            'cb=commandbrain:main',  # Ultra-short alias!
            'commandbrain-setup=setup_commandbrain:main',
            'commandbrain-import=import_commands:main',
            'commandbrain-kali=add_kali_tools:add_kali_tools',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    keywords="linux commands reference cli tool terminal",
    project_urls={
        "Source": "https://github.com/yourusername/commandbrain",
    },
)
