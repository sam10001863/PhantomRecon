# 🚀 PhantomRecon

![Python](https://img.shields.io/badge/Python-3.x-green)
![Platform](https://img.shields.io/badge/Platform-Termux%20%7C%20Linux-brightgreen)
![License](https://img.shields.io/github/license/sam10001863/PhantomRecon)
![Repo Size](https://img.shields.io/github/repo-size/sam10001863/PhantomRecon)
![Stars](https://img.shields.io/github/stars/sam10001863/PhantomRecon?style=social)

> Android Professional Recon Engine  
> Developed by Samrat Kharat

---

## 🔍 Overview

PhantomRecon is a fully automated reconnaissance framework designed for:

- Bug Bounty Hunters  
- Security Researchers  
- Red Team Operators  
- Ethical Hackers  

It answers the common question:

**“What should I scan after subdomain enumeration?”**

PhantomRecon intelligently chains professional security tools into a structured workflow with automated reporting and risk scoring.

Optimized for Termux (Android) and Linux environments.

---

## ⚙️ Features

- Subdomain Enumeration (subfinder)
- DNS Resolution (dnsx)
- Live Host Detection (httpx)
- Port Scanning (Nmap)
- URL Collection (gau)
- Directory Bruteforce (ffuf)
- Vulnerability Scanning (nuclei)
- Sensitive File Detection
- Risk Exposure Scoring
- Timestamp-Based Output Isolation
- Ctrl+C Stage Skipping
- Interactive Tool Installation Prompts
- Termux Optimized

---

## 📦 Installation (Recommended for Termux)

### 1. Clone Repository

```bash
git clone https://github.com/sam10001863/PhantomRecon.git
cd PhantomRecon
```

### 2. Run Installer

```bash
chmod +x install.sh
./install.sh
```

### 3. Reload Environment

```bash
source ~/.bashrc
```

---

## ⚠️ Important Notes

- This tool uses ProjectDiscovery httpx (NOT the Python httpx package).
- Port scanning is handled by Nmap.
- If tools are not detected after installation, run:

```bash
source ~/.bashrc
```

---

## 🚀 Usage

### Basic Scan (Balanced Default)

```bash
python sam.py -d example.com
```

### Fast Mode

```bash
python sam.py -d example.com --fast
```

### Aggressive Mode

```bash
python sam.py -d example.com --aggressive
```

### Custom Wordlist

```bash
python sam.py -d example.com --wordlist wordlists/custom.txt
```

### Manual Override Example

```bash
python sam.py -d example.com --aggressive --threads 80 --severity critical
```

---

## 🧠 Scan Modes

| Mode | Description |
|------|------------|
| Default | Balanced reconnaissance |
| --fast | Quick lightweight scan |
| --aggressive | Deep full-scope scan |

Manual flags override mode defaults.

---

## 📁 Output Structure

Each scan is saved in a unique timestamped directory:

```
output/<domain>/<timestamp>/
```

Example:

```
output/example.com/20260226_113004/
├── subdomains.txt
├── resolved.txt
├── live.txt
├── live_hosts.txt
├── ports.txt
├── urls.txt
├── dirs.json
├── vulns.txt
```

---

## 📊 Risk Scoring System

PhantomRecon calculates exposure level based on:

- Number of subdomains
- Live hosts detected
- Open ports
- Vulnerabilities discovered
- Sensitive files exposed

Risk Levels:

- LOW
- MEDIUM
- HIGH

---

## 🖥 Example Final Output

```
PhantomRecon Final Report

Subdomains  : 187
Live Hosts  : 92
Open Ports  : 18
Vulnerabilities : 6
Sensitive Files : 1

Risk Score  : 7/10
Risk Level  : HIGH
```

---

## 🔐 Disclaimer

This tool is intended for authorized security testing and educational purposes only.

The author is not responsible for misuse or illegal activities.

Always obtain proper permission before scanning any target.

---

## 👨‍💻 Author

Samrat Kharat  
GitHub: https://github.com/sam10001863

---

## 📜 License

MIT License
