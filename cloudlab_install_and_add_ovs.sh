#!/bin/bash
echo Yong:1|sudo chpasswd
sudo apt-get update
sudo apt-get install -y openvswitch-switch vim
sudo ovs-vsctl add-br br0
sudo ovs-vsctl set-controller br0 tcp:155.98.39.124:6653
sudo ovs-vsctl set bridge br0 other-config:datapath-id=000000000000000$1;
