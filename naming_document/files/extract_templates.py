#
# Script for extracting templates from an LDIF file exported from AD.
#
# Each template is stored in a separate file named <TemplateName>.ldf
# where <TemplateName> is the name of the template.
#
# Usage:
#
#   python3 extract_templates.py --file <ExportedFile.ldf> \
#       --output-directory <OutputDirectory>

import argparse
import os
from os import path

def is_certificate_template(lines):
    for line in lines:
        if line.startswith('objectClass: pKICertificateTemplate'):
            return True
    return False

def write_lines(lines, directory):
    if not path.exists(directory):
        os.mkdir(directory)
    for line in lines:
        if line.startswith('cn:'):
            file_name = line.split(':')[1].strip() + ".ldf"
    with open(path.join(directory, file_name), 'w') as output_file:
        for line in lines:
            if line != '\r\n' and line != '\n':
                output_file.write(line)

argparser = argparse.ArgumentParser(description = 'Extract certificate templates from an LDIF file exported from AD.')
argparser.add_argument('--file',
    required = True,
    help = 'Path to a file with LDIF object(s) to process.')
argparser.add_argument('--output-directory',
    required = True,
    help = 'Path to a directory where the extracted templates will be stored. The directory is created if it does not exist.')
args = argparser.parse_args()

# Process the input file line by line
lines = []
with open(args.file, 'r') as file:
    for line in file.readlines():
        lines.append(line)
#        print("Read line: '{}'".format(line.replace('\n', '')))
        if line == '\r\n' or line == '\n':
            if is_certificate_template(lines):
                write_lines(lines, args.output_directory)
            lines = []
if is_certificate_template(lines):
    write_lines(lines, args.output_directory)