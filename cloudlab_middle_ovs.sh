#!/bin/bash
echo Yong:1|sudo chpasswd
if [ -z "$1" ]
then
	echo "need an argument as a part of ovs dpid\n"
	echo "such as 01,09,0a,11"
	exit
fi
sudo apt-get update -q=2
sudo apt-get install -y vim openvswitch-switch

sudo ovs-vsctl add-br br0
sudo ovs-vsctl set bridge br0 other-config:datapath-id=00aa00bb00cc00$1;
sudo ovs-vsctl set-controller br0 tcp:155.98.39.124:6653
echo "*********************************"
sudo ovs-vsctl show
echo "*********************************"
sudo ovs-ofctl show br0
echo "*********************************"

