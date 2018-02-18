# -*- coding: utf8 -*-
'''
Created on 15 february 2018
@author: PYOL6775
'''

import os
from subprocess import Popen, PIPE

def exec_cmd(cmds):
    process = Popen(cmds, shell=True, stdout=PIPE, stderr=PIPE)
    output, error = process.communicate()
    output = output.decode('utf-8')
    error = error.decode('utf-8')
    code = process.returncode
    if code != 0:
        raise Exception ("Command: "+cmds+" failled! "+error)
    return output

