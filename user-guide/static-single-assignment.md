
## SSA & Constant Propagation

Static Single Assignment (SSA) is a technique of IR in the compiling thoery, it also shows great benefits to static anaysis tasks such as constant propagation, Dead code elimination and etc.

Constant propagation are also a matured technqiue in static anaysis. It is the process to evaluating or recognize the actual constant values or expressions at a particular program point.  This is realized by utilizing control flow and data flow information. Determining the possible values for variables before runtime gives great benefits to software anaysis. For instance, with constant value propagation, we can detect and remove dead code or perfrom type checking. 

 
In scalpel, we implenent constant progagtion along with the SSA for execution effiency.  

### How to use the SSA module and Constant Propagation

The demo input python program we will be using is as follows.
```python
code_str="""
def func(a:int)->str:
    b = 10
    if b>0:
        a = str(a)
    else:
        a = 10
    return a
"""
```
It can be seen from the above code, the variable a has two possible values. By utilizing the phi functions in SSA, we are able to infer the actual return value will has two potenial values. We follow the algorithms from [4]. The input parameter for SSA computing is the CFG as it represent how the code blocks are organized in the program exection flow. 

```python
# create a mnode object.
mnode = MNode("local")
# feed the code snippet
mnode.source = code_str 
mnode.gen_ast()
 # get the cfg
cfg = mnode.gen_cfg() 
m_ssa = SSA()
# do the job
ssa_results, const_dict = m_ssa.compute_SSA(cfg) 
for block_id, stmt_res in ssa_results.items():
  print("These are the results for block ".format(blck_id))
  print(stmt_res)
for name, value in const_dict.items():
  print(name, value)
print(ssa_results)

```

Please note that the funciton ` compute_SSA` returns two dictionary. For the first one, the key values are block numbers in the given CFG, the value is a list of dictioanary, each of which corresponds one statement in the block. Therefore, the `ssa_results[1]` is a list SSA representations for the first block. If we inspect the the last block (print statement is located), the results are 

```python
 [{'print': [], 'a': [0, 1]}]}
```
This is due to the variable a can take values from two assignments. 


The second one named `const_dict` are the global constant values for the numbered identifiers. For instance, `const_dict["(a,0)"]` are the constant value after the first assignment to variable `a`. The constant values in this module are the Python ```ast.expr``` type.  In this participular case `(a,0)` is an `ast.BinOp` type and `(a,1)` is an `ast.Num` type.
The tutorial code can be found here:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[SSA_example.py](example.com)

### APIs
[Place Holder](placeholder.com)\
[Place Holder](placeholder.com)\
[Place Holder](placeholder.com)\
[Place Holder](placeholder.com)

### Reference
1. [A Simple, Fast Dominance Algorithm](https://www.cs.rice.edu/~keith/EMBED/dom.pdf) Keith D. Cooper, Timothy J. Harvey, and Ken Kennedy
2. [COS598C Advanced Compilers](https://www.cs.princeton.edu/courses/archive/spr04/cos598C/lectures/02-ControlFlow.pdf), Princeton University
3. [CMU 15-411 Compiler Design](https://www.cs.cmu.edu/~fp/courses/15411-f08/lectures/09-ssa.pdf)
4. [Harvard CS252r Spring 2011](https://groups.seas.harvard.edu/courses/cs252/2011sp/slides/Lec04-SSA.pdf)