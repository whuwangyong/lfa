#!/bin/bash
echo Yong:1|sudo chpasswd
sudo apt-get update
sudo apt-get install -y vim openvswitch-switch dkms axel
axel http://download.virtualbox.org/virtualbox/5.0.8/virtualbox-5.0_5.0.8-103449~Ubuntu~precise_amd64.deb
sudo dpkg -i virtualbox-5.0_5.0.8-103449~Ubuntu~precise_amd64.deb
sudo apt-get -f install
axel http://download.virtualbox.org/virtualbox/5.0.8/Oracle_VM_VirtualBox_Extension_Pack-5.0.8-103449.vbox-extpack
sudo vboxmanage extpack install Oracle_VM_VirtualBox_Extension_Pack-5.0.8-103449.vbox-extpack

