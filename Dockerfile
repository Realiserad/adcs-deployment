FROM ubuntu:jammy

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

RUN apt update
RUN apt install -y texlive-full python3 python3-pip zip pandoc git
RUN pip3 install sphinx ansible restructuredtext-lint doc8 docxtpl diagrams
RUN ansible-galaxy collection install community.general
RUN mkdir -p /root/release

ADD files /root
ADD templates /root
ADD group_vars /root
COPY playbook.yml /root

WORKDIR /root

CMD ansible-playbook playbook.yml