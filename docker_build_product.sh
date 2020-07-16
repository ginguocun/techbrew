#!/bin/sh

cd /opt || exit
cp /opt/techbrew/dockerfile_product /opt/dockerfile_product
sudo docker build --rm -t tb2:$1 -f dockerfile_product .
