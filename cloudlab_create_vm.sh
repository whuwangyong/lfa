#!/bin/bash
# create vm and start them
# requirement:
# 1. openvswitch br0 and vnet-port
# 2. VirtualBox and extpack installed

vboxmanage import host.ova
vboxmanage modifyvm host --name h1
vboxmanage import host.ova
vboxmanage modifyvm host --name h2

vboxmanage hostonlyif create

vboxmanage modifyvm h1 --nic2 bridged
vboxmanage modifyvm h1 --bridgeadapter2 vnet-br0-h1
vboxmanage modifyvm h1 --nic3 hostonly
vboxmanage modifyvm h1 --hostonlyadapter3 vboxnet0

vboxmanage modifyvm h2 --nic2 bridged
vboxmanage modifyvm h2 --bridgeadapter2 vnet-br0-h2
vboxmanage modifyvm h2 --nic3 hostonly
vboxmanage modifyvm h2 --hostonlyadapter3 vboxnet0

vboxmanage startvm h1 --type headless
vboxmanage startvm h2 --type headless
