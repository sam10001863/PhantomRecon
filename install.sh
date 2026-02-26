#!/data/data/com.termux/files/usr/bin/bash

echo "[*] Updating packages..."
pkg update -y
pkg upgrade -y

echo "[*] Installing dependencies..."
pkg install -y git curl wget python python-pip go nmap libpcap

echo "[*] Setting Go environment..."
echo 'export PATH=$PATH:$HOME/go/bin' >> ~/.bashrc
export PATH=$PATH:$HOME/go/bin

export CGO_ENABLED=0

echo "[*] Installing Go tools..."

go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
go install github.com/lc/gau/v2/cmd/gau@latest
go install github.com/ffuf/ffuf@latest
go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

echo "[*] Creating wordlists directory..."
mkdir -p wordlists

echo "[✓] Installation Complete"
echo "[!] Restart Termux or run: source ~/.bashrc"


