About
=====

This directory contains files needed to build a Naming and Profile Document for an ADCS-installation.

The content of the document is extracted from the Public Key Services configuration exported from AD as LDIF objects.

How to use
==========

1. Log in to one of the domain controllers.

2. Open PowerShell and export *Public Key Services* from AD using ``ldifde``. For example, if your domain is called ``example.com``, you would run the following command:
    ```
    ldifde -m -v -d "CN=Public Key Services,CN=Services,CN=Configuration,DC=example,DC=com" -f Configuration.ldf
    ```

    This saves the configuration as an LDIF-file named ``Configuration.ldf``.

    > **NOTE** You *need* to use the filename ``Configuration.ldf`` for the playbook to detect it.

3. Optionally log in to each one of the CA machines and export the local configuration from the registry.
    ```
    $CaName = (CertUtil -cainfo name | Select-String 'CA name: (.+)').Matches.Groups[1].Value
    reg save HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\CertSvc\Configuration $CaName.dat
    ```

4. Put ``Configuration.ldf`` and any registry hives on a volume mapped to ``/build/files`` on the container.