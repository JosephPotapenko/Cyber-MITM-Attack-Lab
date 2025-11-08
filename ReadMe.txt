Lab 2 - Scapy MITM (simple README)

This is a small lab project that intercepts local HTTP traffic, inspects requests, drops any request containing the word frankenstein (prints [CENSORED]), prints visited pages ([HTTP] host/path), and forwards everything else to port 80.

Files:

sniffer1.py - Scapy-based sniffer/forwarder
lab2setup.sh - bash file that sets up iptables
lab2teardown.sh - bash file that tears down iptables


Requirements:

Linux
Python 3
scapy (pip3 install scapy)
iptables (you’ll need sudo/root)

How to run:

Run these commands with sudo:

sudo ./lab2setup.sh
sudo python3 sniffer1.py

Use a non-root browser or curl to visit plain HTTP pages (not HTTPS).
Stop the sniffer with Ctrl+C; the script will then remove the iptables rules.
Then, traverse the links on 10.101.68.89/books

What you should see:


[HTTP] example.com/path
Your packet has been forwarded to port 80


If the request contains frankenstein:

[CENSORED]


If no payload could be extracted:

No Payload Found

Finally, run the last command:
sudo ./lab2teardown.sh









