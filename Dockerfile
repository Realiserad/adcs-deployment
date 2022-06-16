FROM ubuntu:jammy

LABEL org.opencontainers.image.source https://github.com/Realiserad/adcs-deployment

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

RUN apt update
RUN apt install -y texlive-latex-recommended texlive-fonts-recommended texlive-latex-extra latexmk texlive-luatex
RUN apt install -y python3 python3-pip zip pandoc git graphviz
RUN pip3 install sphinx ansible restructuredtext-lint doc8 docxtpl diagrams guzzle_sphinx_theme
RUN ansible-galaxy collection install community.general

RUN mkdir -p /build/release
RUN mkdir -p /root/group_vars
RUN ln -s /build/release /root/release
RUN ln -s /build/all.yml /root/group_vars/all.yml

COPY files /root/files
COPY templates /root/templates
COPY playbook.yml /root/playbook.yml
COPY .git /root/.git

WORKDIR /root

CMD ansible-playbook playbook.yml