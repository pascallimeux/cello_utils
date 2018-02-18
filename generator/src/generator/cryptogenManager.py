# -*- coding: utf8 -*-
'''
Created on 15 february 2018
@author: PYOL6775
'''

import json
from generator.utils.yaml_utils import dump_yaml_file
from generator.utils.cmd_utils import exec_cmd
from generator.models import Config
from generator.constants import CRYPTOGEN, CRYPTOCONFIG_FN, logger, root_path


def create_crypto_config_file(config, dir, cryptog_config_filename=CRYPTOCONFIG_FN):
        logger.info("Create crypto-config.yaml...")
        try:
            dic = {}
            orderer = {}
            ca = {}
            specs = []
            peers = []
            orderers = []
            orderer['Domain'] = config.orderer_org.domain
            orderer['Name']   = "orderer" #config.orderer_org.org_name
            ca['Country']     = config.cert.country
            ca['Province']    = config.cert.province
            ca['Locality']    = config.cert.locality
            for o in config.orderer_org.orderers:
                specs.append({'Hostname': o.name})
            orderer['Specs'] = specs
            orderer['CA']    = ca
            orderers.append(orderer)
            for peer_org in config.peer_orgs:
                peer = {}
                users = {}
                template = {}
                users['Count']    = peer_org.nb_users
                template['Count'] = peer_org.nb_peers
                peer['Domain']    = peer_org.domain 
                peer['Name']      = peer_org.org_name
                peer['CA']        = ca
                peer['Users']     = users
                peer['Template']  = template
                peers.append(peer)
            dic['OrdererOrgs'] = orderers
            dic['PeerOrgs']    = peers
            dump_yaml_file(data=dic, file_path=dir+"/"+cryptog_config_filename)
            logger.debug(json.dumps(dic, indent=4))
            return cryptog_config_filename
        except Exception as e:
            logger.error(e)
            raise Exception("Create crypto-config.yaml failled!")


def generate_MSP(path, cryptoconfig_filename):
    logger.info("Generate MSP...")
    cmd_cryptogen = "cd "+path+ " && "+root_path+CRYPTOGEN+" generate --config="+path+"/"+cryptoconfig_filename+" --output=crypto-config"
    exec_cmd(cmd_cryptogen)