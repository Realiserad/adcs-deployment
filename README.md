About
=====

This repository contains the documentation needed to successfully deploy a PKI based on Active Directory Certificate Services (AD CS).

The documentation is supposed to be *reusable*, all customer-specific data should go into ``group_vars/all.yml`` which is rendered using Jinja2 templating.

To speed up the installation process, minimise the risk of making mistakes and make it possible to deploy on Windows Server Core, operations should be carried out using PowerShell commands where possible.

Prerequisites
=============

The documentation is written in RST and Jinja2 which can be edited using any text editor, for example Visual Studio Code. To build the documentation using Ansible, you also need to install Sphinx and optionally a LaTeX distribution of your choice for producing PDF files.

Install on Ubuntu
-----------------

Install the required packages using ``apt`` and Python's package manager.

    sudo apt install texlive-full python3 python3-pip zip pandoc git
    pip3 install sphinx ansible restructuredtext-lint doc8 docxtpl diagrams
    ansible-galaxy collection install community.general
Build
=====

1. Adjust ``group_vars/all.yml`` according to the customer's needs.

2. Build the documentation and installation files using Ansible:

    ```
    ansible-playbook playbook.yml
    ```

The result is put in the ``release`` folder:

- ``Customer.zip`` contains the documentation for AD CS in HTML and PDF format.
- ``Genomlysning av PKI.zip`` contains *AD CS Collector* and instructions for how to use it.
- ``proposal-adcs-with-luna.docx`` describes a proposal for an installation of AD CS with a Luna 7 HSM.
- ``proposal-pki-assessment.docx`` describes a proposal for assessing an existing PKI based on AD CS.

Contribute
==========

Small changes, unlikely to cause any breakage can be pushed directly to main. Larger work, split over multiple commits which should be reviewed as one, can preferably be put on a separate branch. Fo example:

1. Create and check out a new branch in git.

    ```
    git branch my-fancy-feature
    ```

2. Commit your changes and push them to GitHub.

    ```
    git add -A
    git commit
    git push --set-upstream origin my-fancy-feature
    ```

A pull request can then be created from the branch ``my-fancy-feature`` and reviewed in GitHub before merging to ``main``.
