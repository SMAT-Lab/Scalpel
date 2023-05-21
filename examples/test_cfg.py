import sys
sys.path.append('../src/')
from scalpel.cfg import CFGBuilder

src  = """
try:
    a = open("test.txt", "r")
    v = a.read()
    a.close()
except IOError:
    v = "ioError"
except:
    v = "otherError"
finally:
    a = 123
"""
cfg_five = CFGBuilder().build_from_src("divide", src)
cfg_five.build_visual('png')
