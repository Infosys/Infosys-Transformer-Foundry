# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

from setuptools import find_packages,setup
from pathlib import Path
from typing import List

def get_install_requires() -> List[str]:
    """Returns requirements.txt parsed to a list"""
    fname = Path(__file__).parent / 'requirement/requirement.txt'
    targets = []
    if fname.exists():
        with open(fname, 'r') as f:
            targets = f.read().splitlines()
    return targets

if __name__ == '__main__':
        setup(
            name='project_mgmt_service',
            url="project_mgmt_service",
            packages=find_packages(),
            include_package_data=True,
            python_requires='>=3.6',
            version='0.1.0',
            description='Project Management Services',
            install_requires=get_install_requires(),
            author='Infosys Limited',
            license='Apache License Version 2.0',
        )