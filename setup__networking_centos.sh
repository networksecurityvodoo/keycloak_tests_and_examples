#!/bin/bash          

#####################################################################
### Skript changes the network configruation in                    ##
### File:  /etc/sysconfig/netowrking/scripts/ifcfg-$interfacename  ##
#####################################################################

# Get Interfacename 
interfacename=`nmcli -t | grep ^en | cut -d ":" -f1`

# Save old values to file
nmcli con show $interfacename | grep ipv4 >> nw_values.old

# Setup static IP-Address
nmcli con mod $interfacename ip4.address "10.0.0.1"

# Setup Gateway
nmcli con mod $interfacename ipv4.gateway "8.8.8.8"

# Setup DNS
nmcli con mod $interfacename ipv4.dns "8.8.8.8 8.8.4.4"

# show new settings
nmcli con show $interfacename | grep ipv4 >> nw_values.new
nmcli con show $interfacename | grep ipv4

#Restart Networking
nmcli networking off
nmcli networking on

exit
