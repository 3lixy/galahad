#!/bin/bash


# Set the hostname
echo "127.0.0.1 rethinkdb.galahad.com" | sudo tee -a /etc/hosts


# Add RethinkDB repository and install
source /etc/lsb-release && echo "deb http://download.rethinkdb.com/apt $DISTRIB_CODENAME main" | sudo tee /etc/apt/sources.list.d/rethinkdb.list
sudo wget -qO- https://download.rethinkdb.com/apt/pubkey.gpg | sudo apt-key add -
sudo apt-get update
sudo apt-get --assume-yes install rethinkdb

# Retrieve keys and put them in their appropriate location
sudo mkdir -p /var/private/ssl/

sudo cp galahad-config/rethinkdb_keys/rethinkdb.pem      /var/private/ssl/
sudo cp galahad-config/rethinkdb_keys/rethinkdb_cert.pem /var/private/ssl/
sudo cp galahad-config/excalibur_private_key.pem         /var/private/ssl/

sudo chown rethinkdb:rethinkdb /var/private/ssl/*.pem
sudo chmod 600 /var/private/ssl/*.pem


# Put RethinkDB configuration file in its appropriate location
sudo cp rethinkdb.conf /etc/rethinkdb/instances.d/


# Restart RethinkDB with its new configuration file
sudo /etc/init.d/rethinkdb restart


# Install python libraries for rethinkdb and configure the database
sudo apt-get --assume-yes install python2.7 python-pip
pip install rethinkdb==2.3.0.post6


sudo python configure_rethinkdb.py
