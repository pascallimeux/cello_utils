# -*- coding: utf8 -*-
'''
Created on 15 february 2018
@author: PYOL6775
'''

from models import OrdererOrg, PeerOrg, Peer, Ca, Cert
from cryptoconfig_gen import generate_certs
from configtx_gen import generate_channels_artifacts
from docker_gen import create_docker_compose_file
from network_config_gen import create_network_configFile4his, generate_artifacts_for4his
from yaml_utils import logger, exec_cmd, root_path
from constants import CA_PORT, ORDERER_PORT, PEER_EVENT_PORT, PEER_REQUEST_PORT
from constants import  PEER_IMAGE, ORDERER_IMAGE, CA_IMAGE, DEFAULTNETWORK, GENERATED, LOCAL
import os 

if __name__ == '__main__':
    try:
#---------------------------------------------------
        IP      = "192.168.8.133"
        DOMAIN  = "example.com" #"orange-labs.fr"
        CHANNEL = "mychannel" #"orange1"
        ORDERERORGNAME="Orderer"
        PEERORGNAME1="Org1" #"Org-or1"
        PEERORGNAME2="Org2"  #"Org-or2"
        PROVINCE="Rhone Alpe"
        COUNTRY="FR"
        LOCALITY="Meylan"
        PEER01PORTREQUEST=PEER_REQUEST_PORT
        PEER11PORTREQUEST=7056
        PEER02PORTREQUEST=8051
        PEER12PORTREQUEST=8056
        PEER01PORTEVNT=PEER_EVENT_PORT
        PEER11PORTEVNT=7058
        PEER02PORTEVNT=8053
        PEER12PORTEVNT=8088 
        CA1PORT=CA_PORT
        CA2PORT=8054  
        ORDERERPORT=ORDERER_PORT 
        NBADMINS = 1
        TLS=True
#---------------------------------------------------

        if TLS:
            GRPCSURL = "grpcs://"+IP
            HTTPSURL = "https://"+IP
            tls="true"
        else:
            GRPCSURL = "grpc://"+IP
            HTTPSURL = "http://"+IP
            tls="false"
        cert = Cert(country=COUNTRY, province=PROVINCE, locality=LOCALITY)
        peer0_1=Peer(url=GRPCSURL, request_port=PEER01PORTREQUEST,  event_port=PEER01PORTEVNT)
        peer1_1=Peer(url=GRPCSURL, request_port=PEER11PORTREQUEST,  event_port=PEER11PORTEVNT)
        peer0_2=Peer(url=GRPCSURL, request_port=PEER02PORTREQUEST,  event_port=PEER02PORTEVNT)
        peer1_2=Peer(url=GRPCSURL, request_port=PEER12PORTREQUEST, event_port=PEER12PORTEVNT)
        ca1 = Ca(url=HTTPSURL, port=CA1PORT)
        ca2 = Ca(url=HTTPSURL, port=CA2PORT)
        ordererOrg = OrdererOrg(org_name=ORDERERORGNAME, domain=DOMAIN, url=GRPCSURL, port=ORDERERPORT)
        peerOrg1 = PeerOrg(org_name=PEERORGNAME1, domain=DOMAIN, nb_admins=NBADMINS, peers=[peer0_1, peer1_1], ca=ca1, orderers=)
        peerOrg2 = PeerOrg(org_name=PEERORGNAME2, domain=DOMAIN, nb_admins=NBADMINS, peers=[peer0_2, peer1_2], ca=ca2) 
        ordererOrgs=[ordererOrg]
        peerOrgs=[peerOrg1, peerOrg2]

        channel_dir = root_path+GENERATED+"/"+CHANNEL+"/"
        local_dir = channel_dir + LOCAL
        exec_cmd("rm -Rf {}".format(channel_dir))
        exec_cmd("mkdir -p {}".format(local_dir))

        generate_certs(cert=cert, ordererOrgs=ordererOrgs, peerOrgs=peerOrgs, dir=local_dir)

        generate_channels_artifacts(ordererOrgs=ordererOrgs, 
                                    peerOrgs=peerOrgs, 
                                    dir=local_dir, 
                                    channel_name=CHANNEL)

        create_docker_compose_file( ordererOrgs=ordererOrgs, 
                                    peerOrgs=peerOrgs, 
                                    peer_image=PEER_IMAGE, 
                                    orderer_image=ORDERER_IMAGE, 
                                    ca_image=CA_IMAGE, 
                                    tls=tls, 
                                    dir=local_dir,
                                    network=DEFAULTNETWORK)


        #generate_artifacts_for4his(ordererOrgs=ordererOrgs, peerOrgs=peerOrgs, dir=dir)
        #create_network_configFile4his(ordererOrgs=ordererOrgs, peerOrgs=peerOrgs, dir=dir)

    except Exception as e:
        logger.error (e)                                    