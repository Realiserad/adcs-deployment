#!/bin/sh

echo "🏁 Starting the ADCS build container!"
echo "ℹ️ Built from commit $(git rev-parse HEAD)."

if [ ! -f "/build/all.yml" ]; then
    echo "🙁 I could not find an Ansible configuration file!"
    echo "🧑‍🏫 Create a file called 'all.yml' and provide it on a volume mapped to '/build' in the container."
    exit 1
fi

if [ ! -d "/build/files" ]; then
    echo "🙁 I could not find a customisations directory!"
    echo "🧑‍🏫 Create a directory called 'files' and provide it on a volume mapped to '/build' in the container."
    exit 1
fi

ansible-playbook playbook.yml
mkdir -p /build/release
cp release/* /build/release

echo "🎉 I created the following artifacts in '/build/release':"
ls /build/release