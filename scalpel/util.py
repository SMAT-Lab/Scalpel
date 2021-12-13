import os


# scan a folder recurisively and return all files ending with the flag
def get_path_by_ext(root_dir, flag='.py'):
    paths = []
    for root, dirs, files in os.walk(root_dir):
        files = [f for f in files if not f[0] == '.']  # skip hidden files such as git files
        dirs[:] = [d for d in dirs if not d[0] == '.']
        for f in files:
            if f.endswith(flag):
                paths.append(os.path.join(root, f))
    return paths
