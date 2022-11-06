#!/bin/sh
cat << EOF
FROM ubuntu:jammy

LABEL org.opencontainers.image.source https://github.com/Realiserad/adcs-deployment

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

RUN mkdir -p /etc/ansible
RUN mkdir -p /root/group_vars
RUN ln -s /build/all.yml /root/group_vars/all.yml
RUN ln -s /build/files /root/files

COPY container/run.sh /root
COPY container/ansible.cfg /etc/ansible

COPY roles /root/roles
COPY playbook.yml /root/playbook.yml
COPY .git /root/.git

RUN apt update --fix-missing
RUN apt install python3 python3-pip zip git -y

EOF

snippets='# Dependencies'

for snippet in roles/*/container/Dockerfile.snippet; do
    snippets="$snippets\n$(cat $snippet)"
done

echo "$snippets" > /dev/shm/snippets
awk '!x[$snippets]++' /dev/shm/snippets

cat << EOF

RUN rm -rf /var/lib/apt/lists/*
WORKDIR /root

CMD /bin/sh run.sh
EOF