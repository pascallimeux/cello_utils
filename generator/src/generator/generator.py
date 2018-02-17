# -*- coding: utf8 -*-
'''
Created on 17 february 2018
@author: PYOL6775
'''
import json
from models import json2config, Config
from constants import logger, root_path, GENERATED, LOCAL, COMPOSER_PATH, EXPLORER_PATH
from cryptogenManager import create_crypto_config_file, generate_MSP
from configtxManager import generate_genesis_block, generate_configTX, create_configtx_file
from cmd_utils import exec_cmd
from generator4composer import create_connection_file, generate_archive4composer
from generator4explorer import create_config_file, generate_archive4explorer


def generate_archives(json_config, archive="ALL"):
    config          = json2config(json_config)
    channel_dir     = __init_folders(config.channel.name)
    local_folder    = channel_dir + LOCAL
    __generate_crypto_material(local_folder, config)
    if archive == 'CRYPTO':
        return 
    __generate_channel_artifacts(local_folder, config)
    if archive == 'CHANNEL':
        return
    __generate_dockerfiles()
    if archive == 'DOCKER':
        return
    if archive == 'COMPOSER':
        __generate4composer(channel_dir, config)
        return 
    if archive == 'EXPLORER':
        __generate4explorer(channel_dir, config)
    else:
        __generate4composer(channel_dir, config)
        __generate4explorer(channel_dir, config)

def __init_folders(channel):
    logger.info("Initialize archives folders...")
    channel_dir = root_path+GENERATED+"/"+channel+"/"
    exec_cmd("rm -Rf {}".format(channel_dir))
    exec_cmd("mkdir -p {}".format(channel_dir + LOCAL))
    return channel_dir

def __generate_crypto_material(local_folder, config):
    config_filename = create_crypto_config_file(config, local_folder)
    generate_MSP(local_folder, config_filename)

def __generate_channel_artifacts(local_folder, config):
    create_configtx_file(config, local_folder)
    generate_genesis_block(local_folder)
    generate_configTX(local_folder, config.channel.name)

def __generate_dockerfiles(): #TODO
    pass

def __generate4explorer(channel_dir, config):
    exec_cmd("mkdir -p {}".format(channel_dir + EXPLORER_PATH))
    generate_archive4explorer(config, channel_dir)
    
def __generate4composer(channel_dir, config):
    exec_cmd("mkdir -p {}".format(channel_dir + COMPOSER_PATH))
    generate_archive4composer(config, channel_dir)
