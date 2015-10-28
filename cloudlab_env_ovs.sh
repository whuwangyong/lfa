#!/bin/bash
echo Yong:1|sudo chpasswd
echo 'deb http://download.virtualbox.org/virtualbox/debian trusty contrib' | sudo tee -a /etc/apt/sources.list
sudo apt-get update
sleep 60 # 1 min
sudo apt-get install -y vim openvswitch-switch virtualbox-5.0 dkms axel
sleep 120 # 2 min
sudo apt-get -f install
sleep 60 # 1 min
axel http://download.virtualbox.org/virtualbox/5.0.8/Oracle_VM_VirtualBox_Extension_Pack-5.0.8-103449.vbox-extpack
sleep 60 # 1 min
sudo vboxmanage extpack install Oracle_VM_VirtualBox_Extension_Pack-5.0.8-103449.vbox-extpack

