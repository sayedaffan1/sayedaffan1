#!/bin/bash
# Client Profile Generator
CLIENT=
if [ -z " ]; then
 echo Usage: ./generate_client.sh <client_name>
 exit 1
fi
echo [+] Generating profile for ...
echo [✓] Saved unified profile to clients/.ovpn