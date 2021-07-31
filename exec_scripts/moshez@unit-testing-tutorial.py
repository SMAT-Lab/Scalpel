#!/usr/bin/env python
# coding: utf-8
# In[1]:
import unittest
def run(klass):
    suite = unittest.TestLoader().loadTestsFromTestCase(klass)
    unittest.TextTestRunner(verbosity=2).run(suite)
# In[2]:
class SimpleFailingTest(unittest.TestCase):
    def test_wrong(self):
        self.assertEqual(0, 1)
run(SimpleFailingTest)
# In[8]:
class WeirdFailures(unittest.TestCase):
    def test_greater(self):
        self.assertGreater(0, 1)
    def test_exc(self):
        with self.assertRaises(KeyError):
            a=1
run(WeirdFailures)
# In[11]:
class StateTests(unittest.TestCase):
    def setUp(self):
        self.a = [1,2,3]
    def test_foo(self):
        self.a.sort()
        self.assertGreater(self.a[0], self.a[-1])
    def test_bar(self):
        self.a.reverse()
        self.assertLess(self.a[0], self.a[-1])
run(StateTests)