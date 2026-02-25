# PhantomRecon

> Android Professional Recon Engine  
> Developed by Samrat Kharat

---

## Overview

PhantomRecon is an automated reconnaissance framework built for security researchers, bug bounty hunters, and red team operators.

It solves the common problem:

"What should I scan after subdomain enumeration?"

PhantomRecon intelligently chains professional security tools into a structured, automated reconnaissance workflow with clean CLI output and risk scoring.

Optimized for Termux (Android) and Linux environments.

---

## Features

- Subdomain Enumeration (subfinder)
- DNS Resolution (dnsx)
- Live Host Detection (httpx)
- Port Scanning (naabu)
- URL Collection (gau)
- Vulnerability Scanning (nuclei)
- Mode-Based Scanning (Fast / Aggressive / Balanced)
- Manual Argument Override
- Interactive Tool Installation
- Risk Scoring Engine
- Clean Animated CLI Interface
- Mobile Optimized (Termux Ready)

---

## Installation

### 1. Update Termux

```bash
pkg update && pkg upgrade -y
pkg install python golang git -y
```

### 2. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/PhantomRecon.git
cd PhantomRecon
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Required Go Tools

Make sure CGO is disabled:

```bash
export CGO_ENABLED=0
```

Install tools:

```bash
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest
go install github.com/projectdiscovery/naabu/v2/cmd/naabu@latest
go install github.com/lc/gau/v2/cmd/gau@latest
go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
```

Add Go to PATH permanently:

```bash
echo 'export PATH=$PATH:$HOME/go/bin' >> ~/.profile
source ~/.profile
```

---

## Usage

### Basic Scan (Balanced Default)

```bash
python phantomrecon.py -d example.com
```

### Fast Mode

```bash
python phantomrecon.py -d example.com --fast
```

### Aggressive Mode

```bash
python phantomrecon.py -d example.com --aggressive
```

### Manual Override Example

```bash
python phantomrecon.py -d example.com --aggressive --ports top --threads 80 --severity critical
```

---

## Scan Modes

| Mode | Description |
|------|------------|
| Default | Balanced scan |
| --fast | Lightweight quick recon |
| --aggressive | Deep full-scope scan |
| --stealth | Low-rate scanning |

Manual flags override mode defaults.

---

## Output Structure

All scan results are saved inside:

```
output/<target_domain>/
```

Example:

```
output/example.com/
│
├── subdomains.txt
├── resolved.txt
├── live.txt
├── ports.txt
├── urls.txt
└── vulns.txt
```

---

## Risk Scoring

PhantomRecon calculates exposure level based on:

- Number of subdomains
- Live hosts detected
- Open ports
- Vulnerabilities discovered

Risk Levels:

- LOW
- MEDIUM
- HIGH

---

## Example Final Output

```
PhantomRecon Final Report

Subdomains  : 187
Live Hosts  : 92
Open Ports  : 18
Vulnerabilities : 6

Risk Score  : 7/10
Risk Level  : HIGH
```

---

## Disclaimer

This tool is intended for authorized security testing and educational purposes only.

The author is not responsible for misuse or illegal activities.

Always obtain proper permission before scanning any target.

---

## Author

Samrat Kharat

---

## Roadmap

- HTML Reporting
- JSON Export
- Service-Aware Scanning
- Resume Sessions
- CVE Enrichment
- Parallel Execution Engine

---

## License

MIT License

