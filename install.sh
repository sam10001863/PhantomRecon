#!/data/data/com.termux/files/usr/bin/bash

echo "[*] Updating packages..."
pkg update -y && pkg upgrade -y

echo "[*] Installing base dependencies..."
pkg install -y git curl wget unzip python python-pip nmap libpcap

echo "[*] Installing Python dependencies..."
pip install rich pyfiglet

INSTALL_DIR=$PREFIX/bin
TMP_DIR=$HOME/.phantom_tmp

mkdir -p $TMP_DIR
cd $TMP_DIR

echo "[*] Installing Subfinder..."
wget https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_arm64.zip
unzip subfinder_2.6.6_linux_arm64.zip
chmod +x subfinder
mv subfinder $INSTALL_DIR/

echo "[*] Installing Dnsx..."
wget https://github.com/projectdiscovery/dnsx/releases/download/v1.2.0/dnsx_1.2.0_linux_arm64.zip
unzip dnsx_1.2.0_linux_arm64.zip
chmod +x dnsx
mv dnsx $INSTALL_DIR/

echo "[*] Installing Httpx..."
wget https://github.com/projectdiscovery/httpx/releases/download/v1.6.6/httpx_1.6.6_linux_arm64.zip
unzip httpx_1.6.6_linux_arm64.zip
chmod +x httpx
mv httpx $INSTALL_DIR/

echo "[*] Installing Nuclei..."
wget https://github.com/projectdiscovery/nuclei/releases/download/v3.2.4/nuclei_3.2.4_linux_arm64.zip
unzip nuclei_3.2.4_linux_arm64.zip
chmod +x nuclei
mv nuclei $INSTALL_DIR/

echo "[*] Installing Gau..."
wget https://github.com/lc/gau/releases/download/v2.2.4/gau_2.2.4_linux_arm64.tar.gz
tar -xzf gau_2.2.4_linux_arm64.tar.gz
chmod +x gau
mv gau $INSTALL_DIR/

echo "[*] Installing FFUF..."
wget https://github.com/ffuf/ffuf/releases/download/v2.1.0/ffuf_2.1.0_linux_arm64.tar.gz
tar -xzf ffuf_2.1.0_linux_arm64.tar.gz
chmod +x ffuf
mv ffuf $INSTALL_DIR/

cd $HOME
rm -rf $TMP_DIR

echo "[*] Creating wordlists directory..."
mkdir -p wordlists

echo "[✓] Installation Complete"
