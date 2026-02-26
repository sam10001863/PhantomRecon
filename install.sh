#!/data/data/com.termux/files/usr/bin/bash

echo "[*] Updating packages..."
pkg update -y && pkg upgrade -y

echo "[*] Installing base dependencies..."
pkg install -y git curl wget python python-pip golang nmap libpcap

echo "[*] Installing Python dependencies..."
pip install rich pyfiglet

echo "[*] Setting Go environment..."

# Disable CGO for Termux compatibility
export CGO_ENABLED=0

# Add Go bin to PATH permanently if not already
if ! grep -q "go/bin" ~/.profile; then
    echo 'export PATH=$PATH:$HOME/go/bin' >> ~/.profile
fi

export PATH=$PATH:$HOME/go/bin

echo "[*] Checking Go installation..."
go version

echo "[*] Installing ProjectDiscovery tools via Go (Android-safe builds)..."

go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
go install github.com/lc/gau/v2/cmd/gau@latest
go install github.com/ffuf/ffuf/v2@latest

echo "[*] Refreshing shell..."
source ~/.profile
hash -r

echo "[*] Verifying installation..."

subfinder -version
dnsx -version
httpx -version
nuclei -version
ffuf -V
gau --version

echo "[*] Creating wordlists directory..."
mkdir -p wordlists

echo "[✓] Installation Complete"
echo "[!] Restart Termux or run: source ~/.profile"
