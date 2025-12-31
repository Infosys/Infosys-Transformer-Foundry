# ===============================================================================================================#
# Copyright 2024 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#


from setuptools import find_packages,setup

if __name__ == '__main__':
        setup(
            name='aicloudlibs',
            url=".\\aicloudlibs",
            packages=find_packages(),
            include_package_data=True,
            python_requires='>=3.6',
            version='0.1.0',
            description='aicloud library',
            install_requires=['fastapi==0.83.0',
             'pydantic==1.9.2',
             'databases',
             'motor==2.5.1',
            'pymongo<=4.1.1','kubernetes==10.0.0'],
            author='Infosys Limited',
            license='Apache License Version 2.0',
        )