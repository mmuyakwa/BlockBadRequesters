#!/bin/bash

# root is always user_id 0
SUDO=''
if [ $(id -u) -ne 0 ]; then
    SUDO='sudo'
    echo "Your not root."
    echo "Running apt-get with SUDO."
fi

# Install requirements for Python
pip install -r requirements.txt

# Install goaccess v1.3
$SUDO apt-get install goaccess -y

# Generate the Path where the Report-HTML will be generated
[ ! -d "/var/www/html/report/" ] && mkdir '/var/www/html/report/'

# Install denyhosts
wget http://mesh.dl.sourceforge.net/sourceforge/denyhosts/DenyHosts-2.0.tar.gz
tar xvfz DenyHosts-2.0.tar.gz
cd DenyHosts-2.0
$SUDO python setup.py install
