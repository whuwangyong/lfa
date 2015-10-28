#!/bin/bash
echo Yong:1|sudo chpasswd
echo 'deb http://download.virtualbox.org/virtualbox/debian trusty contrib' | sudo tee /etc/apt/sources.list
sudo apt-get update
sudo apt-get install -y vim openvswitch-switch virtualbox-5.0 dkms axel
sudo apt-get -f install
axel http://download.virtualbox.org/virtualbox/5.0.8/Oracle_VM_VirtualBox_Extension_Pack-5.0.8-103449.vbox-extpack
sudo vboxmanage extpack install Oracle_VM_VirtualBox_Extension_Pack-5.0.8-103449.vbox-extpack

