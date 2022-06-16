#!/bin/sh
pandoc -V geometry:margin=1in --pdf-engine=pdflatex -o assessment-instructions.pdf assessment-instructions.md
zip "../../release/pki-assessment-bundle.zip" "ADCS Collector-v1.0.35.exe" "assessment-instructions.pdf"
rm assessment-instructions.pdf