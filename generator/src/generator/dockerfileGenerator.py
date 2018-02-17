# -*- coding: utf8 -*-
'''
Created on 15 february 2018
@author: PYOL6775
'''

from generator.yaml_utils import dump_yaml_file
from generator.cmd_utils import exec_cmd
from generator.constants import CA_PORT, ORDERER_PORT, PEER_EVENT_PORT, PEER_REQUEST_PORT, DOCKERCOMPOSE_FN, logger, my_path

class DockerService:
    def __init__(self, ports, volumes, environment, command, image, container_name, working_dir=None, networks=None):
        self.ports=ports
        self.volumes=volumes
        self.environment=environment
        self.command=command
        self.image=image
        self.container_name=container_name
        self.working_dir=working_dir
        self.networks=networks

    def to_dict(self):
        dict={}
        dict['ports']=[port for port in self.ports]
        dict['volumes']=self.volumes
        dict['environment']=self.environment
        dict['command']=self.command
        dict['image']=self.image
        dict['container_name']=self.container_name 
        if self.working_dir != None:
            dict['working_dir']=self.working_dir
        if self.networks != None:
            dict['networks']=self.networks            
        return dict                       

def __build_ca_service(caID, peerOrg, ca_image, tls, pk_name, port, network):
    try:
        environment=[   "FABRIC_CA_HOME=/etc/hyperledger/fabric-ca-server", 
                        "FABRIC_CA_SERVER_CA_NAME=ca-"+peerOrg.org_name,
                        "FABRIC_CA_SERVER_TLS_ENABLED="+tls,
                        "FABRIC_CA_SERVER_TLS_CERTFILE=/etc/hyperledger/fabric-ca-server-config/ca."+peerOrg.domain+"-cert.pem",
                        "FABRIC_CA_SERVER_TLS_KEYFILE=/etc/hyperledger/fabric-ca-server-config/"+str(pk_name)
                    ]
        ports=[str(port)+":"+str(CA_PORT)]
        #command="sh -c 'fabric-ca-server start --ca.certfile /etc/hyperledger/fabric-ca-server-config/ca."+peerOrg.domain+"-cert.pem --ca.keyfile /etc/hyperledger/fabric-ca-server-config/"+pk_name+" -b admin:adminpw -d'"
        command="sh -c 'fabric-ca-server start -b admin:adminpw -d'"
        volumes=["./crypto-config/peerOrganizations/"+peerOrg.domain+"/ca/:/etc/hyperledger/fabric-ca-server-config"]
        container_name=caID
        networks=[network]
        return DockerService(ports=ports, volumes=volumes, environment=environment, command=command, image=ca_image, container_name=container_name, networks=networks)
    except Exception as e:
        logger.error (e) 
        raise Exception ("Build ca_service for Docker-compose.yaml failled!") 

def __build_orderer_service(ordererID, ordererOrg, orderer_image, peerOrgs, tls, port, network):
    try:
        environment=[   "ORDERER_GENERAL_LOGLEVEL=debug", 
                        "ORDERER_GENERAL_LISTENADDRESS=0.0.0.0",
                        "ORDERER_GENERAL_GENESISMETHOD=file",
                        "ORDERER_GENERAL_GENESISFILE=/etc/hyperledger/configtx/genesis.block",
                        "ORDERER_GENERAL_LOCALMSPID="+ordererOrg.mspid,
                        "ORDERER_GENERAL_LOCALMSPDIR=/etc/hyperledger/crypto/orderer/msp",
                        "ORDERER_GENERAL_TLS_ENABLED="+tls,
                        "ORDERER_GENERAL_TLS_PRIVATEKEY=/etc/hyperledger/crypto/orderer/tls/server.key",
                        "ORDERER_GENERAL_TLS_CERTIFICATE=/etc/hyperledger/crypto/orderer/tls/server.crt",
                        "ORDERER_GENERAL_TLS_ROOTCAS=[/etc/hyperledger/crypto/orderer/tls/ca.crt, /etc/hyperledger/crypto/peerOrg1/tls/ca.crt, /etc/hyperledger/crypto/peerOrg2/tls/ca.crt]"
                    ]
        ports=[str(port)+":"+str(ORDERER_PORT)]
        command="orderer"
        volumes=[   "./:/etc/hyperledger/configtx",
                    "./crypto-config/ordererOrganizations/"+ordererOrg.domain+"/orderers/"+ordererOrg.org_name.lower()+"."+ordererOrg.domain+"/:/etc/hyperledger/crypto/orderer",
                    "./crypto-config/peerOrganizations/"+peerOrgs[0].domain+"/peers/"+peerOrgs[0].peers[0].hostname+":/etc/hyperledger/crypto/peerOrg1",
                    "./crypto-config/peerOrganizations/"+peerOrgs[1].domain+"/peers/"+peerOrgs[1].peers[0].hostname+":/etc/hyperledger/crypto/peerOrg2"
                ]
        container_name=ordererID
        networks=[network]
        working_dir="/opt/gopath/src/github.com/hyperledger/fabric/orderers"
        return DockerService(ports=ports, volumes=volumes, environment=environment, command=command, image=orderer_image, container_name=container_name, working_dir=working_dir, networks=networks)
    except Exception as e:
        logger.error (e) 
        raise Exception ("build_orderer_service for Docker-compose.yaml failled!") 


def __build_peer_service(peerID, peerOrg, peer_image, tls, port_req, port_evt, network):
    try:
        environment=[
            "CORE_PEER_ID="+peerID,
            "CORE_PEER_ADDRESS="+peerID+":"+str(PEER_REQUEST_PORT),
            "CORE_PEER_LOCALMSPID="+peerOrg.org_name+"MSP",
            "CORE_VM_ENDPOINT=unix:///host/var/run/docker.sock",
            "CORE_VM_DOCKER_HOSTCONFIG_NETWORKMODE=artifacts_default",
            "CORE_LOGGING_LEVEL=DEBUG",
            "CORE_PEER_GOSSIP_USELEADERELECTION=true",
            "CORE_PEER_GOSSIP_ORGLEADER=false",
            "CORE_PEER_GOSSIP_EXTERNALENDPOINT="+peerID+":"+str(PEER_REQUEST_PORT),
            "CORE_PEER_GOSSIP_BOOTSTRAP="+peerID+":"+str(PEER_REQUEST_PORT),
            #"CORE_PEER_GOSSIP_SKIPHANDSHAKE=true",
            "CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/crypto/peer/msp",
            "CORE_PEER_TLS_ENABLED="+tls,
            "CORE_PEER_TLS_KEY_FILE=/etc/hyperledger/crypto/peer/tls/server.key",
            "CORE_PEER_TLS_CERT_FILE=/etc/hyperledger/crypto/peer/tls/server.crt",
            "CORE_PEER_TLS_ROOTCERT_FILE=/etc/hyperledger/crypto/peer/tls/ca.crt"
            ]
        ports=[str(port_req)+":"+str(PEER_REQUEST_PORT), str(port_evt)+":"+str(PEER_EVENT_PORT)]   
        command="peer node start"     
        volumes=["/var/run/:/host/var/run/",
                "./crypto-config/peerOrganizations/"+peerOrg.domain+"/peers/"+peerID+"/msp:/etc/hyperledger/crypto/peer/msp",
                "./crypto-config/peerOrganizations/"+peerOrg.domain+"/peers/"+peerID+"/tls:/etc/hyperledger/crypto/peer/tls"]
        container_name=peerID
        networks=[network]
        working_dir="/opt/gopath/src/github.com/hyperledger/fabric/peer"
        return DockerService(ports=ports, volumes=volumes, environment=environment, command=command, image=peer_image, container_name=container_name, working_dir=working_dir, networks=networks)
    except Exception as e:
        logger.error (e) 
        raise Exception ("build_peer_service for Docker-compose.yaml failled!") 

def create_docker_compose_file(ordererOrgs, peerOrgs, peer_image, orderer_image, ca_image, tls, dir, network="net", filename=DOCKERCOMPOSE_FN):
    try:
        logger.info("Create docker-compose.yaml...")
        services=[]
        for peerOrg in peerOrgs:  
            caID="ca_peer"+peerOrg.org_name
            #pk_name=caID.upper()+"_PK"
            cmd = ('cd {0}/crypto-config/peerOrganizations/{1}/ca/ && ls *_sk'.format(dir, peerOrg.domain))
            pk_name = exec_cmd(cmd).replace('\n','').replace('\r','')
            services.append(__build_ca_service(caID=caID, peerOrg=peerOrg, ca_image=ca_image, tls=tls, pk_name=pk_name, port=peerOrg.ca.port, network=network))
            for peer in peerOrg.peers:
                peerID=peer.hostname
                services.append(__build_peer_service(peerID=peerID, peerOrg=peerOrg, peer_image=peer_image, tls=tls, port_req=peer.request_port, port_evt=peer.event_port, network=network))
        for ordererOrg in ordererOrgs:
            ordererID=ordererOrg.org_name.lower()+"."+ordererOrg.domain
            services.append(__build_orderer_service(ordererID=ordererID, ordererOrg=ordererOrg, orderer_image=orderer_image, peerOrgs=peerOrgs, tls=tls, port=ordererOrg.port, network=network))
        dockerfile_dict={'version':"2"}
        dockerfile_dict['networks']={network:None}
        dockerfile_dict['services']= {service.container_name:service.to_dict() for service in services}
        dump_yaml_file(data=dockerfile_dict, file_path=dir+"/"+filename)
        #logger.debug(json.dumps(dockerfile_dict, indent=4))
        #exec_cmd('cp {0}samples/1.0.4/docker-compose.yaml {1}/{2}'.format(my_path, dir, "docker-compose.yaml"))
        #exec_cmd('cp {0}samples/1.0.4/base.yaml {1}/{2}'.format(my_path, dir, "base.yaml"))

    except Exception as e:
        logger.error (e) 
        raise Exception ("create_docker_compose_file failled!")