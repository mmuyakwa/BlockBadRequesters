#!/bin/bash

# root is always user_id 0
SUDO=''
if [ $(id -u) -ne 0 ]; then
    SUDO='sudo'
    echo "Your not root."
    echo "Using with SUDO, where needed."
fi

# File where we will save all bad requests from NGINX-Log.
touch nginx.errors
ERRORFILE = 'nginx.errors'

# Generate normal report in '/var/www/html/report/report.html'
$SUDO goaccess -f /var/log/nginx/access.log -o /var/www/html/report/report.html --log-format=COMBINED

# Filter all bad requests (HTTP_ERRORS 4XX [400, 404, ...]) and save in 'nginx.errors'
grep -hr '" 4' /var/log/nginx/*.log* > $ERRORFILE

# Generate report about all BAD requests in '/var/www/html/report/bad.html'
$SUDO goaccess -f $ERRORFILE -o /var/www/html/report/bad.html --log-format=COMBINED

echo "Goto https://YOUR_SERVERNAME/report/report.html"
echo "Goto https://YOUR_SERVERNAME/report/bad.html"

# Script to add bad IP's to /etc/hosts.deny
$SUDO python BlockBadRequesters.py

# After adding bad IP's to exclusion-file /etc/hosts.deny , restart DenyHost-Service
$SUDO systemctl restart denyhosts.service

# Cleanup
rm $ERRORFILE
