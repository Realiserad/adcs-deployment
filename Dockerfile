FROM ubuntu:jammy

LABEL org.opencontainers.image.source https://github.com/Realiserad/adcs-deployment

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

RUN apt update --fix-missing && \
    apt install -y texlive-latex-recommended texlive-fonts-recommended texlive-latex-extra latexmk texlive-luatex python3 python3-pip zip pandoc git graphviz cowsay && \
    pip3 install sphinx ansible restructuredtext-lint doc8 docxtpl diagrams docxbuilder guzzle_sphinx_theme && \
    rm -rf /var/lib/apt/lists/* && \
    ansible-galaxy collection install community.general

RUN mkdir -p /etc/ansible && \
    mkdir -p /root/group_vars && \
    ln -s /build/all.yml /root/group_vars/all.yml

COPY files /root/files
COPY templates /root/templates
COPY playbook.yml /root/playbook.yml
COPY .git /root/.git

# extras.naming_and_profile_document
COPY naming_document /root/naming_document
RUN pip3 install ldif pyyaml pygments-ldif cryptography regipy
RUN ln -sf /build/all.yml /root/naming_document/group_vars/all.yml

COPY container/run.sh /root
COPY container/ansible.cfg /etc/ansible

WORKDIR /root

CMD /bin/sh run.sh
