#!/usr/bin/env python
# coding: utf-8
# In[23]:
class Foo(object):
    def __init__(self, val):
        print('__init__')
        self.val = val
    
    def __call__(self, a, b, c):
        print('__call__')        
        print('a, b, c = {}'.format(str([a,b,c])))
# __init__
obj = Foo(10)
# __call__
obj(1,2,3)
        
# In[7]:
fibonacci = [0,1,1,2,3,5,8,13,21,34,55]
odd_numbers = list(filter(lambda x: x % 2, fibonacci))
print(odd_numbers)
# In[11]:
# Python 3 returns iterator
list(map(str, range(10)))
# In[12]:
C = [39.2, 36.5, 37.3, 38, 37.8]
F = list(map(lambda x: (float(9)/5)*x + 32, C))
print(F)
# In[13]:
import functools
functools.reduce(lambda x,y: x+y, [47,11,42,13])
# In[28]:
import functools
def welcome(f):
    @functools.wraps(f) # this is to make docstring correct
    def decorated(*args, **kwargs):
        print('welcome!')
        
        return f(*args, **kwargs)
    return decorated
print('------ without decorator --------')
def foo(name):
    print(name)
foo('pppk')
print('------ with decorator --------')
@welcome
def foo(name):
    print(name)
foo('pppk')
# In[32]:
def welcome(greeting):
    def decorator(f):
        @functools.wraps(f) # this is to make docstring correct
        def decorated(*args, **kwargs):
            print(greeting)
            return f(*args, **kwargs)
        return decorated
    return decorator
@welcome('您好')
@welcome('歡迎光臨')
def foo(name):
    print(name)
foo('pppk')
# In[4]:
from functools import wraps
class Foo(object):
    def __init__(self):
        self.greeting = "hello"
        pass
    
    def my_greeting(self):
        print(self.greeting)
    
    def _decor(f):
        @wraps(f)
        def wrapped(inst, *args, **kwargs):
            inst.my_greeting()
            # the member function to be executed
            result = f(inst, *args, **kwargs)
            inst.my_greeting()
            
            return result
        
        return wrapped
    
    @_decor
    def my_func(self):
        print('my_func')
        
Foo().my_func()
# In[50]:
class Foo(object):
    pass
print(Foo)
# you use class Foo to create an instance
obj = Foo()
print('{}: type = {}'.format(obj, type(obj)))
print('obj class: {}'.format(obj.__class__))
print('')
# but actually class Foo is also an object (class object) so you can assign attributes to it
print(hasattr(Foo, 'new_attr'))
Foo.new_attr = 'new'
print(hasattr(Foo, 'new_attr'))
print('')
# class object Foo is created by its meta class, type
print('obj class.class: {}'.format(obj.__class__.__class__))
print('')
# you can also do it yourself, without class definition
Foo = type('Foo', (object,), {'new_attr': 'new'})
print(Foo)
print(hasattr(Foo, 'new_attr'))
# In[82]:
# remember that `type` is actually a class like `str` and `int`
# so you can inherit from it
class UpperAttrMetaclass(type):
    # __new__ is the method called before __init__
    # it's the method that creates the object and returns it
    # while __init__ just initializes the object passed as parameter
    # you rarely use __new__, except when you want to control how the object
    # is created.
    # here the created object is the class, and we want to customize it
    # so we override __new__
    # you can do some stuff in __init__ too if you wish
    # some advanced use involves overriding __call__ as well, but we won't
    def __new__(cls, clsname, bases, dct):
        print('UpperAttrMetaClass: __new__')
        uppercase_attr = {}
        for name, val in dct.items():
            if not name.startswith('__'):
                uppercase_attr[name.upper()] = val
            else:
                uppercase_attr[name] = val
        return super(UpperAttrMetaclass, cls).__new__(cls, clsname, bases, uppercase_attr)        
    
class Foo(metaclass=UpperAttrMetaclass):
    # the following line is for python 2, python 3 use metaclass=xxx in declaration
    #__metaclass__ = UpperAttrMetaclass
    
    name = 'foo'
    address = 'home'
foo = Foo()
print(foo.__class__.__class__)
print(dir(foo))
# In[86]:
class MetaSingleton(type):
    instance = None
    
    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(MetaSingleton, cls).__call__(*args, **kw)
            
        return cls.instance
class Foo(metaclass=MetaSingleton):
    pass
a = Foo()
b = Foo()
    
print(a is b)
# In[5]:
def add(x, y):
    return x + y
print(add(1, 2))
add = lambda x, y: x + y
print(add(1, 2))
# generally use in
mult3 = filter(lambda x: x % 3 == 0, [1, 2, 3, 4, 5, 6, 7, 8, 9])
print(list(mult3))
# In[7]:
import warnings
# warning
warnings.warn("deprecated", DeprecationWarning)
# wrap it in warning context manager
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    
    # the warning wouldn't show now
    warnings.warn("deprecated", DeprecationWarning)
    
    '''
    Now import packages with DeprecationWarning is fine, such as xgboost
    '''
    #import xgboost
    
# In[4]:
10 * 20
# In[5]:
_
# In[8]:
for _ in range(5):
    print("do something, don't care the index")
# In[3]:
import functools
@functools.lru_cache(maxsize=64)
def fib(n):
    if n < 2:
        return n
    
    return fib(n-1) + fib(n-2)
for n in range(16): 
    fib(n)
fib.cache_info()
# In[16]:
import mmap
FILE_SIZE = 1000
with mmap.mmap(-1, FILE_SIZE) as f:
    f.write(b'test line 1\n')
    f.write(b'test line 2\n')
    f.seek(0)
    print(f.readline())
    print(f.readline())
   
# In[1]:
class MyClass(object):
    def __init__(self):
        self.x = None
        self.y = None
        self._setup = False
        
    @property
    def setup(self):
        if not self._setup:
            self.x = 10
            self.y = 20
            self._setup = True
        
        return self._setup
c = MyClass()
c.setup
print(c._setup)
# In[3]:
import time
'''
Eagerly generate all values and return
'''
def compute():
    ret = []
    
    for i in range(10):
        ret.append(i)
        time.sleep(.5)
    
    return ret
print('--- eager version ---')    
for v in compute():
    print(v)
    
def compute():
    for i in range(10):
        time.sleep(.5) # simulate heavy operation such as DB query
        yield i
print('--- generator version ---')    
for v in compute():
    print(v)
    
    
    