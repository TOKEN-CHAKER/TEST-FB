import requests
from bs4 import BeautifulSoup
import os
import time

def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*60)
    print("        PHONE NUMBER TO URL FINDER - by Broken Nadeem")
    print("="*60)

def find_urls_by_phone(phone_number):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    query = f'"{phone_number}"'
    url = f"https://www.google.com/search?q={query}"

    print(f"\n[*] Searching for: {phone_number}")
    print("[*] Please wait...\n")

    try:
        response = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        print(f"[-] Connection Error: {e}")
        return

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("a")

        found = 0
        printed_urls = set()

        for link in results:
            href = link.get("href")
            if href and "/url?q=" in href and "google.com" not in href:
                clean_url = href.split("&")[0].replace("/url?q=", "")
                if clean_url not in printed_urls:
                    print(f"[+] {clean_url}")
                    printed_urls.add(clean_url)
                    found += 1

        if found == 0:
            print("[-] No URLs found for this number.")
        else:
            print(f"\n[✓] Total {found} URLs found.")
    else:
        print("[-] Failed to fetch search results. Google might be blocking requests. Try again later.")

if __name__ == "__main__":
    while True:
        banner()
        number = input("Enter hater phone number (with country code, e.g. +91): ").strip()
        if not number:
            print("[-] Please enter a valid phone number.")
            time.sleep(2)
            continue
        find_urls_by_phone(number)
        again = input("\nDo you want to search another number? (y/n): ").lower()
        if again != 'y':
            break
