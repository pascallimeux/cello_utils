# -*- coding: utf8 -*-
'''
Created on 15 february 2018
@author: PYOL6775
'''
import json
from generator.constants import EXPLORER_TAR, logger, LOCAL, EXPLORER_PATH,  EXPLORER_CONFIG_FN, EXPLORER_HOST, EXPLORER_MSQL_DB, EXPLORER_MSQL_HOST, EXPLORER_MSQL_LOGIN, EXPLORER_MSQL_PORT, EXPLORER_MSQL_PWD, EXPLORER_LOCAL, EXPLORER_PORT
from generator.utils.cmd_utils import exec_cmd
from generator.utils.tar_utils import build_tarfile

def create_config_file(config, filename):
    logger.info("Create explorer config file...")
    try:
        dic = {}
        dic ['host']=EXPLORER_HOST
        dic ['port']=EXPLORER_PORT
        dic ['channel']=config.channel.name
        dic ['keyValueStore']=EXPLORER_LOCAL+"fabric-client-kvs"
        dic ['eventWaitTime']="30000"
        mysql ={}
        mysql['host']=EXPLORER_MSQL_HOST 
        mysql['port']=EXPLORER_MSQL_PORT
        mysql['database']=EXPLORER_MSQL_DB
        mysql['username']=EXPLORER_MSQL_LOGIN
        mysql['password']=EXPLORER_MSQL_PWD
        dic['mysql'] = mysql
        for o in config.peer_orgs:
            org = {}
            org['name']= "peer"+o.org_name
            org['mspid']= o.mspid
            org['ca']= o.ca.url
            for p in o.peers:
                peer = {}
                peer['request'] = p.request_url
                peer['events'] = p.event_url
                peer['server-hostname'] = p.hostname
                peer['tls_cacerts'] = EXPLORER_LOCAL+o.domain+"/peer/"+p.name+"/ca.crt"
                org[p.name]=peer
            admin = {}
            admin['key']=EXPLORER_LOCAL+o.domain+"/admin/keystore"
            admin['cert']=EXPLORER_LOCAL+o.domain+"/admin/signcerts"
            org['admin']=admin
            dic[o.org_name]=org
        with open(filename, 'w') as f:
            json.dump(dic, f, ensure_ascii=False, indent=4)
        logger.debug(json.dumps(dic, indent=4))
    except Exception as e:
        logger.error(e)
        raise Exception("Create explorer config file failled!")

def generate_archive4explorer(config, channel_dir):
    dir = channel_dir + EXPLORER_PATH
    local = channel_dir + LOCAL
    config_file_path = dir + "/config"
    exec_cmd("mkdir -p {}".format(config_file_path))
    create_config_file(config, config_file_path+"/"+EXPLORER_CONFIG_FN)
    for org in config.peer_orgs:
        exec_cmd("mkdir -p {}".format(dir + "/" + org.org_name + "/admin/keystore"))
        exec_cmd("mkdir -p {}".format(dir + "/" + org.org_name + "/admin/signcerts"))
        admin_local_path = local+"/crypto-config/peerOrganizations/"+org.domain+"/users/Admin@"+org.domain+"/msp/"
        exec_cmd("cp {0} {1}".format(admin_local_path+"/keystore/*", dir + "/" + org.org_name + "/admin/keystore/"))
        exec_cmd("cp {0} {1}".format(admin_local_path+"/signcerts/*", dir + "/" + org.org_name + "/admin/signcerts/"))
        for peer in org.peers:
            exec_cmd("mkdir -p {}".format(dir + "/" + org.org_name + "/peer/"+ peer.name))
            peer_ca_crt = local+"/crypto-config/peerOrganizations/"+org.domain+"/peers/"+peer.name+"."+org.domain+"/tls/ca.crt"
            exec_cmd("cp {0} {1}".format(peer_ca_crt, dir + "/" + org.org_name + "/peer/"+ peer.name+"/ca.crt"))
    build_tarfile(dir, channel_dir+"/"+EXPLORER_TAR)
  
