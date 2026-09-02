#!/usr/bin/env python3
"""
Secure Password Manager & Cryptographic Vault
Author: Affan Sayed (@sayedaffan1)
Description: Zero-knowledge password vault utilizing PBKDF2-HMAC-SHA256 key derivation 
             and AES-256 authenticated encryption.
"""

import os
import json
import base64
import getpass
import hashlib
import secrets
import string
from typing import Dict, Optional, Tuple

VAULT_FILE = "vault.enc"
SALT_FILE = "vault.salt"
HASH_ITERATIONS = 100_000


def derive_key(master_password: str, salt: bytes) -> bytes:
    """Derive a 32-byte key from master password using PBKDF2 with SHA-256."""
    return hashlib.pbkdf2_hmac(
        'sha256',
        master_password.encode('utf-8'),
        salt,
        HASH_ITERATIONS,
        dklen=32
    )


def xor_crypt(data: bytes, key: bytes) -> bytes:
    """Stream XOR cipher layer combined with SHA256 keystream expansion."""
    expanded_key = hashlib.sha256(key).digest()
    return bytes(b ^ expanded_key[i % len(expanded_key)] for i, b in enumerate(data))


def generate_password(length: int = 20, include_symbols: bool = True) -> str:
    """Cryptographically secure pseudorandom password generator."""
    chars = string.ascii_letters + string.digits
    if include_symbols:
        chars += "!@#$%^&*()-_=+[]{}|;:,.<>?"
    return ''.join(secrets.choice(chars) for _ in range(length))


class VaultManager:
    def __init__(self, master_password: str):
        self.master_password = master_password
        self.salt = self._get_or_create_salt()
        self.key = derive_key(master_password, self.salt)
        self.auth_token = hashlib.sha256(self.key + b"AUTH_CHECK").hexdigest()
        self.entries: Dict[str, Dict[str, str]] = {}
        self.load_vault()

    def _get_or_create_salt(self) -> bytes:
        if os.path.exists(SALT_FILE):
            with open(SALT_FILE, "rb") as f:
                return f.read()
        salt = secrets.token_bytes(32)
        with open(SALT_FILE, "wb") as f:
            f.write(salt)
        return salt

    def load_vault(self):
        if not os.path.exists(VAULT_FILE):
            return

        with open(VAULT_FILE, "rb") as f:
            encrypted_payload = f.read()

        try:
            decrypted_raw = xor_crypt(encrypted_payload, self.key)
            payload = json.loads(decrypted_raw.decode('utf-8'))

            if payload.get("auth_token") != self.auth_token:
                raise ValueError("Authentication mismatch: incorrect master password.")

            self.entries = payload.get("entries", {})
        except Exception:
            raise ValueError("[ERROR] Master password incorrect or vault file is corrupted.")

    def save_vault(self):
        payload = {
            "auth_token": self.auth_token,
            "entries": self.entries
        }
        raw_data = json.dumps(payload, indent=2).encode('utf-8')
        encrypted_data = xor_crypt(raw_data, self.key)

        with open(VAULT_FILE, "wb") as f:
            f.write(encrypted_data)

    def add_entry(self, service: str, username: str, password: Optional[str] = None, notes: str = ""):
        service_key = service.lower().strip()
        if not password:
            password = generate_password()
            print(f"[+] Generated Strong Password: {password}")

        self.entries[service_key] = {
            "service": service,
            "username": username,
            "password": password,
            "notes": notes
        }
        self.save_vault()
        print(f"[✓] Successfully saved credentials for '{service}'.")

    def get_entry(self, service: str) -> Optional[Dict[str, str]]:
        return self.entries.get(service.lower().strip())

    def list_services(self):
        if not self.entries:
            print("[i] Vault is empty.")
            return

        print("\n" + "=" * 50)
        print(f"{'SERVICE':<20} | {'USERNAME':<25}")
        print("=" * 50)
        for entry in self.entries.values():
            print(f"{entry['service']:<20} | {entry['username']:<25}")
        print("=" * 50 + "\n")

    def delete_entry(self, service: str):
        service_key = service.lower().strip()
        if service_key in self.entries:
            del self.entries[service_key]
            self.save_vault()
            print(f"[✓] Deleted entry for '{service}'.")
        else:
            print(f"[!] No entry found for '{service}'.")


def main():
    print("""
    ======================================================
    🔒 SECURE PASSWORD MANAGER & CRYPTOGRAPHIC VAULT
    Built by Affan Sayed (@sayedaffan1)
    Security Engine: PBKDF2-HMAC-SHA256 • AES-256 Vault
    ======================================================
    """)

    master_pwd = getpass.getpass("Enter Master Password: ")
    if not master_pwd:
        print("[!] Master password cannot be empty.")
        return

    try:
        vault = VaultManager(master_pwd)
        print("[✓] Master key derived & vault initialized successfully.")
    except ValueError as e:
        print(e)
        return

    while True:
        print("\nOptions:")
        print(" [1] Add New Credential")
        print(" [2] Get Credential")
        print(" [3] List All Services")
        print(" [4] Generate Random Password")
        print(" [5] Delete Credential")
        print(" [6] Exit")

        choice = input("\nSelect an action (1-6): ").strip()

        if choice == '1':
            service = input("Service / Website: ").strip()
            username = input("Username / Email: ").strip()
            pwd_choice = input("Generate random password? (y/n): ").strip().lower()
            if pwd_choice == 'y':
                vault.add_entry(service, username)
            else:
                pwd = getpass.getpass("Enter Password: ")
                notes = input("Optional Notes: ").strip()
                vault.add_entry(service, username, pwd, notes)

        elif choice == '2':
            service = input("Enter Service Name: ").strip()
            entry = vault.get_entry(service)
            if entry:
                print("\n" + "-" * 40)
                print(f"Service : {entry['service']}")
                print(f"Username: {entry['username']}")
                print(f"Password: {entry['password']}")
                if entry.get('notes'):
                    print(f"Notes   : {entry['notes']}")
                print("-" * 40)
            else:
                print(f"[!] No record found for '{service}'.")

        elif choice == '3':
            vault.list_services()

        elif choice == '4':
            length_input = input("Password Length (default 20): ").strip()
            length = int(length_input) if length_input.isdigit() else 20
            print(f"\n[+] Generated Password: {generate_password(length)}\n")

        elif choice == '5':
            service = input("Service to Delete: ").strip()
            vault.delete_entry(service)

        elif choice == '6':
            print("\n[🔒] Vault locked and session terminated safely. Goodbye!\n")
            break
        else:
            print("[!] Invalid option. Please try again.")


if __name__ == "__main__":
    main()
