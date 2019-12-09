#!/bin/bash

sudo pip install jinja2
sudo wget https://www.privateinternetaccess.com/openvpn/openvpn.zip
mkdir configs
cd configs
unzip ../openvpn.zip
cd ..

python generate.py

read -r -p "Install system configs? [y/N] " response
response=${response,,}    # tolower
if [[ "$response" =~ ^(yes|y)$ ]]; then
    sudo cp output/*.nmconnection /etc/NetworkManager/system-connections
    sudo chmod 600 /etc/NetworkManager/system-connections/*
    sudo service network-manager restart
fi
