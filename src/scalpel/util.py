import ast
import builtins
import operator
import sys 
import os


# scan a folder recurisively and return all files ending with the flag
def get_path_by_ext(root_dir, flag=".py"):
    paths = []
    for root, dirs, files in os.walk(root_dir):
        files = [
            f for f in files if not f[0] == "."
        ]  # skip hidden files such as git files
        dirs[:] = [d for d in dirs if not d[0] == "."]
        for f in files:
            if f.endswith(flag):
                paths.append(os.path.join(root, f))
    return paths

def check_python_version():
    """check Python version"""
    # Check for known bad Python versions.
    if sys.version_info[:2] < (3, 8):
        sys.exit("Running Scalpel with Python 3.8 or lower is not supported; ")

