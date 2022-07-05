About
=====

This directory contains files needed to build a Naming and Profile Document for an AD CS-installation.

The content of the document is extracted from the Public Key Services configuration exported from AD as LDIF objects.

How to use
==========

1. Log in to one of the domain controllers.

2. Open PowerShell and export *Public Key Services* from AD using ``ldifde``. For example, if your domain is called ``example.com``, you would run the following command:
    ```
    ldifde -m -v -d "CN=Public Key Services,CN=Services,CN=Configuration,DC=example,DC=com" -f Configuration.ldf
    ```

    This saves the configuration as an LDIF-file named ``Configuration.ldf``.

    > **NOTE** You need to use the filename ``Configuration.ldf`` for the playbook to detect it.

3. Optionally log in to each one of the CA machines and export the local configuration from the registry.
    ```
    $CaName = (CertUtil -cainfo name | Select-String 'CA name: (.+)').Matches.Groups[1].Value
    reg save HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\CertSvc\Configuration $CaName.dat
    ```

4. Create a new folder called ``customer`` in this folder. Transfer ``Configuration.ldf`` and any registry hives to this directory.

5. Install the necessary dependencies.
    ```
    pip3 install ldif pyyaml pygments-ldif cryptography regipy
    ```

6. Adjust ``group_vars/all.yml`` to fit the customer's needs.
    ```
    npm install -g @alexlafroscia/yaml-merge
    yaml-merge ../group_vars/sample.yml group_vars/sample.yml > group_vars/all.yml
    ```

    > **NOTE** You may not want to include all certificate templates from AD in your Naming and Profile Document. You can specify the name of the templates you want to include in the document like this:
    >
    > ```
    > extras:
    >   naming_and_profile_document:
    >     templates:
    >     - name: Certificate Template 1
    >     - name: Certificate Template 2
    > ```

7. Run the Ansible playbook to build the Naming and Profile Document.
    ```
    ansible-playbook playbook.yml
    ```

The playbook creates a ``release`` folder where the document is located.

Create a sample
===============

If you just want to quickly build a document for review, you can use the sample file located in the ``sample`` directory by running the Ansible playbok with ``--tags sample`` as shown below.
```
ansible-playbook playbook.yml --tags sample
```
