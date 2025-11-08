# Cyber-MITM-Attack-Lab

This lab demonstrates low-level packet manipulation, local redirection with iptables, and HTTP traffic inspection using Scapy—core skills for understanding practical man-in-the-middle (MITM) techniques on plaintext HTTP.

> Transparency: The HTML demo pages (`index.html`, `all-in-one.html`) and some explanatory UI content were generated with AI assistance. The underlying lab source files (`sniffer1.py`, shell scripts, original README notes) remain authored manually and unchanged in intent.

This repository contains everything you need to run the lab. No additional files are required beyond what's in this repo.

## What's in this repository

- `sniffer1.py` – Scapy-based sniffer/forwarder that:
	- Listens for redirected outbound HTTP packets on port 8080
	- Prints `[HTTP] host/path` when it recognizes an HTTP request
	- Prints `[CENSORED]` and drops any request containing the keyword `frankenstein`
	- Forwards permitted traffic to real destination port 80 and logs "Your packet has been forwarded to port 80"
- `lab2setup.sh` – Adds iptables rules: DNAT outbound TCP dport 80 (non-root) to local :8080 and drops RST/RST,ACK packets to keep flows stable
- `lab2teardown.sh` – Removes the iptables rules added during setup
- `index.html` – A self-contained HTML demo that explains the lab, shows example output, and includes a small client-side simulation of the decision logic
- `all-in-one.html` – Consolidated page that displays the code, README content, and links to the PDFs in one place
- `README.md` – This detailed guide
- `ReadMe.txt` – A shorter, original readme for the lab
- `Lab2.pdf`, `Lab2_jpotapenko.pdf` – Lab handout/notes (viewable from the all-in-one page)

## Requirements

- Linux
- Python 3
- scapy (`pip3 install scapy`)
- iptables (run scripts with sudo/root)

## Quick start

0) Install dependencies (one time)

```bash
pip3 install scapy
```

1) Setup redirection rules

```bash
sudo ./lab2setup.sh
```

2) Run the sniffer

```bash
sudo python3 sniffer1.py
```

3) Generate HTTP traffic (e.g., using a non-root browser or `curl http://example.com/`), observe console logs, then stop with Ctrl+C.

4) Optional cleanup
## How to test (examples)

Run these in a separate, non-root terminal while the sniffer is running. Because the iptables rule excludes root, do not prefix with `sudo`.

Forwarded (no body → may show "No Payload Found"):

```bash
curl http://example.com/books
```

Forwarded (POST body allowed):

```bash
curl -X POST -d "q=hello" http://example.com/search
```

Censored (POST body contains the keyword):

```bash
curl -X POST -d "q=frankenstein" http://example.com/search
```

Expected console snippets:

```
[HTTP] example.com/books
Your packet has been forwarded to port 80

[HTTP] example.com/search
[CENSORED]
```

```bash
sudo ./lab2teardown.sh
```

## HTML demos

- Open `index.html` directly in your browser to read an overview and try the client-side simulation of the censor/forward logic.
- If you prefer a local server:

```bash
python3 -m http.server 8000
# then open http://localhost:8000/index.html
```

The demo includes a link back to the full source on GitHub so you can explore the code in context.

Also see the consolidated view at `all-in-one.html`, which shows the code, README content, and lab PDFs in one place. The top of that page includes tab-style buttons to switch between files without opening new pages.

## Notes

- Applies only to plaintext HTTP, not HTTPS/TLS.
- Simplistic keyword filter and no TCP stream reassembly (expects a request within a single packet for the demo).

## Troubleshooting

- No output? Ensure you're generating plaintext HTTP (port 80) and that the sniffer is running with `sudo`.
- Requests not redirected? Confirm iptables rules were applied (`sudo ./lab2setup.sh`) and that your test client is non-root.
- HTTPS pages won't show up here by design; use `http://` instead of `https://` for testing.
