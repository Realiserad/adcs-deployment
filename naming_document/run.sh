#!/bin/sh

# Builds the Naming and Profile Document if there is a customer
# configuration available.

if [ -f "/build/Configuration.ldf" ]; then
    echo "🔨 Building the Naming and Profile Document."
    cp /build/all.yml group_vars/
    ansible-playbook playbook.yml
else
    echo "⏭️ Not building the Naming and Profile Document, the file '/build/Configuration.ldf' is not present on the volume."
fi