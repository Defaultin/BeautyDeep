#!/bin/bash

sudo apt-get update
sudo apt-get -y install python3 python3-pip git
git clone https://github.com/Defaultin/BeautyDeep.git
pip3 install -r BeautyDeep/web-server/requirements.txt
python3 BeautyDeep/web-server/ngrok.py