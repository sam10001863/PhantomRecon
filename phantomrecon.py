#!/usr/bin/env python3

import os
import argparse
import subprocess
import time
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
import pyfiglet

console = Console()

# ===================== BANNER =====================

def banner():
    ascii_banner = pyfiglet.figlet_format("PhantomRecon", font="slant")
    console.print(f"[green]{ascii_banner}[/green]")
    console.print("[green]Android Professional Recon Engine v6.0[/green]")
    console.print("[green]Developed by Samrat Kharat[/green]\n")


# ===================== TOOL CHECK =====================

def check_tool(tool):
    return subprocess.call(
        f"which {tool}",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    ) == 0


def ensure_tool(tool, install_cmd):
    if check_tool(tool):
        console.print(f"[green][+] {tool} OK[/green]")
        return True

    console.print(f"[yellow][!] {tool} not installed.[/yellow]")
    choice = input(f"Install {tool}? (y/n): ").strip().lower()

    if choice == "y":
        subprocess.run(install_cmd, shell=True)
        return check_tool(tool)

    console.print(f"[red]Skipping {tool} stage[/red]")
    return False


# ===================== PROGRESS RUNNER =====================

def run_with_progress(cmd, title):
    console.print(f"[green][*] {title}[/green]")

    with Progress(
        SpinnerColumn(),
        TextColumn("[green]{task.description}[/green]"),
        BarColumn(),
        TextColumn("{task.percentage:>3.0f}%"),
        console=console
    ) as progress:

        task = progress.add_task(title, total=100)
        process = subprocess.Popen(cmd, shell=True)

        try:
            while process.poll() is None:
                if progress.tasks[0].completed < 95:
                    progress.update(task, advance=2)
                time.sleep(0.2)

        except KeyboardInterrupt:
            console.print(f"\n[red][!] {title} Skipped by User[/red]")
            process.terminate()
            time.sleep(1)
            if process.poll() is None:
                process.kill()
            console.print(f"[yellow][→] Moving to Next Stage[/yellow]\n")
            return

        progress.update(task, completed=100)

    console.print(f"[green][✓] {title} Completed[/green]\n")


# ===================== COUNT LINES =====================

def count_lines(file):
    if not os.path.exists(file):
        return 0
    with open(file) as f:
        return len([line for line in f if line.strip()])


# ===================== SENSITIVE FILE CHECK =====================

def sensitive_check(domain):
    sensitive_files = [
        ".env",
        ".git/config",
        "backup.zip",
        "config.php",
        "wp-config.php"
    ]

    exposed = []

    console.print("[green][*] Sensitive File Check[/green]")

    for file in sensitive_files:
        try:
            status = subprocess.check_output(
                f"curl -s -o /dev/null -w '%{{http_code}}' https://{domain}/{file}",
                shell=True
            ).decode().strip()

            if status == "200":
                exposed.append(file)
                console.print(f"[red][!] Exposed: {file}[/red]")

        except:
            pass

    if not exposed:
        console.print("[green][✓] No Sensitive Files Exposed[/green]\n")

    return len(exposed)


# ===================== RISK SCORING =====================

def risk_score(subs, live, ports, vulns):
    score = 0
    if subs > 50: score += 1
    if live > 20: score += 2
    if ports > 10: score += 2
    if vulns > 0: score += 3

    if score <= 3:
        level = "LOW"
    elif score <= 6:
        level = "MEDIUM"
    else:
        level = "HIGH"

    return score, level


# ===================== MAIN =====================

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--domain", required=True)
    parser.add_argument("--wordlist", help="Custom wordlist for directory bruteforce")
    parser.add_argument("--fast", action="store_true")
    parser.add_argument("--aggressive", action="store_true")
    parser.add_argument("--threads", type=int)
    parser.add_argument("--severity")

    args = parser.parse_args()
    banner()

    domain = args.domain

    default_wordlist = "wordlists/common.txt"
    wordlist = args.wordlist if args.wordlist else default_wordlist

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    base_path = f"output/{domain}/{timestamp}"
    os.makedirs(base_path, exist_ok=True)

    port_mode = "top"
    severity = "medium,high"
    threads = 50

    if args.fast:
        threads = 30
        severity = "high"

    if args.aggressive:
        port_mode = "full"
        threads = 100
        severity = "low,medium,high,critical"

    if args.threads:
        threads = args.threads

    if args.severity:
        severity = args.severity

    console.print(f"[green]Threads: {threads} | Severity: {severity} | Port Mode: {port_mode}[/green]\n")

    subfinder_ok = ensure_tool("subfinder",
                               "export CGO_ENABLED=0 && go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest")

    dnsx_ok = ensure_tool("dnsx",
                          "export CGO_ENABLED=0 && go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest")

    httpx_ok = ensure_tool("httpx",
                           "export CGO_ENABLED=0 && go install github.com/projectdiscovery/httpx/cmd/httpx@latest")

    nmap_ok = ensure_tool("nmap", "pkg install nmap")

    gau_ok = ensure_tool("gau",
                         "export CGO_ENABLED=0 && go install github.com/lc/gau/v2/cmd/gau@latest")

    ffuf_ok = ensure_tool("ffuf",
                          "export CGO_ENABLED=0 && go install github.com/ffuf/ffuf@latest")

    nuclei_ok = ensure_tool("nuclei",
                            "export CGO_ENABLED=0 && go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest")

    console.print("\n[green][*] Starting Recon Workflow[/green]\n")

    if subfinder_ok:
        run_with_progress(
            f"subfinder -d {domain} -silent -o {base_path}/subdomains.txt",
            "Subdomain Enumeration"
        )

    if dnsx_ok:
        run_with_progress(
            f"dnsx -l {base_path}/subdomains.txt -silent -o {base_path}/resolved.txt",
            "DNS Resolution"
        )

    if httpx_ok:
        run_with_progress(
            f"httpx -l {base_path}/resolved.txt -silent -o {base_path}/live.txt",
            "Live Host Detection"
        )

    # ===== FIXED NMAP SECTION =====
    if nmap_ok:

        cleaned_hosts = f"{base_path}/live_hosts.txt"
        subprocess.run(
            f"cat {base_path}/live.txt | sed 's|http://||;s|https://||' > {cleaned_hosts}",
            shell=True
        )

        if port_mode == "full":
            cmd = f"nmap -iL {cleaned_hosts} -p- -T4 -oN {base_path}/ports.txt"
        else:
            cmd = f"nmap -iL {cleaned_hosts} --top-ports 1000 -T4 -oN {base_path}/ports.txt"

        run_with_progress(cmd, "Port Scanning")

    if gau_ok:
        run_with_progress(
            f"gau {domain} > {base_path}/urls.txt",
            "URL Collection"
        )

    if ffuf_ok:
        run_with_progress(
            f"ffuf -u https://{domain}/FUZZ -w {wordlist} -t {threads} -mc 200 -o {base_path}/dirs.json",
            "Directory Bruteforce"
        )

    if nuclei_ok:
        run_with_progress(
            f"nuclei -l {base_path}/live.txt -severity {severity} -o {base_path}/vulns.txt",
            "Vulnerability Scanning"
        )

    sensitive_count = sensitive_check(domain)

    subs = count_lines(f"{base_path}/subdomains.txt")
    live = count_lines(f"{base_path}/live.txt")
    ports = count_lines(f"{base_path}/ports.txt")
    vulns = count_lines(f"{base_path}/vulns.txt")

    score, level = risk_score(subs, live, ports, vulns)

    console.print("\n[green]==============================[/green]")
    console.print("[green]PhantomRecon Final Report[/green]")
    console.print("[green]==============================[/green]\n")

    console.print(f"[green]Subdomains  : {subs}[/green]")
    console.print(f"[green]Live Hosts  : {live}[/green]")
    console.print(f"[green]Open Ports  : {ports}[/green]")
    console.print(f"[green]Vulnerabilities : {vulns}[/green]")
    console.print(f"[green]Sensitive Files : {sensitive_count}[/green]\n")

    console.print(f"[green]Risk Score  : {score}/10[/green]")
    console.print(f"[green]Risk Level  : {level}[/green]")
    console.print(f"[green]Output Path : {base_path}[/green]")
    console.print("[green]\n[✓] Recon Completed Successfully[/green]")


if __name__ == "__main__":
    main()


