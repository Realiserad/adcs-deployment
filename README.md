[![Build status](https://github.com/Realiserad/adcs-deployment/actions/workflows/publish.yml/badge.svg?event=push&branch=main)](https://github.com/Realiserad/adcs-deployment/actions/workflows/publish.yml)

About
=====

This repository contains the documentation and scripts needed to successfully deploy and operate a PKI based on Microsoft Active Directory Certificate Services (AD CS).

The documentation is supposed to be *reusable*, all customer specific data should go into ``group_vars/all.yml`` which is rendered using Jinja2 templating.

To speed up the installation process, minimise the risk of making mistakes and make it possible to deploy on Windows Server Core, operations should be carried out using PowerShell commands where possible.

After building, the result is put in the ``release`` folder:

- ``system-documentation.zip`` contains the system documentation for AD CS in HTML, PDF and DOCX format.
- ``pki-assessment-bundle.zip`` contains *AD CS Collector* and instructions for how to use it.
- ``proposal-new-adcs-installation-with-luna.docx`` describes a proposal for a new installation of AD CS with a Luna 7 HSM.
- ``proposal-pki-assessment.docx`` describes a proposal for assessing an existing PKI based on AD CS.

Build
=====

Build using the container
-------------------------

You can use the container to build the documentation on any system where you have Docker installed. The container can be built locally or pulled directly from GitHub's container registry at ``ghcr.io``.

1. Create an Ansible configuration file named ``all.yml``, and adjust it according to the customer's needs. You can use ``group_vars/sample.yml`` as a template.

2. Build and run the container. The configuration file ``all.yml`` must be provided on a volume mapped to ``/build`` on the container. The output files are written to the ``release`` folder on this volume before the container stops.
    ```
    docker build -t realiserad/adcs-deployment .
    docker run -v (pwd)/group_vars/all.yml:/build/all.yml -v (pwd)/release:/build/release realiserad/adcs-deployment
    ```

| File                     | Description                                                                      | Required                                  |
|--------------------------|----------------------------------------------------------------------------------|-------------------------------------------|
| /build/all.yml           | Ansible configuration file.                                                      | Yes                                       |
| /build/logo.png          | Customer logo.                                                                   | No                                        |
| /build/Configuration.ldf | Configuration exported from AD used to generate the Naming and Profile Document. | To create the Naming and Profile Document |
| /build/*.dat             | Registry hive(s) used to generate parts of the Naming and Profile Document.      | No                                        |

Build on Ubuntu
---------------

1. Create ``group_vars/all.yml`` and adjust it according to the customer's needs.
    ```
    cp group_vars/sample.yml group_vars/all.yml
    ```

2. Replace the customer specific files in ``files/customer``.

3. Install dependencies.
    ```
    sudo apt install texlive-full python3 python3-pip zip pandoc git graphviz
    pip3 install sphinx ansible restructuredtext-lint doc8 docxtpl diagrams docxbuilder guzzle_sphinx_theme
    ansible-galaxy collection install community.general
    ```

4. Build the documentation and installation files using Ansible.
    ```
    ansible-playbook playbook.yml
    ```
Contribute
==========

List TODO items
---------------

Parts of the code which may be improved in the future are marked with *TODO* followed by a comment.

You can use ``git-grep`` to search for these items.
```
git grep --untracked "TODO:" ./
```

Pull requests
-------------

It is recommended to commit changes to a separate branch and create a pull request in GitHub. This makes it possible to perform a code review and test any changes separately.

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
Sometimes, it is convenient to keep a pull request open while working on a feature. Mark the pull request with ``Draft`` in the beginning of the title to avoid an accidental merge of unfinished work.

Squash commits before merging
-----------------------------

Consider squashing the commits into one commit when merging to ``main`` to keep the history clean. In GitHub, this is done by selecting the option "Squash and merge" when accepting the pull request.

Automatic builds
----------------

Once changes are pushed to the ``main`` branch, GitHub Actions will automatically build a new container and push it to the GitHub Container Registry. If you want to avoid triggering a container build, you can put ``#nobuild`` somewhere in your commit message.
