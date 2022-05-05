"""
This file is a wrapper of the pycg, a practical python call graph generator. Please refer to:
1. https://github.com/vitsalis/PyCG
2. https://pypi.org/project/pycg/
3. Vitalis Salis, Thodoris Sotiropoulos, Panos Louridas, Diomidis Spinellis and Dimitris Mitropoulos. PyCG: Practical
Call Graph Generation in Python. In 43rd International Conference on Software Engineering, ICSE '21, 25–28 May 2021.
"""

from pycg.pycg import CallGraphGenerator as CallGraphGeneratorPyCG
from pycg import formats
import pycg
import pkg_resources
import packaging
from packaging import version
pycg_version = pkg_resources.get_distribution('pycg').version
if packaging.version.Version(pycg_version)>packaging.version.Version("0.0.3"):
    class CallGraphGenerator(CallGraphGeneratorPyCG):
        def __init__(self, entry_points, package, max_iter=-1, operation="call-graph"):
            super().__init__(entry_points, package, max_iter, operation)

    pycg.pycg.CallGraphGeneratorPyCG = CallGraphGenerator
