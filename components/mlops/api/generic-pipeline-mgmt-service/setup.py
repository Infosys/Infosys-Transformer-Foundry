# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

import setuptools
from distutils.core import setup
from setuptools import find_packages

setup(
    name="generic_pipeline_service",
    version="5.7.1",
    author='Infosys Limited',
    license='Apache License Version 2.0',
    author_email="",
    description="The app for generic pipeline management",
    long_description="",
    long_description_content_type="text/markdown",
    url="",
    package_dir={},
    packages=find_packages(where='src'),
    install_requires=[],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: Apache License Version 2.0",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
