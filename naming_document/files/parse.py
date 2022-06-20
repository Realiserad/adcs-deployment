#
# Script for parsing certificate templates and certificate authorities for
# Active Directory Certificate Services, exported from Active Directory as LDIF.
#
# On a Windows machine, you can perform the export using ldifde.
# For example, if you want to export a certificate template named
# "MyTemplate" residing in the "example.com" domain, you would run
# the following command:
#
#    ldifde -m -v -d "CN=MyTemplate,CN=Certificate Templates,
#        ↪ CN=Public Key Services,CN=Services,CN=Configuration,
#        ↪ DC=example,DC=com" -f MyTemplate.ldf
#
# You can also export everything under Public Key Services, including
# certificate authorities.
#
#    ldifde -m -v -d "CN=Public Key Services,CN=Services,CN=Configuration,
#        ↪ DC=example,DC=com" -f Configuration.ldf
#
# The parsed data is printed as a YAML list to stdout.
#
# Before you can run the script, you need to install a couple of
# Python packages:
#
#     pip3 install ldif pyyaml
#
# Usage:
#
#     python3 parse.py --file <Template.ldif>
#
# Log lines are written to the syslog. To enable debug logging, run the script
# with the --debug flag.

import argparse
from ldif import LDIFParser
import os
import json
import yaml
from datetime import datetime
import logging
import logging.handlers

# Class for hex encoding all binary values we don't have
# any special handling for.
class HexEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, bytes):
            return ''.join(format(x, '02x') for x in o)
        return json.JSONEncoder.default(self, o)

# Converts a Win32 FILETIME structure to a dictionary.
# {
#   "unit": "years|months|weeks|days|hours",
#   "value": int
# }
def filetime_to_dict(filetime):
    intervals = 18446744073709551616 - int.from_bytes(filetime, byteorder = 'little')
    if intervals % (1E7 * 60 * 60 * 24 * 365) == 0:
        return {
            "unit": "years",
            "value": int(intervals / (1E7 * 60 * 60 * 24 * 365))
        }
    if intervals % (1E7 * 60 * 60 * 24 * 30) == 0:
        return {
            "unit": "months",
            "value": int(intervals / (1E7 * 60 * 60 * 24 * 30))
        }
    if intervals % (1E7 * 60 * 60 * 24 * 7) == 0:
        return {
            "unit": "weeks",
            "value": int(intervals / (1E7 * 60 * 60 * 24 * 7))
        }
    if intervals % (1E7 * 60 * 60 * 24) == 0:
        return {
            "unit": "days",
            "value": int(intervals / (1E7 * 60 * 60 * 24))
        }
    if intervals % (1E7 * 60 * 60) == 0:
        return {
            "unit": "hours",
            "value": int(intervals / (1E7 * 60 * 60))
        }
    return {
        "unit": "filetime",
        "value": filetime
    }

# Convert directory string "CN=someName,O=someOrg,C=EX", to
#   CN:
#   - someName
#   O:
#   - someOrg
#   C:
#   - EX
# TODO: Handle escaped values (e.g. \=) and parsing of RDNs
def dictionary_string_to_dict(dictionary_string):
    dict = {}
    for attribute_pair in dictionary_string.split(','):
        (_key, _value) = attribute_pair.split('=')
        if _key.lower() not in dict:
            dict[_key.lower()] = [ _value ]
        else:
            dict[_key.lower()].append(_value)
    return dict

argparser = argparse.ArgumentParser(description = 'Parse certificate templates exported from Active Directory into human-readable YAML.')
argparser.add_argument('--debug', help = 'Enable debug logging to syslog.', action = 'store_true')
argparser.add_argument('--file', help = 'Path to a file with LDIF object(s) to parse.', required = True)
args = argparser.parse_args()

# Determine if an LDAP object represents an AD CS certificate template.
def is_certificate_template(records):
    return 'pKICertificateTemplate' in records['objectClass']

log = logging.getLogger('syslog')
if args.debug:
    log.setLevel(logging.DEBUG)
else:
    log.setLevel(logging.INFO)
handler = logging.handlers.SysLogHandler(address = '/dev/log')
log.addHandler(handler)

# Remove these attributes from the output
ignored_attributes = [
    'changetype',
    'cn', # This is the same as the 'name'
    'instanceType',
    'dSCorePropagationData',
    'showInAdvancedViewOnly',
    'uSNChanged',
    'uSNCreated'
]

output = {
    'templates': [],
    'certificate_authorities': [],
}

if args.file.startswith('/') or args.file.startswith('~'):
    # Use absolute path
    parser = LDIFParser(
        input_file = open(args.file, "rb"),
        ignored_attr_types = ignored_attributes)
else:
    # Assume path relative to the current working directory
    parser = LDIFParser(
        input_file = open(os.path.join(os.getcwd(), args.file), "rb"),
        ignored_attr_types = ignored_attributes)

for dn, records in parser.parse():
    if not is_certificate_template(records):
        log.debug('Skipped object which is not a certificate template: %s' % dn)
        continue
    log.info('Parsed certificate template: %s' % dn)
    template = {}
    for key in records:
        if key == 'distinguishedName':
            template[key] = dictionary_string_to_dict(records[key][0])
            continue
        # https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-crtd/6cc7eb79-3e84-477a-b398-b0ff2b68a6c0
        if key == 'flags':
            flags = []
            flag_value = int(records[key][0])
            if flag_value & 0x00000020:
                flags.append('CT_FLAG_AUTO_ENROLLMENT')
            if flag_value & 0x00000040:
                flags.append('CT_FLAG_MACHINE_TYPE')
            if flag_value & 0x00000080:
                flags.append('CT_FLAG_IS_CA')
            if flag_value & 0x00000200:
                flags.append('CT_FLAG_ADD_TEMPLATE_NAME')
            if flag_value & 0x00000800:
                flags.append('CT_FLAG_IS_CROSS_CA')
            if flag_value & 0x00010000:
                flags.append('CT_FLAG_IS_DEFAULT')
            if flag_value & 0x00020000:
                flags.append('CT_FLAG_IS_MODIFIED')
            if flag_value & 0x00000400:
                flags.append('CT_FLAG_DONOTPERSISTINDB')
            if flag_value & 0x00000002:
                flags.append('CT_FLAG_ADD_EMAIL')
            if flag_value & 0x00000008:
                flags.append('CT_FLAG_PUBLISH_TO_DS')
            if flag_value & 0x00000010:
                flags.append('CT_FLAG_EXPORTABLE_KEY')
            template[key] = flags
            continue
        if key == 'msPKI-Enrollment-Flag':
            flags = []
            val = int(records[key][0])
            if val & 0x00000001:
                flags.append('CT_FLAG_INCLUDE_SYMMETRIC_ALGORITHMS')
            if val & 0x00000002:
                flags.append('CT_FLAG_PEND_ALL_REQUESTS')
            if val & 0x00000004:
                flags.append('CT_FLAG_PUBLISH_TO_KRA_CONTAINER')
            if val & 0x00000008:
                flags.append('CT_FLAG_PUBLISH_TO_DS')
            if val & 0x00000010:
                flags.append('CT_FLAG_AUTO_ENROLLMENT_CHECK_USER_DS_CERTIFICATE')
            if val & 0x00000020:
                flags.append('CT_FLAG_AUTO_ENROLLMENT')
            if val & 0x00000040:
                flags.append('CT_FLAG_PREVIOUS_APPROVAL_VALIDATE_REENROLLMENT')
            if val & 0x00000100:
                flags.append('CT_FLAG_USER_INTERACTION_REQUIRED')
            if val & 0x00000400:
                flags.append('CT_FLAG_REMOVE_INVALID_CERTIFICATE_FROM_PERSONAL_STORE')
            if val & 0x00000800:
                flags.append('CT_FLAG_ALLOW_ENROLL_ON_BEHALF_OF')
            if val & 0x00001000:
                flags.append('CT_FLAG_ADD_OCSP_NOCHECK')
            if val & 0x00002000:
                flags.append('CT_FLAG_ENABLE_KEY_REUSE_ON_NT_TOKEN_KEYSET_STORAGE_FULL')
            if val & 0x00004000:
                flags.append('CT_FLAG_NOREVOCATIONINFOINISSUEDCERTS')
            if val & 0x00008000:
                flags.append('CT_FLAG_INCLUDE_BASIC_CONSTRAINTS_FOR_EE_CERTS')
            if val & 0x00010000:
                flags.append('CT_FLAG_ALLOW_PREVIOUS_APPROVAL_KEYBASEDRENEWAL_VALIDATE_REENROLLMENT')
            if val & 0x00020000:
                flags.append('CT_FLAG_ISSUANCE_POLICIES_FROM_REQUEST')
            if val & 0x00040000:
                flags.append('CT_FLAG_SKIP_AUTO_RENEWAL')
            template[key] = flags
            continue
        if key == 'msPKI-Private-Key-Flag':
            flags = []
            val = int(records[key][0])
            if val & 0x00000001:
                flags.append('CT_FLAG_REQUIRE_PRIVATE_KEY_ARCHIVAL')
            if val & 0x00000010:
                flags.append('CT_FLAG_EXPORTABLE_KEY')
            if val & 0x00000020:
                flags.append('CT_FLAG_STRONG_KEY_PROTECTION_REQUIRED')
            if val & 0x00000040:
                flags.append('CT_FLAG_REQUIRE_ALTERNATE_SIGNATURE_ALGORITHM')
            if val & 0x00000080:
                flags.append('CT_FLAG_REQUIRE_SAME_KEY_RENEWAL')
            if val & 0x00000100:
                flags.append('CT_FLAG_USE_LEGACY_PROVIDER')
            if val & 0x00002000:
                flags.append('CT_FLAG_ATTEST_REQUIRED')
            if val & 0x00001000:
                flags.append('CT_FLAG_ATTEST_PREFERRED')
            if val & 0x00004000:
                flags.append('CT_FLAG_ATTESTATION_WITHOUT_POLICY')
            if val & 0x00000200:
                flags.append('CT_FLAG_EK_TRUST_ON_USE')
            if val & 0x00000400:
                flags.append('CT_FLAG_EK_VALIDATE_CERT')
            if val & 0x00000800:
                flags.append('CT_FLAG_EK_VALIDATE_KEY')
            if val & 0x00200000:
                flags.append('CT_FLAG_HELLO_LOGON_KEY')
            if len(flags) == 0:
                flags.append('CT_FLAG_ATTEST_NONE')
            template[key] = flags
            continue
        # Unpack from LDIF
        #   msPKI-RA-Application-Policies: "key`datatype`value"
        # to YML
        #   msPKI-RA-Application-Policies:
        #   - key: "value"
        # https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-crtd/3fe798de-6252-4350-aace-f418603ddeda
        if key == 'msPKI-RA-Application-Policies':
            schema_version = int(records['msPKI-Template-Schema-Version'][0])
            use_legacy_provider = int(records['msPKI-Private-Key-Flag'][0]) & 0x00002000
            if schema_version in [ 1, 2 ] or (schema_version == 4 and use_legacy_provider):
                template[key] = records[key][0].split(',')
            else:
                pieces = records[key][0].split('`')
                policies = {}
                for i in range(0, len(pieces) - 3, 3):
                    _key = pieces[i]
                    _value = pieces[i + 2]
                    if _key == 'msPKI-RA-Application-Policies':
                        _value = _value.split(',')
                    if _key == 'msPKI-Symmetric-Key-Length':
                        _value = int(_value)
                    if _key == 'msPKI-Key-Usage':
                        _flags = []
                        if int(_value) & 0x00000001:
                            _flags.append('NCRYPT_ALLOW_DECRYPT_FLAG')
                        if int(_value) & 0x00000002:
                            _flags.append('NCRYPT_ALLOW_SIGNING_FLAG')
                        if int(_value) & 0x00000004:
                            _flags.append('NCRYPT_ALLOW_KEY_AGREEMENT_FLAG')
                        if int(_value) & 0x00ffffff:
                            _flags.append('NCRYPT_ALLOW_ALL_USAGES')
                        _value = _flags
                    policies[_key.lower().replace('-', '_')] = _value
                template[key] = policies
            continue
        # https://docs.microsoft.com/en-us/windows/win32/adschema/a-mspki-ra-signature
        if key == 'msPKI-RA-Signature':
            template[key] = int(records[key][0])
            continue
        if key == 'objectCategory':
            template[key] = dictionary_string_to_dict(records[key][0])
            continue
        # https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-crtd/63c334a0-7a0c-49c5-a95c-c6daa8410a7d
        if key == 'pKIOverlapPeriod' or key == 'pKIExpirationPeriod':
            template[key] = filetime_to_dict(records[key][0])
            continue
        # https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-crtd/ee5d75a7-8416-4a92-b708-ee8f6e8baffb
        if key == 'pKIDefaultKeySpec':
            pki_default_key_spec = int(records[key][0])
            if pki_default_key_spec == 1:
                template[key] = 'AT_KEYEXCHANGE'
            elif pki_default_key_spec == 2:
                template[key] = 'AT_SIGNATURE'
            else:
                template[key] = pki_default_key_spec
            continue
        # https://ldapwiki.com/wiki/KeyUsage
        if key == 'pKIKeyUsage':
            key_usages = []
            if records[key][0][0] == ' ':
                log.debug('ignoring bad KU bits')
                continue
            key_usage_bits = records[key][0][0]
            if  key_usage_bits & (0b1 << 7):
                key_usages.append('Digital Signature')
            if key_usage_bits & (0b1 << 6):
                key_usages.append('Content Commitment')
            if key_usage_bits & (0b1 << 5):
                key_usages.append('Key Encipherment')
            if key_usage_bits & (0b1 << 4):
                key_usages.append('Data Encipherment')
            if key_usage_bits & (0b1 << 3):
                key_usages.append('Key Agreement')
            if key_usage_bits & (0b1 << 2):
                key_usages.append('Key Certificate Signing')
            if key_usage_bits & (0b1 << 1):
                key_usages.append('CRL Signing')
            # TODO: Handle encryptOnly and decryptOnly KU
            template[key] = key_usages
            continue
        if key == 'pKIExtendedKeyUsage':
            extended_key_usages = []
            for eku_oid in records[key]:
                if eku_oid == '1.3.6.1.5.5.7.3.1':
                    extended_key_usages.append('TLS Server Authentication')
                elif eku_oid == '1.3.6.1.5.5.7.3.2':
                    extended_key_usages.append('TLS Client Authentication')
                elif eku_oid == '1.3.6.1.4.1.311.10.3.4':
                    extended_key_usages.append('EFS File System Encryption')
                elif eku_oid == '1.3.6.1.5.5.7.3.4':
                    extended_key_usages.append('Email Protection')
                else:
                    extended_key_usages.append(eku_oid)
            template[key] = extended_key_usages
            continue
        # https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-crtd/1192823c-d839-4bc3-9b6b-fa8c53507ae1
        if key == 'msPKI-Certificate-Name-Flag':
            val = int(records[key][0])
            flags = []
            if val & 0x00000001:
                flags.append("CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT")
            if val & 0x00010000:
                flags.append("CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT_ALT_NAME")
            if val & 0x00400000:
                flags.append("CT_FLAG_SUBJECT_ALT_REQUIRE_DOMAIN_DNS")
            if val & 0x00800000:
                flags.append("CT_FLAG_SUBJECT_ALT_REQUIRE_SPN")
            if val & 0x01000000:
                flags.append("CT_FLAG_SUBJECT_ALT_REQUIRE_DIRECTORY_GUID")
            if val & 0x02000000:
                flags.append("CT_FLAG_SUBJECT_ALT_REQUIRE_UPN")
            if val & 0x04000000:
                flags.append("CT_FLAG_SUBJECT_ALT_REQUIRE_EMAIL")
            if val & 0x08000000:
                flags.append("CT_FLAG_SUBJECT_ALT_REQUIRE_DNS")
            if val & 0x10000000:
                flags.append("CT_FLAG_SUBJECT_REQUIRE_DNS_AS_CN")
            if val & 0x20000000:
                flags.append("CT_FLAG_SUBJECT_REQUIRE_EMAIL")
            if val & 0x40000000:
                flags.append("CT_FLAG_SUBJECT_REQUIRE_COMMON_NAME")
            if val & 0x80000000:
                flags.append("CT_FLAG_SUBJECT_REQUIRE_DIRECTORY_PATH")
            if val & 0x00000008:
                flags.append("CT_FLAG_OLD_CERT_SUPPLIES_SUBJECT_AND_ALT_NAME")
            template[key] = flags
            continue

        # Convert these values into human-readable dates
        if key in [ 'whenChanged', 'whenCreated' ]:
            date = datetime.strptime(records[key][0], '%Y%m%d%H%M%S.0Z')
            template[key] = date.strftime('%Y-%m-%d %H:%M:%S')
            continue
        # Convert these values into integers
        if key in [
            'msPKI-Template-Minor-Revision',
            'msPKI-Template-Schema-Version',
            'msPKI-Minimal-Key-Size',
            'pKIMaxIssuingDepth',
            'revision' ]:
            template[key] = int(records[key][0])
            continue

        if len(records[key]) == 1:
            template[key] = records[key][0]
        else:
            template[key] = records[key]

    # Normalise keys msPKI-Blah-Blah -> mspki_blah_blah
    template = { k.lower().replace('-', '_'): v for k, v in template.items() }
    output['templates'].append(template)

json_data = json.dumps(output, cls = HexEncoder)
yaml_data = yaml.dump(yaml.load(json_data,
    Loader = yaml.SafeLoader),
    default_flow_style = False)
print(yaml_data)