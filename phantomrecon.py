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
    console.print("[green]Android Professional Recon Engine v5.0[/green]")
    console.print("[green]Developed by Samrat Kharat[/green]\n")


# ===================== TOOL CHECK =====================

def check_tool(tool):
    return subprocess.call(f"which {tool}", shell=True,
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL) == 0


def ensure_tool(tool, install_cmd):
    if check_tool(tool):
        console.print(f"[green][+] {tool} OK[/green]")
        return True

    console.print(f"[yellow][!] {tool} not installed.[/yellow]")
    choice = input(f"Install {tool}? (y/n): ").strip().lower()

    if choice == "y":
        subprocess.run(install_cmd, shell=True)
        return check_tool(tool)
    return False


# ===================== PROGRESS WRAPPER =====================

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

        while process.poll() is None:
            if progress.tasks[0].completed < 95:
                progress.update(task, advance=2)
            time.sleep(0.2)

        progress.update(task, completed=100)

    console.print(f"[green][✓] {title} Completed[/green]\n")


# ===================== COUNT LINES =====================

def count_lines(file):
    if not os.path.exists(file):
        return 0
    with open(file) as f:
        return len([line for line in f if line.strip()])


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
    parser.add_argument("--fast", action="store_true")
    parser.add_argument("--aggressive", action="store_true")
    parser.add_argument("--threads", type=int)
    parser.add_argument("--severity")

    args = parser.parse_args()
    banner()

    domain = args.domain
    base_path = f"output/{domain}"
    os.makedirs(base_path, exist_ok=True)

    # ===== Mode Defaults =====

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

    # ===== Tool Checks =====

    subfinder_ok = ensure_tool("subfinder",
                               "export CGO_ENABLED=0 && go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest")

    dnsx_ok = ensure_tool("dnsx",
                          "export CGO_ENABLED=0 && go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest")

    httpx_ok = ensure_tool("httpx",
                           "export CGO_ENABLED=0 && go install github.com/projectdiscovery/httpx/cmd/httpx@latest")

    naabu_ok = ensure_tool("naabu",
                           "export CGO_ENABLED=0 && go install github.com/projectdiscovery/naabu/v2/cmd/naabu@latest")

    gau_ok = ensure_tool("gau",
                         "export CGO_ENABLED=0 && go install github.com/lc/gau/v2/cmd/gau@latest")

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

    if naabu_ok:
        if port_mode == "full":
            cmd = f"naabu -l {base_path}/live.txt -p - -rate {threads} -o {base_path}/ports.txt"
        else:
            cmd = f"naabu -l {base_path}/live.txt -top-ports 1000 -rate {threads} -o {base_path}/ports.txt"

        run_with_progress(cmd, "Port Scanning")

    if gau_ok:
        run_with_progress(
            f"gau {domain} > {base_path}/urls.txt",
            "URL Collection"
        )

    if nuclei_ok:
        run_with_progress(
            f"nuclei -l {base_path}/live.txt -severity {severity} -o {base_path}/vulns.txt",
            "Vulnerability Scanning"
        )

    # ===== Summary =====

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
    console.print(f"[green]Vulnerabilities : {vulns}[/green]\n")

    console.print(f"[green]Risk Score  : {score}/10[/green]")
    console.print(f"[green]Risk Level  : {level}[/green]")
    console.print(f"[green]Output Path : {base_path}[/green]")
    console.print("[green]\n[✓] Recon Completed Successfully[/green]")


if __name__ == "__main__":
    main()
