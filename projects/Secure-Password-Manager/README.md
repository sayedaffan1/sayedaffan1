# 🔑 Secure Password Manager & Cryptographic Vault

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Security: Zero Knowledge](https://img.shields.io/badge/Security-Zero_Knowledge-00C853?style=for-the-badge)](https://en.wikipedia.org/wiki/Zero-knowledge_proof)
[![Cryptography: PBKDF2](https://img.shields.io/badge/Key_Derivation-PBKDF2--HMAC--SHA256-blue?style=for-the-badge)](https://en.wikipedia.org/wiki/PBKDF2)
[![License: MIT](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)](LICENSE)

A lightweight, zero-knowledge, and cryptographically fortified credential vault built in Python. Designed to securely generate, encrypt, store, and manage secrets locally without third-party cloud vulnerabilities.

---

## 🏗️ Cryptographic Architecture

```mermaid
flowchart TD
    A[Master Password] --> B[PBKDF2-HMAC-SHA256]
    C[Cryptographic Salt 32-byte CSPRNG] --> B
    B -->|100,000 Iterations| D[256-Bit Master Key]
    E[Plaintext Credentials JSON] --> F[Authenticated Encryption Engine]
    D --> F
    F --> G[(vault.enc Encrypted File)]
```

---

## 🔒 Security Properties & Defense Features

* **Zero-Knowledge Local Storage**: Master keys are never written to disk or transmitted across networks.
* **PBKDF2-HMAC-SHA256 Key Stretching**: Salted with 100,000 iterations to mitigate GPU/ASIC brute-force and dictionary attacks.
* **Authenticated Integrity Verification**: SHA-256 HMAC verification token detects tampering or incorrect master password input.
* **CSPRNG Random Password Generator**: Cryptographically secure pseudorandom token generation with customizable symbol entropy.

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/sayedaffan1/Secure-Password-Manager.git
cd Secure-Password-Manager
```

### 2. Run the Application
```bash
python password_manager.py
```

---

## 💻 CLI Usage Demonstration

```text
======================================================
🔒 SECURE PASSWORD MANAGER & CRYPTOGRAPHIC VAULT
Built by Affan Sayed (@sayedaffan1)
Security Engine: PBKDF2-HMAC-SHA256 • AES-256 Vault
======================================================

Enter Master Password: ******************
[✓] Master key derived & vault initialized successfully.

Options:
 [1] Add New Credential
 [2] Get Credential
 [3] List All Services
 [4] Generate Random Password
 [5] Delete Credential
 [6] Exit
```

---

## 📜 Threat Model & Assumptions

1. **At-Rest Protection**: If the `vault.enc` file is exfiltrated, data remains protected against offline attacks due to high-iteration key stretching and CSPRNG salt.
2. **Side-Channel Minimization**: Sensitive password input is masked from standard terminal outputs using secure streams.

---

## 📄 License
This project is open-source and licensed under the [MIT License](LICENSE).
Author: **[Affan Sayed](https://github.com/sayedaffan1)**
