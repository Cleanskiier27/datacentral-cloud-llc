#!/bin/bash
# NetworkBuster Ultimate Permission Test Script
# Runs with root access to test protection system

wsl -u root bash -c "cd /mnt/c/Users/cadil/datacentral-cloud-llc && chmod +x scripts/*.sh && bash scripts/protection.sh test"
