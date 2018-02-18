#!/bin/bash
HYP_FOLDER=$GOPATH/src/github.com/hyperledger
HYP_VERSION=v1.0.5
if [ -d $HYP_FOLDER ]; then
        sudo rm -Rf $HYP_FOLDER 
fi
mkdir -p $HYP_FOLDER                       
cd $HYP_FOLDER               
git clone https://gerrit.hyperledger.org/r/fabric
cd fabric
git checkout $HYP_VERSION
cd $HYP_FOLDER 
git clone https://gerrit.hyperledger.org/r/fabric-ca
cd fabric-ca
git checkout $HYP_VERSION

cd $HYP_FOLDER/fabric
make configtxgen
make configtxlator
make cryptogen
cp $HYP_FOLDER/fabric/build/bin/* ../bin/
