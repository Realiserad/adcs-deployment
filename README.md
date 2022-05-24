About
=====

This repository contains the documentation and installation files needed to successfully deploy PKI based on Active Directory Certificate Services (AD CS).

The documentation is supposed to be *reusable*, all customer-specific data should go into ``group_vars/all.yml`` which is rendered using Jinja2 templating.

To speed up the installation process, minimise the risk of making mistakes and make it possible to deploy on Windows Server Core, operations should be carried out using PowerShell commands where possible.

Prerequisites
=============

Install on Ubuntu
-----------------

Download LaTeX, Python and Python's package manager::

    sudo apt install texlive-full python3 python3-pip

Install Sphinx, Ansible and the RST linter::

    pip3 install sphinx ansible restructuredtext-lint::

Install the Ansible modules needed::

    ansible-galaxy collection install community.general

Build
=====

1. Adjust ``group_vars/all.yml`` according to the customer's needs.

2. Build the documentation and installation files using Ansible::

ansible-playbook playbook.yml

The result is put in ``Customer.zip``. 
