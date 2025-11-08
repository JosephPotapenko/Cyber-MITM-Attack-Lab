#!/usr/bin/env python3
from scapy.all import *

CENSOR = b"frankenstein"

def http_info(data):
    if not data: 
        return None
    if not data.startswith((b"GET", b"POST", b"HEAD", b"PUT", b"DELETE", b"OPTIONS")):
        return None
    try:
        first, rest = data.split(b"\r\n", 1)
    except ValueError:
        first = data
        rest = b""
    parts = first.split()
    path = parts[1].decode(errors="ignore") if len(parts) > 1 else "/"
    host = "unknown"
    for line in rest.split(b"\r\n"):
        if line.lower().startswith(b"host:"):
            host = line.split(b":", 1)[1].strip().decode(errors="ignore")
    return (host, path)

def get_payload(pkt):
    if not (IP in pkt and TCP in pkt):
        return b""

    # start from IP layer and walk the payload chain
    layer = pkt[IP]
    while hasattr(layer, "payload") and type(layer.payload) is not NoPayload:
        layer = layer.payload

    if hasattr(layer, "load"):
        return layer.load
    return b""

def packet_sniffer(pkt):
    if not (IP in pkt and TCP in pkt):
        print("No payload")
        return

    # only handle packets going to port 8080
    if pkt[TCP].dport != 8080:
        return

    payload = get_payload(pkt)

    info = http_info(payload)
    if info:
        host, path = info
        print(f"[HTTP] {host}{path}")

    if CENSOR in payload:
        print("[CENSORED]")
        return

    ip = pkt[IP]
    tcp = pkt[TCP]
    new_pkt = IP(src=ip.src, dst=ip.dst, ttl=ip.ttl, tos=ip.tos)/TCP(
        sport=tcp.sport, dport=80, seq=tcp.seq, ack=tcp.ack,
        flags=tcp.flags, window=tcp.window, options=tcp.options)

    if payload:
        new_pkt = new_pkt/payload

    del new_pkt[IP].chksum
    del new_pkt[TCP].chksum
    send(new_pkt, verbose=0)
    print("Your packet has been forwarded to port 80")

if __name__ == "__main__":
    print("The packet sniffer is starting now. Type Ctrl+C to stop sniffing:")
    try:
        sniff(prn=packet_sniffer, filter="tcp and port 8080", store=0)
    except KeyboardInterrupt:
        print("Stopped.")

