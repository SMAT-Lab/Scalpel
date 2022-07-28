#!/bin/bash

for ((c=6; c<=10; c++)) # From python 3.6 to 3.10
do
  printf "${GREEN}Testing for python3.%s ${NC}\n" "$c"
  conda activate scalpel-python3."$c"
  pytest
  conda deactivate
done