# -*- coding: utf8 -*-
'''
Created on 15 february 2018
@author: PYOL6775
'''

import os
import yaml

def load_yaml_file(filename) :
    with open(filename, 'r') as stream:
        try:
            data = yaml.load(stream)
            return data
        except yaml.YAMLError:
            return None


def dump_yaml_file(data, file_path=None):
    if file_path == None:
        print(yaml.dump(data=data, default_flow_style=False, indent=2))
    else:
        with open(file_path, 'w') as yaml_file:
            try:
                yaml.dump(data=data, stream=yaml_file, default_flow_style=False, indent=2)
            except yaml.YAMLError:
                return None
