# -*- coding: utf8 -*-
'''
Created on 18 february 2018
@author: PYOL6775
'''

import tarfile
import os

def build_tarfile(src_path, dst_path):
    with tarfile.open(dst_path, "w:gz") as tar:
        tar.add(src_path, arcname=os.path.basename(src_path))