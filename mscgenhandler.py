#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
    mscgenhandler
    ~~~~~~~~~~~~~~~~~~~~
    handling mscgen to generate msc in image format

    See the README file for details.
    :author: Jonathan <m10802821@gapps.ntust.edu.tw>.
    :license: MIT, see LICENSE for details.
"""

import sys
from subprocess import Popen, PIPE
from shutil import which

def mscgenhandler(format, textinput, imageoutput):

    # check if mscgen avail
    if which('mscgen') == None:
        return -1

    # calling mscgen
    pipe = Popen("mscgen -T "+ format + " -i " + textinput + " -o " + imageoutput, stdout=PIPE)
    ret = pipe.communicate()
    ret = str(ret[0],'utf-8')

    if ret == '':
        return 0
    else:
        return -1