#!/bin/bash

function createEnv(){
    echo "Create venv directory."
    virtualenv venv -p python3
    source venv/bin/activate
    pip install -r requirements.txt
    deactivate
}

function removeEnv(){
    if [ -d venv ]; then
        echo "Remove venv directory."
        sudo rm -Rf venv 
    fi
}

removeEnv
createEnv