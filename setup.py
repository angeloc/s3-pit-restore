#!/usr/bin/env python3
#
# MIT License
#
# s3-pit-restore, a point in time restore tool for Amazon S3
#
# Copyright (c) [2016] [Madisoft S.p.A.]
#
# Author: Matteo Moretti <matteo.moretti@madisoft.it>
# Author: Angelo Compagnucci <angelo.compagnucci@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from distutils.core import setup

setup(name='s3-pit-restore',
      version='0.5',
      description='s3-pit-restore, a point in time restore tool for Amazon S3',
      author='Angelo Compagnucci, Matteo Moretti',
      author_email='angelo.compagnucci@gmail.com, matteo.moretti@gmail.com',
      url='https://github.com/madisoft/s3-pit-restore/',
      keywords = ['amazon', 's3', 'restore', 'point', 'time', 'timestamp'],
      scripts=['s3-pit-restore'],
      install_requires=['boto3'],
     )
