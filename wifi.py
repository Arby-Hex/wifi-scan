# WiFi ScanX Dominator MAX Edition™
import os
import subprocess
import time
import shutil
import json
import math
import random
import urllib.request
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.progress import track
from rich.text import Text
from rich import print

console = Console()

QUOTES = [
    "💻 'Keren Kan Cui Wkwk, Auto Berasa Jadi Hacker Dah.'",
    "🛰️ 'Jika Temanmu Gila Cewe, Maka Kamu Gila Dalam Kode.'",
    "🔒 'Wifi Dienkripsi? Bukan Penghalang Bagi Tool Ini😈.'",
    "🧠 'Peretas melihat pola sedangkan yang lain melihat gangguan.'",
    "🎯 'Jadilah tak terlihat. Ketahui segalanya. Serang dengan tepat.'"
]

CONFIG_PATH = "config.json"

def auto_install():
    pkgs = ['figlet', 'termux-api', 'lolcat']
    for pkg in pkgs:
        if shutil.which(pkg) is None:
            console.print(f"[yellow]➤ Menginstall [bold]{pkg}[/bold]...[/yellow]")
            os.system(f"pkg install {pkg} -y > /dev/null 2>&1")
    try:
        import rich
    except ImportError:
        console.print("[yellow]➤ Menginstall modul [bold]rich[/bold]...[/yellow]")
        os.system("pip install rich")

def waktu_scan():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_public_ip():
    try:
        return urllib.request.urlopen("https://api.ipify.org").read().decode()
    except:
        return "Tidak tersedia 🌐"

def get_current_connection():
    try:
        info = subprocess.check_output(['termux-wifi-connectioninfo']).decode()
        data = json.loads(info)
        ssid = data.get("ssid", "<unknown>")
        ip = data.get("ip", "0.0.0.0")
        return f"[green]✔ Terhubung ke:[/green] [bold]{ssid}[/bold] | IP: {ip}"
    except:
        return "[red]✘ Tidak dapat mendeteksi koneksi aktif[/red]"

def get_wifi_info():
    try:
        result = subprocess.check_output(['termux-wifi-scaninfo']).decode()
        return json.loads(result)
    except Exception as e:
        console.print(f"[red]Gagal mengambil info WiFi: {e}[/red]")
        return []

def estimasi_jarak(freq, level):
    try:
        exp = (27.55 - (20 * math.log10(freq)) + abs(level)) / 20.0
        return round(pow(10, exp), 1)
    except:
        return "?"

def sinyal_bar(level):
    if level == -999:
        return "[dim]Unknown[/dim]"
    bar = "█" * max(1, int((level + 100) / 5))
    return f"{level} dBm {bar}"

def sinyal_emoji(level):
    if level >= -60:
        return f"{level} dBm 🟢"
    elif level >= -75:
        return f"{level} dBm 🟡"
    else:
        return f"{level} dBm 🔴"

def keamanan_keterangan(cap):
    if "WPA2" in cap or "WPA" in cap:
        return "WPA/WPA2 🔐"
    elif "WEP" in cap:
        return "WEP 🟠"
    elif "ESS" in cap:
        return "Open 🔓"
    return "❔ Tidak Diketahui"

def deteksi_channel(freq):
    if 2412 <= freq <= 2484:
        return "2.4GHz 📶"
    elif 5170 <= freq <= 5825:
        return "5GHz 🚀"
    else:
        return "❔"

def loading_bar():
    console.print("\n[cyan]🛸 [bold]Mendapatkan Lalu Lintas Jaringan...[/bold][/cyan]\n")
    for _ in track(range(30), description="[bold green]Memindai jaringan...[/bold green]"):
        time.sleep(0.02)

def banner():
    os.system("clear")
    os.system("figlet Wifi ScanX | lolcat")
    console.print("[bold magenta]Daemonium - Wifi ScanX\nAuthor : 🐉 Arby-Hex 🐉\n[/bold magenta]")

def simpan_config():
    config = {"last_scan": waktu_scan()}
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f)

def export_data(wifi_list):
    waktu = datetime.now().strftime("%Y%m%d_%H%M%S")
    txt_file = f"scan_report_{waktu}.txt"
    json_file = f"scan_report_{waktu}.json"
    with open(txt_file, "w") as txt, open(json_file, "w") as js:
        for w in wifi_list:
            txt.write(json.dumps(w, indent=2) + "\n")
        json.dump(wifi_list, js, indent=2)
    console.print(f"\n[green]✅ Export selesai:[/green] [bold]{txt_file}[/bold], [bold]{json_file}[/bold]")

def wifi_scanx(refresh=False):
    auto_install()
    simpan_config()
    while True:
        banner()
        console.print(f"[bold cyan]🌐 IP Publik:[/bold cyan] {get_public_ip()}")
        console.print(f"[bold magenta]🕒 Waktu Scan:[/bold magenta] {waktu_scan()}")
        console.print(get_current_connection())

        loading_bar()
        wifi_list = get_wifi_info()
        if not wifi_list:
            console.print("[red]❌ Tidak ada jaringan terdeteksi.[/red]")
        else:
            sorted_wifi = sorted(wifi_list, key=lambda x: x.get("level", -999), reverse=True)
            for i, wifi in enumerate(sorted_wifi, 1):
                ssid = wifi.get("ssid", "<Hidden>")
                bssid = wifi.get("bssid", "❔")
                freq = wifi.get("frequency", 0)
                level = wifi.get("level", -999)
                cap = wifi.get("capabilities", "")
                channel = deteksi_channel(freq)
                level_str = sinyal_emoji(level) if level != -999 else "❔"
                bar = sinyal_bar(level)
                jarak = estimasi_jarak(freq, level) if freq and level != -999 else "❔"
                keamanan = keamanan_keterangan(cap)

                content = f"""[bold cyan]SSID:[/bold cyan] {ssid}
[bold green]BSSID:[/bold green] {bssid}
[bold blue]Frekuensi:[/bold blue] {freq} MHz ({channel})
[bold yellow]Sinyal:[/bold yellow] {bar}
[bold red]Keamanan:[/bold red] {keamanan}
[bold white]Estimasi Jarak:[/bold white] {jarak} m
[dim]Target #{i}[/dim]
"""
                panel = Panel.fit(content, title=f"[bold green]📶 WiFi #{i}[/bold green]", border_style="cyan")
                console.print(panel)
                time.sleep(0.15)

        console.print("\n[bold cyan]" + random.choice(QUOTES) + "[/bold cyan]")

        console.print("\n[bold magenta]➤ Pilihan:[/bold magenta] [green][E][/green]xport, [yellow][R][/yellow]escan, [red][Q][/red]uit")
        inp = input(">> ").lower()
        if inp == "e":
            export_data(wifi_list)
        elif inp == "r":
            continue
        elif inp == "q":
            break
        else:
            break

if __name__ == "__main__":
    wifi_scanx(refresh=False)
