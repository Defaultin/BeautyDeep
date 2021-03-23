#!/bin/bash

sudo apt-get update
sudo apt-get -y install python3 python3-pip git gunicorn3
sudo apt -y install nginx
git clone https://github.com/Defaultin/BeautyDeep.git
pip3 install -r BeautyDeep/web-server/requirements.txt

wget -qO - icanhazip.com
public_ip="wget -qO - icanhazip.com"

sudo echo """server {
    listen 80;
    server_name $(wget -qO - icanhazip.com);

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}""" > /etc/nginx/sites-enabled/BeautyDeep

sudo unlink /etc/nginx/sites-enabled/default
sudo nginx -s reload
cd BeautyDeep/web-server
sudo gunicorn3 --bind 127.0.0.1:5000 server:app