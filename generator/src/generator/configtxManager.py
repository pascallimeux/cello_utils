# -*- coding: utf8 -*-
'''
Created on 15 february 2018
@author: PYOL6775
'''

import json
from constants import logger
from cmd_utils import exec_cmd
from yaml_utils import dump_yaml_file
from models import Config
from constants import CONFIGTXGEN, CNFIGTX_FN, GENESISBLOCKNAME, logger, root_path, CHANNEL_NAME


def __create_orderer_org(config):
    organizations = [] 
    orderer = {}
    orderer['ID'] = config.orderer_org.mspid
    orderer['MSPDir'] = config.orderer_org.mspdir
    orderer['Name'] = config.orderer_org.org_name+"Org"
    organizations.append(orderer)
    return organizations

def __create_peers_org(config):
    organizations = [] 
    for peer_org in config.peer_orgs:
        peer = {}
        peer['ID']     = peer_org.mspid
        peer['MSPDir'] = peer_org.mspdir            
        peer['Name']   = peer_org.mspid
        anchorPeers = []
        anchorPeer = {}
        anchorPeer['Host'] = peer_org.peers[0].hostname
        anchorPeer['Port'] = peer_org.peers[0].request_port
        anchorPeers.append(anchorPeer)
        peer['AnchorPeers'] = anchorPeers
        organizations.append(peer)
    return organizations

def __create_orderer(config):
    orderer={}
    orderer['OrdererType']  = 'solo'
    orderer['BatchTimeout'] = '2s'
    addresses=[]
    for o in config.orderer_org.orderers:
        addresses.append(o.hostname)
    orderer['Addresses'] = addresses
    batchSize = {}
    batchSize['AbsoluteMaxBytes']  = "99 MB"
    batchSize['MaxMessageCount']   = 10
    batchSize['PreferredMaxBytes'] = "512 KB"
    orderer['BatchSize'] = batchSize
    brokers=[]
    brokers.append("127.0.0.1:9092")
    kafka = {}
    kafka['Brokers'] = brokers
    orderer['Kafka'] = kafka
    orderer['Organizations']=''
    return orderer

def __create_application(config):
    application = {}
    application['Organizations']=''
    return application


def create_configtx_file(config, dir, configtx_filename=CNFIGTX_FN):
    logger.info("Create configtx.yaml...")
    try:  
        orderer_default     = __create_orderer(config)
        orderer_org         = __create_orderer_org(config)
        peers_org           = __create_peers_org(config)
        application_default = __create_application(config)
        orderer_default['Organizations']     = orderer_org
        application_default['Organizations'] = peers_org

        orderer_profil = {}
        sample_consortium = {}
        consortiums = {}
        channel_profil = {}
        profiles = {}
        dic = {}
        orderer_profil['Orderer']          = orderer_default
        sample_consortium['Organizations'] = peers_org
        consortiums['SampleConsortium']    = sample_consortium
        orderer_profil['Consortiums']      = consortiums
        channel_profil['Consortium']       = "SampleConsortium"
        channel_profil['Application']      = application_default
        profiles ['OrgsChannel']           = channel_profil
        profiles ['OrgsOrdererGenesis']    = orderer_profil
        dic ['Profiles']                   = profiles
        dump_yaml_file(data=dic, file_path=dir+"/"+configtx_filename)
        logger.debug(json.dumps(dic, indent=4))
    except Exception as e:
        logger.error(e)
        raise Exception("Create crypto-config.yaml failled!")

def generate_genesis_block(path):
    logger.info("Generate genesis block...")
    cmd_genesis_block ="cd "+path+ " && "+root_path+CONFIGTXGEN+" -profile OrgsOrdererGenesis -outputBlock "+GENESISBLOCKNAME
    exec_cmd(cmd_genesis_block)

def generate_configTX(path, channel_name=CHANNEL_NAME):
    logger.info("Generate configTX file...")
    channeltx_filename = channel_name+".tx"
    cmd_channeltx = "cd "+path+ " && "+root_path+CONFIGTXGEN+" -profile OrgsChannel -outputCreateChannelTx "+channeltx_filename+" -channelID "+channel_name
    exec_cmd(cmd_channeltx)
