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


RUN pip3 install ldif pyyaml pygments-ldif cryptography regipy
RUN apt install -y texlive-latex-recommended texlive-fonts-recommended texlive-latex-extra latexmk texlive-luatex graphviz cowsay && \
    pip3 install sphinx ansible restructuredtext-lint doc8 diagrams docxbuilder guzzle_sphinx_theme docxtpl && \
    ansible-galaxy collection install community.general

RUN rm -rf /var/lib/apt/lists/*
WORKDIR /root

CMD /bin/sh run.sh
