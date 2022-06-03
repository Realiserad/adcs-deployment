About
=====

This directory contains files needed to build a Naming and Profile Document for an AD CS-installation.

The content of the document is extracted from certificate templates exported from AD as LDIF files.

How to use
==========

1. Log in to one of the domain controllers.

2. Open PowerShell and export the certificate templates from AD using ``ldifde``. For example, if you want to export a certificate template named ``MyTemplate``residing in the ``example.com`` domain, you would run the following command:

    ```
    ldifde -m -v -d "CN=MyTemplate,CN=Certificate Templates,CN=Public Key Services,CN=Services,CN=Configuration,DC=example,DC=com" -f MyTemplate.ldf
    ```

    This saves the certificate template as an LDIF-file named ``MyTemplate.ldf``.

    > **NOTE** You need to use the ``.ldf`` file extension for the certificate template to be included in the Naming and Profile Document.

3. Create a new folder called ``customer`` in this folder. Transfer your LDIF-files to this directory.

4. Adjust ``group_vars/all.yml`` to fit your needs.

5. Run the Ansible playbook to build the Naming and Profile Document.

    ```
    ansible-playbook playbook.yml
    ```

The playbook creates a ``release`` folder where the document is located.

Create a sample
===============

If you just want to quickly build a document for review, you can use the sample templates located in the ``samples`` directory by running the Ansible playbok with the ``--sample`` tag.
```
    ansible-playbook playbook.yml --tags sample
```
