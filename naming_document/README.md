About
=====

This directory contains files needed to build a Naming and Profile Document for an AD CS-installation.

The content of the document is extracted from certificate templates exported from AD as LDIF files.

How to use
==========

1. Log in to one of the domain controllers.

2. Open PowerShell and export *Public Key Services* from AD using ``ldifde``. For example, if your domain is called ``example.com``, you would run the following command:
    ```
    ldifde -m -v -d "CN=Public Key Services,CN=Services,CN=Configuration,DC=example,DC=com" -f Configuration.ldf
    ```

    This saves the configuration as an LDIF-file named ``Configuration.ldf``.

    > **NOTE** You need to use the filename ``Configuration.ldf`` for the playbook to detect it.

3. Create a new folder called ``customer`` in this folder. Transfer ``Configuration.ldf`` to this directory.

4. Adjust ``group_vars/all.yml`` to fit your needs.
    ```
    mkdir -p group_vars
    cp ../group_vars/*.yml group_vars/
    ```

    > **NOTE** You may not want to include all certificate templates from AD in your Naming and Profile Document. You can specify the name of the templates you want to include in the document like this:
    >
    > ```
    > naming_and_profile_document:
    >     templates:
    >     - name: Certificate Template 1
    >     - name: Certificate Template 2
    > ```

5. Install the necessary dependencies.
    ```
    pip3 install ldif pyyaml pygments-ldif
    ```

6. Run the Ansible playbook to build the Naming and Profile Document.
    ```
    ansible-playbook playbook.yml
    ```

The playbook creates a ``release`` folder where the document is located.

Create a sample
===============

If you just want to quickly build a document for review, you can use the sample templates located in the ``samples`` directory by running the Ansible playbok with ``--tags sample`` as shown below.
```
ansible-playbook playbook.yml --tags sample
```
