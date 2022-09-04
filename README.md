[![Build status](https://github.com/Realiserad/adcs-deployment/actions/workflows/publish.yml/badge.svg?event=push&branch=main)](https://github.com/Realiserad/adcs-deployment/actions/workflows/publish.yml)

About
=====

This repository contains the documentation and scripts needed to successfully deploy and operate a PKI based on Microsoft Active Directory Certificate Services (ADCS).

The documentation is supposed to be *reusable*, all customer specific data should go into ``group_vars/all.yml`` which is rendered using Jinja2 templating.

To speed up the installation process, minimise the risk of making mistakes and make it possible to deploy on Windows Server Core, operations should be carried out using PowerShell commands where possible.

After building, the result is put in the ``release`` folder:

- ``system-documentation.zip`` contains the system documentation for ADCS in HTML, PDF and DOCX format.

Build
=====

You can a container to build the documentation on any system where you have Docker installed. The container can be built locally or pulled directly from GitHub's container registry at ``ghcr.io``.

1. Adjust the Ansible configuration file ``group_vars/all.yml`` according to the customer's needs.

2. Optionally replace the files in ``files`` to customise the output according to the table below.

| File                    | Description                                                 | Can remove?     |
|-------------------------|-------------------------------------------------------------|-----------------|
| files/                  | Folder containing customisation files                       |                 |
|   all.yml               | Ansible configuration file.                                 |                 |
|   logo.png              | Customer logo.                                              |                 |
|   atea.png              | Logo used for PDF headers.                                  |                 |
|   atea_aligned.png      | Logo used for PDF headers.                                  |                 |
|   naming_document/      |                                                             | Yes             |
|     Configuration.ldf   | Configuration exported from AD.                             |                 |
|     *.dat               | Registry hive(s).                                           | Yes             |

3. Generate a ``Dockerfile`` and build the container.
```
./build.sh
```

4. Run the container. The Ansible configuration file and a directory with customisations  must be provided on a volume mapped to ``/build`` on the container. The output files are written to the ``release`` folder on this volume before the container stops.
```
docker run \
  -v (pwd)/group_vars/all.yml:/build/all.yml \
  -v (pwd)/files:/build/files \
  -v /tmp/release:/build/release \
  realiserad/adcs-deployment
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

Pull requests are squashed
--------------------------

When a pull request is accepted, all commits are being squashed into one commit to keep the history of the ``main`` branch as clean as possible. In GitHub, this is done by selecting the option "Squash and merge" when accepting the pull request.

Automatic builds
----------------

Once changes are pushed to the ``main`` branch, GitHub Actions will automatically build a new container and push it to the GitHub Container Registry. If you want to avoid triggering a container build, you can put ``#nobuild`` somewhere in your commit message.
