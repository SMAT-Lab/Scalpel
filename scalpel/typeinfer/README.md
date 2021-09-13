## Scalpel Type Inference Module

### Heuristics Used

| No.    | Code Example                         | Explanation
| ------ | ------------------------------       | ---------------------------------------------------------
| 1      |  fun1(): return fun2()               | fun1 and fun2 shared same return type
| 2      |  fun1(param1), func1(fun2())         | fun2 has same return type as variable param1
| 3      |  fun1().fun2()                       | fun1's return type should have defined fun2
| 4      |  if/while fun1():                    | fun1's return type is boolean
| 5      |  fun1() OP x x OP fun1()             | fun1’s return type equals to the type of variable x if OP is one of the following binary opera- tions {==, !=, +}. For other binary operators, fun1’s return type will be regarded as numbers.
| 6      |  a = fun1(); a()                     | fun1's return type is a function
| 7      |  if isinstance(fun1(),typename)      | fun1’s returns type could be typename
| 8      |  def fun1(x); y= "hello"; fun1(y);   | fun1’s argument x is the same type as y
| 8      |  Ruby paper !                        | 

To deduce types using these heuristics we need the ability to:
- [ ] Track all variable assignments
- [ ] Track where functions are called and whether variables are assigned to their output (heuristic 1)
- [ ] Get information about imported functions, variables etc. Typeshed and running the module on dependencies? (heuristic 1)
- [ ] Track function inputs (heuristic 2)
- [ ] Assess classes and store references to their methods. Need to be able to quickly lookup what class a function could have been defined in (heuristic 3)
- [ ] Track binary operations on variables and function outputs (heuristic 6)
- [ ] Track whether function output is invoked as a callable (heuristic 6)
- [ ] Track usage of isinstance() (heuristic 7)

__
