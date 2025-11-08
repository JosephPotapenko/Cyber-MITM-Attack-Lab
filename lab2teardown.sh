echo "Now that you have ended the program, the bash script will now delete the iptable changes we made."
echo "-"

sudo iptables -t nat -D OUTPUT -p tcp -m owner ! --uid-owner root --dport 80 -j DNAT --to :8080
sudo iptables -D OUTPUT -p tcp --tcp-flags ALL RST,ACK -j DROP
sudo iptables -D OUTPUT -p tcp --tcp-flags ALL RST -j DROP
sudo iptables -D INPUT -p tcp --tcp-flags ALL RST -j DROP
sudo iptables -D INPUT -p tcp --tcp-flags ALL RST,ACK -j DROP

echo "Thank-you for using our program!"

