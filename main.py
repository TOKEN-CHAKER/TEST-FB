import requests
from bs4 import BeautifulSoup
import os
import re
import time

def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*60)
    print("       PHONE NUMBER TO GMAIL FINDER - by Broken Nadeem")
    print("="*60)

def find_gmails_by_phone(phone_number):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    query = f'"{phone_number}" "@gmail.com"'
    url = f"https://www.google.com/search?q={query}"

    print(f"\n[*] Searching for Gmail accounts linked to: {phone_number}")
    print("[*] Please wait...\n")

    try:
        response = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        print(f"[-] Connection Error: {e}")
        return

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        gmails = set(re.findall(r"[a-zA-Z0-9_.+-]+@gmail\.com", soup.text))

        if gmails:
            print("[+] Gmail addresses found:\n")
            for gmail in gmails:
                print(f"  → {gmail}")
            print(f"\n[✓] Total {len(gmails)} Gmail(s) found.")
        else:
            print("[-] No Gmail addresses found for this number.")
    else:
        print("[-] Google blocked the request or failed to fetch results.")

if __name__ == "__main__":
    while True:
        banner()
        number = input("Enter hater phone number (e.g. +91XXXXXXXXXX): ").strip()
        if not number:
            print("[-] Please enter a valid number.")
            time.sleep(2)
            continue
        find_gmails_by_phone(number)
        again = input("\nDo you want to search another number? (y/n): ").lower()
        if again != 'y':
            break
