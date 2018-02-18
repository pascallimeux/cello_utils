# -*- coding: utf8 -*-
'''
Created on 16 february 2018
@author: PYOL6775
'''

from generator.generator import generate_archives
from generator.constants import logger

def generate_all_material(json_config):
    logger.info("Generate all material...")
    generate_archives(json_config)

def generate_crypto_material(json_config):
    logger.info("Generate crypto material...")
    generate_archives(json_config, "CRYPTO")

def generate_channel_artifacts(json_config):
    logger.info("Generate channel artificats...")
    generate_archives(json_config, "CHANNEL")

def generate_dockerfiles(json_config):
    logger.info("Generate docker files...")
    generate_archives(json_config, "DOCKER")

def generate4explorer(json_config):
    logger.info("Generate archive for explorer...")
    generate_archives(json_config, "EXPLORER")
    
def generate4composer(json_config):
    logger.info("Generate archive for composer...")
    generate_archives(json_config, "COMPOSER")