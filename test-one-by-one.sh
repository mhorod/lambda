#!/bin/bash

for file in $(find tests -type f -name "test_*.py") 
do
  echo "Running ${file}"
  echo
  python3 -m unittest -v ${file} 2>&1 | sed -e 's/(.*)//' -e 's/test_//' -e 's/_/ /g'
  echo ""
done
