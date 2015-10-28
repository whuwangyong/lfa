#!/bin/bash
echo Yong:1|sudo chpasswd
sudo apt-get update
sleep 60 # 1min
sudo apt-get install -y vim openjdk-7-jdk ant axel
sleep 120 #2 min
git clone https://github.com/floodlight/floodlight.git
sleep 60
cd floodlight
ant
sleep 120 #2 min
sudo java -jar target/floodlight.jar
