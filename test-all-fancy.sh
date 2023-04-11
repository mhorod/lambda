#!/bin/bash
files=$(find tests -type f -name "test_*.py")
python3 -m unittest -v ${files} 2>&1 | sed -e 's/(.*)//' -e 's/test_//' -e 's/_/ /g'
