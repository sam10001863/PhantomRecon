# PhantomRecon

![Python](https://img.shields.io/badge/Python-3.x-green)
![Platform](https://img.shields.io/badge/Platform-Termux%20%7C%20Linux-brightgreen)
![License](https://img.shields.io/github/license/sam10001863/PhantomRecon)
![Repo Size](https://img.shields.io/github/repo-size/sam10001863/PhantomRecon)
![Stars](https://img.shields.io/github/stars/sam10001863/PhantomRecon?style=social)

> Android Professional Recon Engine  
> Developed by Samrat Kharat  

---

## Overview

PhantomRecon is an automated reconnaissance framework built for:

- Security Researchers  
- Bug Bounty Hunters  
- Red Team Operators  

It solves a common problem:

**"What should I scan after subdomain enumeration?"**

PhantomRecon intelligently chains professional security tools into a structured reconnaissance workflow with:

- Mode-based scanning  
- Manual argument override  
- Interactive tool installation  
- Risk scoring engine  
- Clean animated CLI interface  
- Mobile optimization (Termux ready)  

---

## Features

- Subdomain Enumeration (subfinder)  
- DNS Resolution (dnsx)  
- Live Host Detection (httpx)  
- Port Scanning (nmap)  
- URL Collection (gau)  
- Directory Bruteforce (ffuf)  
- Vulnerability Scanning (nuclei)  
- Risk Exposure Scoring  
- Mode-Based Scanning (Fast / Aggressive / Balanced)  
- Manual Overrides  
- Interactive Tool Checks  
- Professional CLI Output  

---

## Installation (Termux)

### 1. Update & Install Base Dependencies

```bash
pkg update && pkg upgrade -y
pkg install git curl wget unzip python python-pip nmap libpcap -y
```

### 2. Clone Repository

```bash
git clone https://github.com/sam10001863/PhantomRecon.git
cd PhantomRecon
```

### 3. Run Installer (Recommended)

```bash
chmod +x install.sh
bash install.sh
```

This installer automatically installs:

- subfinder  
- dnsx  
- httpx  
- nuclei  
- gau  
- ffuf  
- nmap  


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
python phantomrecon.py -d example.com --aggressive --threads 80 --severity critical
```

---

## Scan Modes

| Mode | Description |
|------|------------|
| Default | Balanced scan |
| --fast | Quick lightweight recon |
| --aggressive | Deep full-scope scan |

Manual flags override mode defaults.

---

## Output Structure

All results are saved inside:

```
output/<target_domain>/<timestamp>/
```

Example:

```
output/example.com/
├── subdomains.txt
├── resolved.txt
├── live.txt
├── ports.txt
├── urls.txt
├── dirs.json
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
GitHub: https://github.com/sam10001863  

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
