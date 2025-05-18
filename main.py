import requests
import time
import random
import os

def banner():
    os.system('clear' if os.name != 'nt' else 'cls')
    print("="*60)
    print("     FACEBOOK GROUP AUTO REPORT TOOL - by Broken Nadeem")
    print("="*60)

def load_tokens(file_path):
    if not os.path.exists(file_path):
        print("[-] Token file not found.")
        return []
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def report_group(token, group_id):
    url = f"https://graph.facebook.com/{group_id}/report"
    payload = {
        "reason": "nudity",  # You can change to 'spam', 'hate', etc.
        "access_token": token
    }

    try:
        res = requests.post(url, data=payload)
        if res.status_code == 200:
            print(f"[✓] Report sent successfully with token: {token[:10]}...")
        else:
            print(f"[-] Failed with token: {token[:10]}... | {res.text}")
    except Exception as e:
        print(f"[-] Error: {e}")

def main():
    banner()
    group_id = input("Enter Target Group ID: ").strip()
    token_file = input("Enter token file path (one token per line): ").strip()
    tokens = load_tokens(token_file)

    if not tokens:
        print("[-] No tokens found.")
        return

    print(f"\n[+] Starting report flood on Group ID: {group_id}")
    print(f"[+] Total Tokens Loaded: {len(tokens)}\n")

    for token in tokens:
        report_group(token, group_id)
        time.sleep(random.uniform(1.5, 3.0))  # To avoid detection

    print("\n[✓] Reporting completed.")

if __name__ == "__main__":
    main()
