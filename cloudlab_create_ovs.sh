#!/bin/bash
sudo ovs-vsctl add-br br0
sudo ovs-vsctl set-controller br0 tcp:155.98.39.124:6653
sudo ovs-vsctl set bridge br0 other-config:datapath-id=000000000000000$1;

function add_port()
{
	ovs=${1};
	node=${2};

	echo $ovs --tap port-- $node;
	port=vnet-${ovs}-${node};

	sudo ip tuntap add mode tap $port;
	sudo ip link set $port up;
	sudo ovs-vsctl add-port $ovs $port;
}

add_port br0 h1
add_port br0 h2
