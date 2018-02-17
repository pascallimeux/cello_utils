# -*- coding: utf8 -*-
'''
Created on 15 february 2018
@author: PYOL6775
'''

import os
import logging
import logging.config

# Logger and path
my_path   = os.path.dirname(os.path.abspath(__file__))+"/"
root_path = os.path.abspath(os.path.join(os.path.abspath(os.path.join(my_path, os.pardir)), os.pardir))+"/"
logging.config.fileConfig(my_path+'logging.conf')
logger    = logging.getLogger('generator')


# Default ports for hyperledger
DEFAULT_CA_PORT           = 7054
DEFAULT_ORDERER_PORT      = 7050
DEFAULT_PEER_REQUEST_PORT = 7051
DEFAULT_PEER_EVENT_PORT   = 7053

# Binaries
CONFIGTXGEN="bin/configtxgen"
CRYPTOGEN="bin/cryptogen"
CONFIGTXLATOR="bin\configtxlator"

# Config paths
GENERATED     = "generated"
LOCAL         = "local"
SRCPATH       = "/msp/"
DSTARTIFACTS  = "/artifacts"
DSTPATH       = "/artifacts/channel/"
DSTCRYPTO     = "crypto-config/"
CACRTFILE     = "ca.crt"
KEYSTOREDIR   = "/msp/keystore"
SIGNCERTSDIR  = "/msp/signcerts"

# Hyperledger images for docker
PEER_IMAGE    = "hyperledger/fabric-peer:x86_64-1.0.5"
ORDERER_IMAGE = "hyperledger/fabric-orderer:x86_64-1.0.5" 
CA_IMAGE      = "hyperledger/fabric-ca:x86_64-1.0.5"

DEFAULTNETWORK = "net" 
DEFAULT_NB_USERS = 1

# Filenames
DOCKERCOMPOSE_FN   = "docker-compose.yaml"
CNFIGTX_FN         = "configtx.yaml"
CRYPTOCONFIG_FN    = "crypto-config.yaml"
NETCONFIG_FN       = "network-config.json"
CHANNEL_NAME       = "mychannel"
GENESISBLOCKNAME   = "genesis.block"

# Explorer constants
EXPLORER_PORT  = "8080"
EXPLORER_LOCAL = "/opt/ols/explorer/local/"
EXPLORER_HOST  = "localhost" 
EXPLORER_MSQL_HOST  = "127.0.0.1"
EXPLORER_MSQL_PORT  = "3306"
EXPLORER_MSQL_DB    = "fabricexplorer"
EXPLORER_MSQL_LOGIN = "root"
EXPLORER_MSQL_PWD   = "123456"
EXPLORER_CONFIG_FN  = "config.json"
EXPLORER_PATH = "explorer/local"

# Composer constants
COMPOSER_PATH = "composer/local"
COMPOSER_CONFIG_FN = "connection.json"
COMPOSER_LOCAL = "/opt/ols/composer/local/"