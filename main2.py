# readable code?

import os
import sys
import socket
import argparse
try:
  import requests
except ModuleNotFoundError:
  sys.exit("Cuba \"pip install requests\" dan jalankan script lagi sekali.")
from concurrent.futures import ThreadPoolExecutor

banner = r'''
     _______. __    __  .______   ___   ___ 
    /       ||  |  |  | |   _  \  \  \ /  / 
   |   (----`|  |  |  | |  |_)  |  \  V  /  
    \   \    |  |  |  | |   _  <    >   <   
.----)   |   |  `--'  | |  |_)  |  /  .  \  
|_______/     \______/  |______/  /__/ \__\ 
                Author | Mika259
                     Github
'''

# Fungsi untuk memeriksa kewujudan subdomain melalui DNS
def check_subdomain(domain, subdomain):
    try:
        full_domain = f"{subdomain}.{domain}"
        ip = socket.gethostbyname(full_domain)
        print(f"  {full_domain} | {ip}")
        return full_domain, True
    except socket.gaierror:
        return subdomain, False

# Fungsi utama untuk memproses wordlist
def process_subdomain(domain, subdomains):
    print("Mula check...")
    try:
      socket.gethostbyname(domain)
      with ThreadPoolExecutor(max_workers=10) as executor:
          for subdomain, exists in executor.map(lambda sub: check_subdomain(domain, sub), subdomains):
              if exists:
                  check_subdomain(domain,subdomain)
    except socket.gaierror:
      sys.exit("domain seperti tidak wujud, cuba lagi nanti.")

# Fungsi utama program
def main():
    parser = argparse.ArgumentParser(description="Tool Subdomain Finder")
    parser.add_argument("domain", help="Nama domain untuk dicari (contoh: example.com)")
    parser.add_argument("wordlist", help="Fail wordlist untuk subdomain (contoh: subdomains.txt)")
    args = parser.parse_args()

    domain = args.domain
    wordlist_file = args.wordlist
    try:
        with open(wordlist_file, "r") as file:
            line_count = len(file.readlines())
            print(f"File list: {line_count} line of data")
    except FileNotFoundError:
            sys.exit(f"File \"{wordlist_file}\" tidak wujud!")

    # Baca wordlist
    try:
        with open(wordlist_file, "r") as file:
            subdomains = file.read().splitlines()
    except FileNotFoundError:
        print("[-] Wordlist tak wujud")
        return

    print(f"[*] Domain : {domain}")
    process_subdomain(domain, subdomains)

if __name__ == "__main__":
    try:
        clear = "clear" if os.name == "posix" else "cls";
        os.system(clear)
        print(banner)
        main()
    except KeyboardInterrupt:
        sys.exit("Keluar program.");
