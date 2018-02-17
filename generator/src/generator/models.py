# -*- coding: utf8 -*-
'''
Created on 15 february 2018
@author: PYOL6775
'''

from constants import DEFAULT_CA_PORT, DEFAULT_ORDERER_PORT, DEFAULT_PEER_EVENT_PORT, DEFAULT_PEER_REQUEST_PORT, DEFAULT_NB_USERS
from MyMalformedException import MyMalformedException

class Channel:
    def __init__(self, name):
        self.name = name

class Cert:
    def __init__(self, country, province, locality):
        self.country = country
        self.province = province
        self.locality = locality

class Node:
    def __init__(self, address, port):
        self.address = address
        self.port    = port
        self.url     = "{0}:{1}".format(address, str(port))

    def complete(self, name, domain):
        self.name = name
        self.hostname = "{0}.{1}".format(name, domain)

class Ca(Node):
    def __init__(self, address, port=DEFAULT_CA_PORT):
        super().__init__(address, port)

class Orderer(Node):
    def __init__(self, address, port=DEFAULT_ORDERER_PORT):
        super().__init__(address, port)

class Peer(Node):
    def __init__(self, address, request_port=DEFAULT_PEER_REQUEST_PORT, event_port=DEFAULT_PEER_EVENT_PORT):
        super().__init__(address, request_port)
        self.request_port = request_port
        self.event_port   = event_port
        self.request_url  = self.url
        self.event_url    = "{0}:{1}".format(address,str(self.event_port))

class OrdererOrg:
    def __init__(self, org_name, domain, orderers):
        self.org_name=org_name
        self.mspid=org_name+"MSP"
        self.domain=domain
        self.nb_orderes=len(orderers)
        self.orderers = []
        self.mspdir = "crypto-config/ordererOrganizations/{}/msp".format(self.domain)
        self.tls_cacerts_path = "ordererOrganizations/{0}/orderers/{1}.{2}/tls".format(domain, self.org_name.lower(), self.domain)
        indice = 0
        for orderer in orderers:
            orderer.complete("orderer"+str(indice),self.domain)
            self.orderers.append(orderer)
            indice = indice + 1

class PeerOrg:
    def __init__(self, org_name, domain, peers, ca):
        self.nb_users = DEFAULT_NB_USERS
        self.org_name=org_name
        self.mspid=org_name+"MSP"
        self.domain="{0}.{1}".format(org_name, domain).lower()
        self.nb_peers=len(peers)
        self.peers = []
        self.mspdir = "crypto-config/peerOrganizations/{}/msp".format(self.domain)
        self.adminkeyspath="peerOrganizations/"+self.domain+"/users/Admin@"+self.domain
        self.ca = ca
        indice=0
        for peer in peers:
            peer.complete("peer"+str(indice),self.domain)
            self.peers.append(peer)
            indice = indice + 1

class Config:
    def __init__(self, cert, channel, orderer_org, peer_orgs):
        self.cert = cert
        self.channel = channel
        self.orderer_org = orderer_org
        self.peer_orgs = peer_orgs


def json2cert(data):
    try:
        return  Cert(data['country'], data['province'], data['locality'])
    except Exception:
        raise MyMalformedException("Malformed json certificate") 

def json2channel(data):
    try:
        return Channel(data['name'])
    except Exception:
        raise MyMalformedException("Malformed json channel") 

def json2orderer(data):
    try:
        return Orderer(data['address'], data['port'])
    except Exception:
        raise MyMalformedException("Malformed json orderer") 
     
def json2peer(data):
    try:
        return Peer(data['address'], data['request_port'], data['event_port'])
    except Exception as e :
        raise MyMalformedException("Malformed json peer") 

def json2ca(data):
    try:
        return Ca(data['address'], data['port'])
    except Exception:
        raise MyMalformedException("Malformed json ca") 

def json2ordererOrg(data):
    try:
        domain = data ['domain']
        name   = data ['org_name']
        orderers_data = data['orderers']
        orderers = []
        for orderer_data in orderers_data:
            orderers.append(json2orderer(orderer_data))
        return OrdererOrg(name, domain, orderers)
    except Exception as e:
        raise MyMalformedException("Malformed json ordererOrg") 


def json2peerOrgs(data):
    try:
        peer_orgs = []
        for peerOrg in data:
            domain = peerOrg ['domain']
            name   = peerOrg ['org_name']
            ca = json2ca(peerOrg['ca'])
            peers_data = peerOrg['peers']
            peers = []
            for peer_data in peers_data:
                peers.append(json2peer(peer_data))
            peer_orgs.append(PeerOrg(name, domain, peers, ca))
        return peer_orgs
    except Exception as e :
        raise MyMalformedException("Malformed json peerOrg") 

def json2config(data):
    try:
        certificate = json2cert(data['cert'])
        channel = json2channel(data['channel'])
        orderer_orgs = json2ordererOrg(data['orderer_org'])
        peer_orgs = json2peerOrgs(data['peer_orgs'])
        return Config(certificate, channel, orderer_orgs, peer_orgs)
    except MyMalformedException as e:
        raise (e)
    except Exception as e:
        raise Exception ("Malformed json config")
