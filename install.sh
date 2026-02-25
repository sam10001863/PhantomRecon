#!/bin/bash

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Setting CGO disabled..."
echo 'export CGO_ENABLED=0' >> ~/.profile
source ~/.profile

echo "Installing Go tools..."

go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest
go install github.com/projectdiscovery/naabu/v2/cmd/naabu@latest
go install github.com/lc/gau/v2/cmd/gau@latest
go install github.com/ffuf/ffuf/v2@v2.1.0
go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

echo "Installation Completed."
