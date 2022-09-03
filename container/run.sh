#!/bin/sh

echo "🏁 Starting the ADCS build container!"
echo "ℹ️ Built from commit $(git rev-parse HEAD)."

if [ ! -f "/build/all.yml" ]; then
    echo "🙁 I could not find an Ansible configuration file!"
    echo "🧑‍🏫 Create a file called 'all.yml' and provide it on a volume mapped to '/build' in the container."
    exit 1
fi

if [ -f "/build/logo.png" ]; then
    echo "🖼️ Copying customer logo from volume."
    cp /build/logo.png files/customer/logo.png
fi
ansible-playbook playbook.yml
mkdir -p /build/release
cp release/* /build/release

for directory in ./*; do
    if [ -f "$directory/playbook.yml" ]; then
        echo "😃 Found addon '$(basename "$directory")'."
        cd "$directory"
        ansible-playbook playbook.yml
        cp release/* /build/release
        cd -
    fi
done

echo "🎉 I created the following artifacts in '/build/release':"
ls /build/release