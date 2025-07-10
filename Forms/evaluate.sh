#! /bin/bash

cd /home/.evaluationScripts/
[ -f forms-1.html ] && rm forms-1.html
cp /home/labDirectory/forms-1.html /home/.evaluationScripts/
python3 /home/.evaluationScripts/autograder.py
