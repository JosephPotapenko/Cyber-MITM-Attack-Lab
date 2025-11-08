#!/bin/bash

echo "Welcome to the program!"
echo "First, the code will setup the iptables, and drop RST packets."
echo "-"

sudo iptables -t nat -A OUTPUT -p tcp -m owner ! --uid-owner root --dport 80 -j DNAT --to :8080
sudo iptables -I OUTPUT -p tcp --tcp-flags ALL RST,ACK -j DROP
sudo iptables -I OUTPUT -p tcp --tcp-flags ALL RST -j DROP
sudo iptables -I INPUT -p tcp --tcp-flags ALL RST -j DROP
sudo iptables -I INPUT -p tcp --tcp-flags ALL RST,ACK -j DROP

echo "Now, run sniffer1.py"


