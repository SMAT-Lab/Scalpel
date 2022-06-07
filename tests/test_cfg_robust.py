'''
The objective of this script is to process as many files as possible to test the robustness of the framework. 

'''

from scalpel.cfg.builder import CFGBuilder
from scalpel.cfg.model import Block
from scalpel.util import get_path_by_ext
import os
import sys
import glob 

def test_all():
    target_dir = "./cfg_robust_cases/"
    all_files =  get_path_by_ext(target_dir)
    print(f"In total, there are {len(all_files)} files to be tested!")
    for fn in all_files:
        builder = CFGBuilder()
        print(os.path.basename(fn), fn)
        cfg = builder.build_from_file(os.path.basename(fn), fn)

def main():
    test_all()

if __name__ == '__main__':
    main() 

