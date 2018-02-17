#!/bin/bash

# Usage:
# ./install-vm.sh
#
# User must then logout and login upon completion of script
#

# Exit on any failure
set -e
OLS_FOLDER="/opt/ols"
COMPOSER_FOLDER=$OLS_FOLDER"/composer"
EXPLORER_FOLDER=$OLS_FOLDER"/explorer"
MYLOGIN="$(whoami)"
MYGRP="$(id -g -n $MYLOGIN)"

check(){
    # Array of supported versions
    declare -a versions=('trusty' 'xenial' 'yakkety', 'sonya');

    # check the version and extract codename of ubuntu if release codename not provided by user
    if [ -z "$1" ]; then
        source /etc/lsb-release || \
            (echo "Error: Release information not found, run script passing Ubuntu version codename as a parameter"; exit 1)
        CODENAME=${DISTRIB_CODENAME}
    else
        CODENAME=${1}
    fi
    # correspondance for mint
    if [[ "$CODENAME" == "sonya" ]]; then 
        CODENAME="xenial"
    fi
    # check version is supported
    if echo ${versions[@]} | grep -q -w ${CODENAME}; then
        echo "Installing Hyperledger Composer prereqs for Ubuntu ${CODENAME}"
    else
        echo "Error: Ubuntu ${CODENAME} is not supported"
        exit 1
    fi

    # Update package lists
    echo "# Updating package lists"
    sudo apt-add-repository -y ppa:git-core/ppa
    sudo apt update
}


install_git_curl(){
    # Install Git and Curl
    echo "# Installing Git and Curl"
    sudo apt-get install -y git curl
}

install_nvm(){
    # Install nvm dependencies
    echo "# Installing nvm dependencies"
    sudo apt-get -y install build-essential libssl-dev

    # Execute nvm installation script
    echo "# Executing nvm installation script"
    curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.2/install.sh | bash

    # Set up nvm environment without restarting the shell
    export NVM_DIR="${HOME}/.nvm"
    [ -s "${NVM_DIR}/nvm.sh" ] && . "${NVM_DIR}/nvm.sh"
    [ -s "${NVM_DIR}/bash_completion" ] && . "${NVM_DIR}/bash_completion"
}


install_node_npm_pm2(){
    # Install node
    echo "# Installing nodeJS"
    nvm install --lts

    # Configure nvm to use version 6.9.5
    nvm use --lts
    nvm alias default 'lts/*'

    # Install the latest version of npm
    echo "# Installing npm"
    npm install npm@latest -g
    npm install pm2 -g
}

install_docker(){
    echo $CODENAME
    # Ensure that CA certificates are installed
    sudo apt-get -y install apt-transport-https ca-certificates

    # Add Docker repository key to APT keychain
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

    # Update where APT will search for Docker Packages
    echo "deb [arch=amd64] https://download.docker.com/linux/ubuntu ${CODENAME} stable" | \
        sudo tee /etc/apt/sources.list.d/docker.list

    # Update package lists
    sudo apt-get update

    # Verifies APT is pulling from the correct Repository
    sudo apt-cache policy docker-ce

    # Install kernel packages which allows us to use aufs storage driver if V14 (trusty/utopic)
    if [ "${CODENAME}" == "trusty" ]; then
        echo "# Installing required kernel packages"
        sudo apt-get -y install linux-image-extra-$(uname -r) linux-image-extra-virtual
    fi
    echo "# Installing Docker"
    sudo apt-get -y install docker-ce
    # Add user account to the docker group
    sudo usermod -aG docker $MYLOGIN
}

# Install docker compose
install_docker-compose(){
    echo "# Installing Docker-Compose"
    sudo curl -L "https://github.com/docker/compose/releases/download/1.13.0/docker-compose-$(uname -s)-$(uname -m)" \
        -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
}

# Install python v2 if required
install_python() {
    set +e
    COUNT="$(python -V 2>&1 | grep -c 2.)"
    if [ ${COUNT} -ne 1 ]
    then
    sudo apt-get install -y python-minimal
    fi
}

# Install blockchain-explorer
explorer_install(){
    cd $COMPOSER_EXPLORER && sudo git clone https://gerrit.hyperledger.org/r/blockchain-explorer
    cd $COMPOSER_EXPLORER/blockchain-explorer && npm install
    sudo apt install mysql-server -y
}

# Install composer
composer_install(){
    npm install -g composer-cli
    npm install -g composer-rest-server
    npm install -g generator-hyperledger-composer
    npm install -g yo
    npm install -g composer-playground
}

# Create folder application
create_application_folder(){
    if [ ! -d $OLS_EXPLORER ]; then
        sudo mkdir $OLS_EXPLORER
    fi
    sudo cp -R * $OLS_FOLDER
    sudo chown $MYLOGIN.$MYGRP -R $OLS
}


# Print installation details for user
display_version(){
    echo ''
    echo 'Installation completed, versions installed are:'
    echo ''
    echo -n 'Node:                 '
    node --version
    echo -n 'npm:                  '
    npm --version
    echo -n 'Docker:               '
    docker --version
    echo -n 'Docker Compose:       '
    docker-compose --version
    echo -n 'Python:               '
    python -V
    echo -n 'composer-cli:         '
    composer --version
    echo -n 'composer-playground   '
    composer-playground --version
    echo -n 'compooser-rest-server '
    composer-rest-server --version
}

check
install_git_curl
install_nvm
install_node_npm_pm2
install_docker
install_docker-compose
install_python
composer_install
explorer_install
display_version
create_application_folder


# Print reminder of need to logout in order for these changes to take effect!
echo ''
echo "Please logout then login before continuing."
