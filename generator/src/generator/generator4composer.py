# -*- coding: utf8 -*-
'''
Created on 15 february 2018
@author: PYOL6775
'''
import json
from constants import logger, COMPOSER_CONFIG_FN, COMPOSER_LOCAL, LOCAL, COMPOSER_PATH
from models import Config
from cmd_utils import exec_cmd

def create_connection_file(config, filename):
    for peer_org in config.peer_orgs:
        logger.info("Create composer config file...")
        try:
            dic ={}
            dic['name']    = 'profil'+peer_org.org_name
            dic['type']    = 'hlfv1'
            dic['mspID']   = peer_org.mspid
            dic['channel'] = config.channel.name            
            dic['timeout'] = 300      
            peers=[]
            for p in peer_org.peers:
                peer = {}
                peer['requestURL']=p.request_url 
                peer['eventURL']=p.event_url 
                peer['cert']=COMPOSER_LOCAL+peer_org.domain+"/peer/"+p.name+"/ca.crt"
                peer['hostnameOverride']=p.hostname          
                peers.append(peer)
            orderers=[]  
            dic['peers']=peers              
            for o in config.orderer_org.orderers:
                orderer = {}
                orderer['url']=o.url 
                orderer['cert']=COMPOSER_LOCAL+config.orderer_org.domain+"/orderer/"+o.name+"/ca.crt"
                orderer['hostnameOverride']=o.hostname     
                orderers.append(orderer)
            dic['orderers']=orderers   
            ca = {}
            ca['url']=peer_org.ca.url 
            ca['name']="ca-"+peer_org.org_name 
            ca['cert']=COMPOSER_LOCAL+peer_org.domain+"/ca/ca.crt"
            ca['hostnameOverride']="ca."+peer_org.domain          
            dic['ca']=ca   
            with open(filename, 'w') as f:
                json.dump(dic, f, ensure_ascii=False, indent=4)
            logger.debug(json.dumps(dic, indent=4))
        except Exception as e:
            logger.error(e)
            raise Exception("Create composer config file failled!")


def generate_archive4composer(config, channel_dir):
    dir = channel_dir + COMPOSER_PATH
    local = channel_dir + LOCAL
    for org in config.peer_orgs:
        config_file_path = dir + "/" + org.org_name + "/connection"
        exec_cmd("mkdir -p {}".format(config_file_path))
        create_connection_file(config, config_file_path+"/"+COMPOSER_CONFIG_FN)
        exec_cmd("mkdir -p {}".format(dir + "/" + org.org_name + "/orderer"))
        orderer_ca_crt = local+"/crypto-config/ordererOrganizations/"+config.orderer_org.domain+"/orderers/"+config.orderer_org.orderers[0].hostname+"/tls/ca.crt"
        exec_cmd("cp {0} {1}".format(orderer_ca_crt, dir + "/" + org.org_name + "/orderer"))
        for peer in org.peers:
            exec_cmd("mkdir -p {}".format(dir + "/" + org.org_name + "/peer/"+ peer.name))
            peer_ca_crt = local+"/crypto-config/peerOrganizations/"+org.domain+"/peers/"+peer.name+"."+org.domain+"/tls/ca.crt"
            exec_cmd("cp {0} {1}".format(peer_ca_crt, dir + "/" + org.org_name + "/peer/"+ peer.name+"/ca.crt"))
    