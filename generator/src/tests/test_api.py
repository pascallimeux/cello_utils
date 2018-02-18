# -*- coding: utf8 -*-
'''
Created on 18 february 2018
@author: PYOL6775
'''
# python -m unittest test_api.TestApis.test_generate_api

import os, sys
import unittest, json

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from generator.constants import logger
from app import app
from generator.constants import DEFAULT_PEER_EVENT_PORT, DEFAULT_PEER_REQUEST_PORT, DEFAULT_ORDERER_PORT, DEFAULT_CA_PORT
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
    logger.debug(json.dumps(config, indent=4))
    return config

class TestApis(unittest.TestCase): 
 
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.config = config_test(tls=True, ip="192.168.8.133")

    def tearDown(self):
        pass

 
    def test_generate_api(self):
        data=json.dumps(self.config)
        response = self.app.post(
            '/generator/api/v1.0/generate',
            data=data,
        )
        logger.debug(response)
        self.assertEqual(response.status_code, 201)
 
 
if __name__ == "__main__":
    unittest.main()