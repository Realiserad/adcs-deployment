[![publish](https://github.com/Realiserad/adcs-deployment/actions/workflows/publish.yml/badge.svg?event=push&branch=main)](https://github.com/Realiserad/adcs-deployment/actions/workflows/publish.yml)

About
=====

This repository contains the documentation needed to successfully deploy a PKI based on Active Directory Certificate Services (AD CS).

The documentation is supposed to be *reusable*, all customer-specific data should go into ``group_vars/all.yml`` which is rendered using Jinja2 templating.

To speed up the installation process, minimise the risk of making mistakes and make it possible to deploy on Windows Server Core, operations should be carried out using PowerShell commands where possible.

After building, the result is put in the ``release`` folder:

- ``Customer.zip`` contains the documentation for AD CS in HTML and PDF format.
- ``Genomlysning av PKI.zip`` contains *AD CS Collector* and instructions for how to use it.
- ``proposal-adcs-with-luna.docx`` describes a proposal for an installation of AD CS with a Luna 7 HSM.
- ``proposal-pki-assessment.docx`` describes a proposal for assessing an existing PKI based on AD CS.

Build
=====

Build using the container
-------------------------

You can use the container to build the documentation on any system where you have Docker installed. The container can be built locally or pulled directly from GitHub's container registry at ``ghcr.io``.

1. Adjust ``group_vars/all.yml`` according to the customer's needs.

2. Build and run the container. The configuration file ``all.yml`` must be provided on a volume mapped to ``/build`` on the container. The output files are written to the ``release`` folder on this volume before the container stops.
    ```
    docker build -t realiserad/adcs-deployment .
    docker run -v (pwd)/group_vars/all.yml:/build/all.yml -v (pwd)/release:/build/release realiserad/adcs-deployment
    ```

Build on Ubuntu
---------------

1. Adjust ``group_vars/all.y--user (id -u):(id -g)ml`` according to the customer's needs.

2. Install dependencies.
    ```
    sudo apt install texlive-full python3 python3-pip zip pandoc git graphviz
    pip3 install sphinx ansible restructuredtext-lint doc8 docxtpl diagrams guzzle_sphinx_theme
    ansible-galaxy collection install community.general
    ```

2. Build the documentation and installation files using Ansible.
    ```
    ansible-playbook playbook.yml
    ```
Contribute
==========

It is recommended to commit changes to a separate branch and create a pull request in GitHub. This makes it possible to perform a code review and test any changes separately. The changes can then be merged to ``main`` in GitHub.

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
    
Once changes are pushed to the ``main`` branch, GitHub Actions will automatically build a new container and push it to the GitHub Container Registry. If you want to avoid triggering a container build, you can put ``#nobuild`` somewhere in your commit message.
