import os

def load_file(phone_number):
    filename = f"{phone_number}.txt"
    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            content = f.read()
        print(f"\n=== Content of {filename} ===\n{content}\n=============================")
        return True
    else:
        print(f"\n[!] File '{filename}' not found.")
        return False

def edit_file(phone_number):
    filename = f"{phone_number}.txt"
    print("\n[+] Enter new content for the file (type 'END' on a new line to finish):")
    lines = []
    while True:
        line = input()
        if line.strip().upper() == 'END':
            break
        lines.append(line)

    with open(filename, 'w') as f:
        f.write("\n".join(lines))
    print(f"\n[+] File '{filename}' updated successfully.")

def main():
    print("=== Phone Number File Loader ===")
    phone_number = input("Enter phone number: ").strip()
    
    found = load_file(phone_number)
    
    if found:
        print("\nOptions:")
        print("1. Edit this file")
        print("2. Exit")
        choice = input("Select an option (1 or 2): ").strip()
        if choice == '1':
            edit_file(phone_number)
        else:
            print("Exiting...")
    else:
        print("\nDo you want to create this file?")
        choice = input("Type 'yes' to create, anything else to exit: ").strip().lower()
        if choice == 'yes':
            edit_file(phone_number)
        else:
            print("Exiting...")

if __name__ == "__main__":
    main()
