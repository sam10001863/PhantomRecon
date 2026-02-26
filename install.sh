#!/data/data/com.termux/files/usr/bin/bash

echo "[*] Updating packages..."
pkg update -y && pkg upgrade -y

echo "[*] Installing base dependencies..."
pkg install -y git curl wget unzip python python-pip golang nmap libpcap

echo "[*] Installing Python dependencies..."
pip install --upgrade rich pyfiglet

echo "[*] Setting Go environment..."
export CGO_ENABLED=0
echo 'export PATH=$PATH:$HOME/go/bin' >> ~/.bashrc
echo 'export CGO_ENABLED=0' >> ~/.bashrc
source ~/.bashrc

echo "[*] Cleaning Go cache..."
go clean -modcache

echo "[*] Installing ProjectDiscovery tools via Go..."

# Subfinder
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

# Dnsx
go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest

# Httpx
go install github.com/projectdiscovery/httpx/cmd/httpx@latest

# Gau (v2 module path)
go install github.com/lc/gau/v2/cmd/gau@latest

# FFUF (correct v2 module path)
go install github.com/ffuf/ffuf/v2@latest

echo "[*] Installing nuclei (ARM64 stable method)..."

NUCLEI_URL=$(curl -s https://api.github.com/repos/projectdiscovery/nuclei/releases/latest \
  | grep browser_download_url \
  | grep linux_arm64.zip \
  | cut -d '"' -f 4)

curl -L -o nuclei.zip "$NUCLEI_URL"

if [ -f nuclei.zip ]; then
    unzip -o nuclei.zip
    chmod +x nuclei
    mv nuclei $PREFIX/bin/
    rm nuclei.zip
    echo "[✓] nuclei installed successfully"
else
    echo "[!] nuclei download failed"
fi

echo "[*] Creating wordlists directory..."
mkdir -p wordlists

echo "[✓] Installation Complete"
echo "[!] Restart Termux or run: source ~/.bashrc"
