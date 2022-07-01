'''
The objective of this script is to process as many files as possible to test the robustness of the framework. 

'''

from scalpel.cfg.builder import CFGBuilder
from scalpel.cfg.model import Block
from scalpel.util import get_path_by_ext
import os
import sys
import glob 


#@profile
def test_all():
    target_dir = "./tests/test-cases/cfg-tests"
    all_files =  get_path_by_ext(target_dir)
    
    print(f"In total, there are {len(all_files)} files to be tested!")
    for idx, fn in enumerate(all_files):
        builder = CFGBuilder()
        print(os.path.basename(fn), idx)
        try:
            cfg = builder.build_from_file(os.path.basename(fn), fn)
        except SyntaxError as e:
            pass
     
    return 0

    
    
         
    print("Number of py files: "+str(file_no))
    print("Number of exception: "+str(except_no))


def main():
    test_all()
    #src = open(src_file).read()
    #builder = CFGBuilder()
    #cfg = builder.build_from_file("test", src_file)


if __name__ == '__main__':
    main() 

