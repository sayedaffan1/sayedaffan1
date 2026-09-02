#!/bin/bash
# =========================================================
# Automated iptables Hardening & Subnet Isolation Script
# Author: Affan Sayed (@sayedaffan1)
# =========================================================

echo [+] Enabling IPv4 Packet Forwarding...
sysctl -w net.ipv4.ip_forward=1

echo [+] Flushing existing firewall rules...
iptables -F
iptables -X
iptables -t nat -F

echo [+] Setting default DROP policies...
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

echo [+] Allowing loopback & established traffic...
iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

echo [+] Opening OpenVPN port (1194/UDP)...
iptables -A INPUT -p udp --dport 1194 -j ACCEPT

echo [+] Configuring NAT masquerade for VPN subnet...
iptables -t nat -A POSTROUTING -s 10.8.0.0/24 -o eth0 -j MASQUERADE

echo [+] Micro-segmentation: Restricting VPN clients to authorized subnets...
iptables -A FORWARD -s 10.8.0.0/24 -d 10.0.10.0/24 -p tcp --dport 22 -j ACCEPT
iptables -A FORWARD -s 10.8.0.0/24 -d 10.0.20.0/24 -p tcp --dport 443 -j ACCEPT

echo [✓] Firewall and micro-segmentation successfully configured!