#!/bin/bash
files=$(find tests -type f -name "test_*.py")
python3 -m unittest -v ${files}
