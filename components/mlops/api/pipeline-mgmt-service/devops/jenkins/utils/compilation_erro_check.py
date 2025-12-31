# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

import py_compile
import sys
import traceback
import re
import string
from s3utilityservice import S3UtilityService 

# Function to check compilation error in the main script file
def compilation_error_output(main_script_file):
	try:
		py_compile.compile(main_script_file, doraise=True)
		op = "success"
		return op		
	except py_compile.PyCompileError as e:
		op = str(e)
		op = " ".join(line.strip() for line in op.splitlines())
		chars = re.escape(string.punctuation)
		op = re.sub('['+chars+']', '',op)
		return op

if __name__ == '__main__':
	localPath = sys.argv[1]
	print(compilation_error_output(localPath))