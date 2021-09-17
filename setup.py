import os

from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    author="Vin985",
    description=("Extra widgets for Qt and Python using PySide6"),
    keywords="qt, python, PySide6, widgets",
    # long_description=read('README.md'),
    name="pyqt_extra",
    version="0.1",
    packages=find_packages(),
    package_data={"": ["*.svg", "*.yaml", "*.zip", "*.ico", "*.bat"]},
)
