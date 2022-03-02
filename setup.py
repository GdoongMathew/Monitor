import os
import sys
import shutil

from setuptools import find_packages, setup, Command

NAME = "monitor"
DESCRIPTION = "Monitor which reads hardware information."
URL = "https://github.com/GdoongMathew/Monitor"
REQUIRES_PYTHON = ">=3.6.0"
VERSION = "0.0.1"

try:
    with open('requirements.txt', encoding='utf-8') as f:
        REQUIRED = f.read().split('\n')

except:
    REQUIRED = []

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(),
    install_requires=REQUIRED
)
