import os
import json
import subprocess
import shutil
from pathlib import Path

LOCAL_COMPOSER_FOLDER =  "/opt/ols/composer/local"
ADMIN_LOGIN           = "admin"
ADMIN_PWD             = "adminpw"
PEER_ADMIN            = "PeerAdmin"
BUSINESS_ADMIN        = "BusinessAdmin"

class Connection():
    def __init__(self, json_data, filename):
        self.filename  = filename
        self.name      = json_data["name"]
        self.type      = json_data["type"]
        self.mspID     = json_data["mspID"]
        self.channel   = json_data["channel"]
        self.timeout   = json_data["timeout"]
        self.ca        = json_data["ca"]
        self.peers     = json_data["peers"]
        self.orderers  = json_data["orderers"]
        self.card_path = ""
        self.key_path  = ""
        self.cert_path = ""
        self.adm_key   = ""
        self.adm_cert  = ""
        self.admin_login = ""
        self.admin_pwd = ""
        self.peer_admin_name = ""
        self.business_admin_name = ""
        self.peeradmin_card_name = ""
        self.business_admin_pub_pem = ""
        self.business_admin_priv_pem = ""
        self.bna_path = ""
        self.network_name = ""
        self.deploy_bna = False


def create_admin_cards():
    orgs=os.listdir(LOCAL_COMPOSER_FOLDER)  
    connections = []
    for org in orgs:
        org_path   = "{0}/{1}/".format(LOCAL_COMPOSER_FOLDER, org)
        connection = __build_connection(org_path, ADMIN_LOGIN, ADMIN_PWD, PEER_ADMIN, BUSINESS_ADMIN)
        connection.peeradmin_card_name = __create_network_admin_card(connection)
        connections.append(connection)
    return connections

def start_networks(connections):
    for connection in connections:
        if connection.deploy_bna :
            __install_runtime_on_peers(connection)
            __create_business_admin(connection)
            __start_business_network(connection)
            __create_business_admin_card(connection)

def clean_locals_card():
    __remove_local_credentials()
    __remove_network_admin_card()

def __build_connection(org_path, admin_login, admin_pwd, peer_admin_name, business_admin_name):
    filename = "{0}connection/connection.json".format(org_path)
    data                  = json.load(open(filename))
    connection            = Connection(data, filename)
    connection.card_path  = "{0}cards".format(org_path)
    connection.key_path   = org_path + "admin/keystore/"
    connection.cert_path  = org_path + "admin/signcerts/"
    connection.adm_key    = connection.key_path + os.listdir("{0}".format(connection.key_path))[0]
    connection.adm_cert   = connection.cert_path+ os.listdir("{0}".format(connection.cert_path))[0]
    connection.admin_login = admin_login
    connection.admin_pwd   = admin_pwd
    connection.peer_admin_name     = peer_admin_name
    connection.business_admin_name = business_admin_name +"-"+ connection.name
    connection.business_admin_priv_pem = connection.card_path +"/"+ connection.business_admin_name + "/admin-priv.pem"
    connection.business_admin_pub_pem = connection.card_path +"/"+ connection.business_admin_name + "/admin-pub.pem"  
    bna = os.listdir("{0}".format(org_path + "/bna")) 
    if len(bna) == 1:
        connection.deploy_bna = True
        connection.bna_path   = org_path + "bna/"+ bna[0] 
        connection.network_name=connection.bna_path[connection.bna_path.find("bna/")+4: connection.bna_path.find("@")]
    return connection

def exec_cmd(cmd):
    print (subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf8'))


def __remove_local_credentials():
    home = str(Path.home())
    credentials_path = "{0}/.composer".format(home)
    if os.path.exists(credentials_path):
        shutil.rmtree(credentials_path)


def __remove_network_admin_card():
    orgs=os.listdir(LOCAL_COMPOSER_FOLDER)  
    for org in orgs:
        org_path  = "{0}/{1}/".format(LOCAL_COMPOSER_FOLDER, org)
        card_path = "{0}cards".format(org_path)
        if os.path.exists(card_path):
            shutil.rmtree(card_path)


def __create_network_admin_card(connection): 
    os.mkdir (connection.card_path)
    os.chdir(connection.card_path)
    card_create_cmd = "composer card create -p {0} -u {1} -c {2} -k {3} -r PeerAdmin -r ChannelAdmin".format(connection.filename, connection.peer_admin_name, connection.adm_cert, connection.adm_key)
    exec_cmd(card_create_cmd)
    peeradmin_card_name = "{0}@{1}.card".format(connection.peer_admin_name,connection.name)
    card_import_cmd = "composer card import -f {0}/{1}".format(connection.card_path, peeradmin_card_name)
    exec_cmd(card_import_cmd)
    return "{0}@{1}".format(connection.peer_admin_name, connection.name)

def __create_business_admin(connection):
    id_req_cmd      = "composer identity request -c {0} -u {1} -s {2} -d {3} ".format(connection.peeradmin_card_name, connection.admin_login, connection.admin_pwd, connection.business_admin_name)
    exec_cmd(id_req_cmd)

def __create_business_admin_card(connection):
    card_create_cmd = "composer card create -p {0} -u {1} -n {2} -c {3} -k {4}".format(connection.filename, connection.business_admin_name, connection.network_name, connection.business_admin_pub_pem, connection.business_admin_priv_pem)
    exec_cmd(card_create_cmd)
    businessadmin_card_name = "{0}@{1}".format(connection.business_admin_name, connection.network_name)
    card_import_cmd = "composer card import -f {0}.card".format(businessadmin_card_name)
    exec_cmd(card_import_cmd)
    ping_cmd = "composer network ping -c {0}".format(businessadmin_card_name)
    exec_cmd(ping_cmd)

def __install_runtime_on_peers(connection):
    inst_runtime_cmd = "composer runtime install -c {0} -n {1}".format(connection.peeradmin_card_name, connection.network_name)
    exec_cmd(inst_runtime_cmd)

def __start_business_network(connection):
    start_bn = "composer network start -c {0} -a {1} -A {2} -C {3}".format(connection.peeradmin_card_name, connection.bna_path, connection.business_admin_name, connection.business_admin_pub_pem)
    exec_cmd(start_bn)

def __start_rest_server():
    stop_rs_cmd = "kill -9 $(ps aux | grep 'composer-rest' | awk '{print $2}')"
    exec_cmd(stop_rs_cmd)
    start_rs_cmd = "nohup composer-rest-server -c  {0} -n required &".format()
    exec_cmd(start_rs_cmd)

if __name__ == "__main__":
    clean_locals_card()
    connections = create_admin_cards()
    start_networks(connections)
