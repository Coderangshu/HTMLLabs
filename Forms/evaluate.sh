#! /bin/bash

cd /home/.evaluationScripts/
[ -f forms.html ] && rm forms.html
cp /home/labDirectory/forms.html /home/.evaluationScripts/
python3 /home/.evaluationScripts/autograder.py
