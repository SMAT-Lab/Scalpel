"""
Static Single Assignment (SSA) is a technique of IR in the compiling thoery, it also shows great benefits to static anaysis tasks such as constant propagation, dead code elimination and etc.
Constant propagation is also a matured technique in static anaysis. 
It is the process of evaluating or recognizing the actual constant values or expressions at a particular program point. This is realized by utilizing control flow and data flow information. Determining the possible values for variables before runtime gives great benefits to software anaysis. 
For instance, with constant value propagation, we can detect and remove dead code or perfrom type checking.
In scalpel, we implement constant propagation along with the SSA for execution efficiency.
"""
__slots__ = ["const"]