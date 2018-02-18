# -*- coding: utf8 -*-
'''
Created on 16 february 2018
@author: PYOL6775
'''
# example to start a single test:
# cd cello_utils/generator/src/tests
# source ../../venv/bin/activate
# python -m unittest test_generator.TestGenerator.test_Generate_crypto_material
# python -m unittest test_generator.TestGenerator.test_Generate_channel_artifacts
# python -m unittest test_generator.TestGenerator.test_Generate4explorer
# python -m unittest test_generator.TestGenerator.test_Generate4composer
# python -m unittest test_generator.TestGenerator.test_Generate_All

import sys, os
import json
import unittest
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
from generator.constants import DEFAULT_PEER_EVENT_PORT, DEFAULT_CA_PORT, DEFAULT_ORDERER_PORT, DEFAULT_PEER_REQUEST_PORT, logger
from generator.interface import generate4composer, generate4explorer, generate_all_material, generate_dockerfiles, generate_crypto_material, generate_channel_artifacts

def config_test(tls, ip):
    DOMAIN_NAME = "example.com"
    PROVINCE    = "Rhone Alpe"
    COUNTRY     = "FR"
    LOCALITY    = "Meylan" 

    if tls:
        GRPCSURL = "grpcs://"+ip
        HTTPSURL = "https://"+ip
        tls="true"
    else:
        GRPCSURL = "grpc://"+ip
        HTTPSURL = "http://"+ip
        tls="false"

    certificate = {'country':COUNTRY, 'province':PROVINCE, 'locality':LOCALITY}
    channel     = {'name': 'mychannel'}
    peer11      = {'address':GRPCSURL, 'request_port':DEFAULT_PEER_REQUEST_PORT, 'event_port':DEFAULT_PEER_EVENT_PORT}
    peer12      = {'address':GRPCSURL, 'request_port':7056, 'event_port':7058}  
    peer21      = {'address':GRPCSURL, 'request_port':8051, 'event_port':8053}
    peer22      = {'address':GRPCSURL, 'request_port':8056, 'event_port':8088}
    orderer     = {'address':GRPCSURL, 'port':DEFAULT_ORDERER_PORT}
    ca1         = {'address':HTTPSURL, 'port':DEFAULT_CA_PORT}
    ca2         = {'address':HTTPSURL, 'port':8054}
    peerOrg1    = {'org_name': 'Org1', 'domain':DOMAIN_NAME, 'peers':[peer11, peer12], 'ca': ca1}
    peerOrg2    = {'org_name': 'Org2', 'domain':DOMAIN_NAME, 'peers':[peer21, peer22], 'ca': ca2}
    ordererOrg  = {'org_name': 'Orderer', 'domain':DOMAIN_NAME, 'orderers': [orderer]}
    config      = {'cert': certificate, 'channel':channel, 'orderer_org': ordererOrg, 'peer_orgs':[peerOrg1, peerOrg2]} 
    #logger.debug(json.dumps(config, indent=4))
    return config

class TestGenerator(unittest.TestCase):
    def setUp(self):
        self.config = config_test(tls=True, ip="192.168.8.133")

    def test_Generate_crypto_material(self):
        generate_crypto_material(self.config)

    def test_Generate_channel_artifacts(self):
        generate_channel_artifacts(self.config)
    
    def test_Generate_dockerfiles(self):
        generate_dockerfiles(self.config)

    def test_Generate4composer(self):
        generate4composer(self.config)
        
    def test_Generate4explorer(self):
        generate4explorer(self.config)

    def test_Generate_All(self):
        generate_all_material(self.config)
    

if __name__ == '__main__':
    unittest.main()