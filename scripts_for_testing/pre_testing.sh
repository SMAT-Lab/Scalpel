#!/bin/bash
# Before running this script, make sure conda is installed and is correctly configured to interact with shell
GREEN='\033[0;32m'
NC='\033[0m' # No Color
# Creating environments for different python versions
for ((c=5; c<=10; c++)) # From python 3.5 to 3.10
do
  printf "${GREEN}Creating environment for python3.%s ${NC}\n" "$c"
  conda create --name scalpel-python3."$c" python=3."$c"
  conda activate scalpel-python3."$c"
  conda install pytest
  pip install -e .
  conda install graphviz
  conda deactivate
done