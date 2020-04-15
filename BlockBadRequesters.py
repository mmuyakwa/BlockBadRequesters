#!/bin/python

# title:         BlockBadRequesters.py
# description:   This script is meant for adding bad hosts (from custom NGINX-Log) to DenyHosts-Service.
# author:        Michael Muyakwa
# created:       2020-04-15
# updated:       2020-04-15
# version:       1.0
# license:       MIT

# regex needed to work: pip install -r requirments.txt
import regex

# Open the DenyHosts-File
blacklist = open('/etc/hosts.deny', 'a+')
# Jump to first Line, because we opened File in Append-Mode (a+)
blacklist.seek(0)
# Lof-File we generated earlier with all Bad-Requests
logfile = open('nginx.errors', 'r')
# Setting up variables for saving the IP's later.
ips_log = [] # IP's from Logfile will be saved here
ips_blist = [] # Known IP's from /etc/hosts.deny will be saved here

# Returns IP from String
def find_ip(s):
    re = regex.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', s).group()
    return re

# Closes the File-Operators for Cleanup
def close_all():
    blacklist.close()
    logfile.close()
    return

# Checking if IP is already known, to prevent duplicate entries
def is_new(ip, ips, checkList):
    if ip not in checkList:
        ips.append(ip)
        #print ("Added IP: ", ip)

# Check if IP is present in List
def check(sentence, words):
    res = [all([k in s for k in words]) for s in sentence]
    return [sentence[i] for i in range(0, len(res)) if res[i]]


# Main Method
def main():
    # Main

    # Step 1
    # Find all IP's in Log-File
    for line1 in logfile:
        is_new(find_ip(line1), ips_log, ips_log)

    # Number of found IP's in Log
    print("LOG - Number of found IP's: ", len(ips_log))

    # Step 2
    # Find all IP's in BlackList
    #print (blacklist.read())
    for line2 in blacklist:
        if not (regex.match('\r?\n', line2)): # Make sure the Line is not empty
            try:
                is_new(find_ip(line2), ips_blist, ips_blist) # Check if IP was already seen
            except:
                #print("Something went wrong")
                pass
        else:
            pass

    # Number of found IP's in BlackList
    print("BLIST - Number of found IP's: ", len(ips_blist))

    # Step 3
    # Find new IP's
    res = []
    for item in ips_log:
        try:
            if len(check(ips_blist, item)) == 0: # Check if IP is already present in DenyHosts-File
                res.append(item)
        except:
            # res.append(item)
            pass


    # Step 4
    # Add new IP's to BlackList
    count = 0
    for item in res:
        if len(check(ips_blist, item)) == 0: # Check if IP is already present in DenyHosts-File
            count += 1
            blacklist.write("ALL: %s\r\n" % (item)) # Add IP to DenyHosts-File and disallow all protocols (SSH/HTTP/HTTPS/FTP...)
        else:
            res.remove(item) # Remove from List, because IP was already known.

    print("DIFF - Number of found IP's: ", len(res))
    # print(res)

    # Closing files
    close_all

    # The number of new IP's added to DenyHosts.
    print(count, " added IP's")

    # print(ips_log)
    # print(ips_blist)
    # print(res)


if __name__ == '__main__':
    main()
