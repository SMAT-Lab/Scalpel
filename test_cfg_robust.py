from scalpel.cfg.builder import CFGBuilder
import os
import sys
import glob


def test_all():

    os_projects_path = "./test-cases/cfg-tests/"
    except_no = 0
    file_no = 0
    error_log = "error_log_cfg_robust.txt"

    files = glob.glob(os_projects_path + '*.py', recursive=True)
    for file_path in files:
        print(file_path)
        file_no += 1
        try:
            builder = CFGBuilder()
            cfg = builder.build_from_file("test", file_path)
            for i, block in enumerate(cfg):
                value = cfg.get_return_value(block)
                line_no = block.at()
                # calls = block.get_calls()
            graph = cfg.build_visual("pdf")
        except Exception as e:
            print(e)
            with open(error_log, 'a') as f:
                f.write("File: {} ".format(file_path))
                f.write(str(e))
                f.write("\n")
            except_no += 1

    print("Number of py files: "+str(file_no))
    print("Number of exception: "+str(except_no))

def main():
    src_file = sys.argv[1]
    src = open(src_file).read()
    builder = CFGBuilder()
    cfg = builder.build_from_file("test", src_file)
    for i, block in enumerate(cfg):
        value = cfg.get_return_value(block)
        line_no = block.at()
        calls = block.get_calls()
    graph = cfg.build_visual("pdf")


if __name__ == '__main__':
    test_all()



