import requests
import os

# Token file jahan sab tokens line by line stored hain
TOKENS_FILE = "all_tokens.txt"

def check_uid(token):
    """
    Token se UID check karta hai
    """
    try:
        url = f"https://graph.facebook.com/me?access_token={token}"
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json().get("id")
    except:
        pass
    return None

def main():
    print("\n========== UID TOKEN FINDER ==========")
    target_uid = input("Enter Target UID: ").strip()

    if not os.path.exists(TOKENS_FILE):
        print(f"\n[ERROR] Token file '{TOKENS_FILE}' not found.")
        return

    tokens_checked = 0
    found = False

    with open(TOKENS_FILE, "r") as file:
        for line in file:
            token = line.strip()
            if not token:
                continue
            tokens_checked += 1
            owner_uid = check_uid(token)
            if owner_uid == target_uid:
                print(f"\n[+] Token FOUND for UID {target_uid}:\n{token}")
                found = True
                break

    if not found:
        print(f"\n[-] No token found for UID {target_uid}")
    print(f"\nChecked {tokens_checked} tokens.\n======================================")

if __name__ == "__main__":
    main()
