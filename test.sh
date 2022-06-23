#!/bin/bash

tests=$(find tests -type f -name "*.py")
for t in ${tests}
do
  python3 -m unittest ${t}
done
