#  ================================================================================================================# 
# # ===============================================================================================================# 
# # Copyright 2024 Infosys Ltd.                                                                                    # 
# # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # 
# # http://www.apache.org/licenses/                                                                                # 
#  ================================================================================================================# 

import os
import shutil
import subprocess

os.environ['NODE_ENV'] = 'production'

os.chdir('./app')

subprocess.run(['parcel', 'build', 'src/index.html', '--no-cache', '--no-source-maps'])

os.chdir('..')

if os.path.exists('./server/static'):
    shutil.rmtree('./server/static')

shutil.copytree('./app/dist', './server/static')