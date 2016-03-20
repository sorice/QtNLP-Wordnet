#!/bin/bash

# adapted from MediaMorph Project
# Thanks guys !!! Awesome script !!!

# Converts all .ui files in current directory into .py files
for d in `ls *.ui`; do
  pyuic4 $d -o "`echo $d | perl -pe 's/\\.[^.]+$//' `_UI.py"
done

# NOTICE: after running this script you might need to update the
#         resources file too, run res2py.sh script if needed
