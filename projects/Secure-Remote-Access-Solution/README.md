# 🛡️ Hardened Secure Remote Access & Zero-Trust VPN Infrastructure

[![OpenVPN](https://img.shields.io/badge/OpenVPN-2.5%2B-EA7E20?style=for-the-badge&logo=openvpn&logoColor=white)](https://openvpn.net/)
[![Security: Zero Trust](https://img.shields.io/badge/Architecture-Zero_Trust-00C853?style=for-the-badge)](https://www.nist.gov/publications/zero-trust-architecture)
[![Encryption: AES-256-GCM](https://img.shields.io/badge/Cipher-AES--256--GCM-blue?style=for-the-badge)](https://en.wikipedia.org/wiki/Galois/Counter_Mode)
[![Network: iptables / NAT](https://img.shields.io/badge/Firewall-iptables_%26_VLANs-red?style=for-the-badge&logo=linux&logoColor=white)](https://netfilter.org/)

An enterprise-hardened, zero-trust remote access architecture implementing multi-factor certificate authentication, strict subnet isolation, TLS 1.3 cryptographic handshakes, and automated client certificate lifecycle management.

---

## 🌐 Network Defense Topology

```mermaid
graph TD
    Client[Remote Workstation / Client] -->|TLS 1.3 / AES-256-GCM Tunnel| Gateway[Hardened OpenVPN Gateway]
    Gateway --> Firewall{Stateful iptables Firewall & NAT}
    
    subgraph Zero-Trust Microsegmentation
        Firewall -->|VLAN 10: Port 22/3389 Auth Only| Mgt[Management Subnet 10.0.10.0/24]
        Firewall -->|VLAN 20: Least Privilege Only| Int[Internal Enterprise Servers 10.0.20.0/24]
        Firewall -.->|STRICT DROP by Default| DMZ[Isolated DMZ Subnet 10.0.30.0/24]
    end
```

---

## 🔒 Hardened Security Controls

* **Cipher Suite**: `AES-256-GCM` authenticated symmetric encryption.
* **Key Exchange & Forward Secrecy**: Diffie-Hellman 4096-bit parameters with `TLS-Crypt-v2` packet authentication.
* **Subnet Micro-segmentation**: `iptables` rules restrict remote workers strictly to designated application ports (Least Privilege).
* **Killswitch & DNS Leak Protection**: Server pushes `redirect-gateway def1` and hardened resolver configurations.

---

## 🚀 Quick Deployment Guide

### 1. Firewall & Routing Hardening
Execute the network setup script on the Linux gateway server:
```bash
chmod +x setup_firewall.sh
sudo ./setup_firewall.sh
```

### 2. Generate Client Certificate Profile
Automate certificate provisioning and export a single unified `.ovpn` configuration:
```bash
chmod +x generate_client.sh
sudo ./generate_client.sh engineering-workstation-01
```

---

## 📁 Repository Structure
```text
├── server.conf                # Hardened OpenVPN server configuration
├── client.ovpn.template       # Unified secure client configuration template
├── setup_firewall.sh          # Linux iptables routing & subnet isolation automation
├── generate_client.sh         # PKI cert generation and client profile packager
├── README.md                  # Comprehensive architecture and security guide
└── .gitignore                 # Excludes raw private keys (*.key, *.crt)
```

---

## 📄 License & Attribution
Maintained by **[Affan Sayed](https://github.com/sayedaffan1)** under the [MIT License](LICENSE).
