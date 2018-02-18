
linux prerequisite:
    sudo apt install virtualenv libltdl-dev -y
    install Golang (script install_go.sh)
    install hyperledger fabric 1.0.5 and generate mandatories binaries (script install_hyp.sh)
    generate configtxgen and cryptogen for your system and place them in the bin directory (script )

initialize virtualenv
    make setup


start unit tests
    make test



