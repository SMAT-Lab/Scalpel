#!/usr/bin/env python
# coding: utf-8
# In[1]:
def fibonacci_recursive_bad(n):
    '''
    Returns the nth fibonacci number. Calls itself recursively to compute
    the two previous fibonacci numbers and adds them together.
    '''
    if n == 0 or n == 1:
        return n
    else:
        return fibonacci_recursive_bad(n-2) + fibonacci_recursive_bad(n-1)
# In[2]:
get_ipython().run_cell_magic('time', '', 'fibonacci_recursive_bad(30)')
# In[3]:
#%%time
# fibonacci_recursive_bad(200), had to interrupt this as it was taking too long
# In[4]:
def fibonacci_recursive_helper(fibo_2, fibo_1, countdown):
    '''
    Calculates fibonacci numbers. fibo_2 is the previous to
    the previous fibonacci number, a.k.a. Fib(n-2), fibo_1
    is the previous fibonacci number, a.k.a. Fib(n-1), countdown
    is the number of fibonacci calculations that are yet to be performed.
    The recursion chain stops once the countdown is zero, in which case the
    result is actually the fibonaci calculated by the previous recursive
    call, a.k.a fibo_1.
    '''
    if countdown == 0:
        return fibo_1
    else:
        return fibonacci_recursive_helper(fibo_1, fibo_2 + fibo_1, countdown-1)
def fibonacci_recursive_good(n):
    '''
    Returns the nth fibonacci number. Calls fibonacci_recursive_helper
    by passing the values of the 0th and the 1st fibonacci number,
    as well as a "countdown" of "next fibonacci number calculations"
    to perform, n is reduced to account for the fact that the 0th
    and the 1st fibonacci numbers don't need to be calculated, as they
    are given.
    '''
    if n == 0 or n == 1:
        return n
    else:
        return fibonacci_recursive_helper(fibo_2=0, fibo_1=1, countdown=n-1)
# In[5]:
get_ipython().run_cell_magic('time', '', 'fibonacci_recursive_good(30)')
# In[6]:
get_ipython().run_cell_magic('time', '', 'fibonacci_recursive_good(200)')