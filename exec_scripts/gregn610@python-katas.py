#!/usr/bin/env python
# coding: utf-8
# In[1]:
get_ipython().getoutput(' file ../data/wordlist.txt')
# In[2]:
get_ipython().getoutput(' tail -50 ../data/wordlist.txt')
# has accented letters and possessive 's es
# In[3]:
import codecs
class AnagramFinder():
    """
    Creates a dictionary of anagrams. 
    Each dict key is a root word with the letters scrambled i.e sorted alphabetically.
    The dict value is a set of anagrams, containing at least the unscrambled root word.
    """
    def __init__(self, dictionary_file, encoding='utf-8'):
        self.dic = {}
        
        with codecs.open(dictionary_file, 'r', encoding) as f:
            for word in f.read().split():
                keyData = ''.join(sorted(list(word)))
                self.dic.setdefault(keyData,set()).add(word)
                        
    def getAnagrams(self, word):
        """
        Returns a set of anagram words
        """
        _wordSorted = ''.join(sorted(list(word)))
        
        # Remember to take the word word out of (differnce) the set of anagrams
        return self.dic.get(_wordSorted, set()).difference({word,})
# In[16]:
from unittest import *
class AnagramFinderTests(TestCase):
    
    @classmethod
    def setUpClass(self):
        self.af = AnagramFinder('../data/wordlist.txt', 'iso-8859-1')
        
    def setUp(self):
        pass
        
    def test_dic_keys(self):
        self.assertEqual(self.af.dic['iknst'], {'stink', 'tinks', 'skint', 'knits'})
        
    def test_getAnagrams1a(self):
        self.assertEqual(self.af.getAnagrams('knits'), {'stink', 'tinks', 'skint'})
        
    def test_getAnagrams1b(self):
        self.assertEqual(self.af.getAnagrams('stink'), {'knits', 'tinks', 'skint'})
        
    def test_anagrams_bulk1(self):
        # Check expected results
        self.testRoots = {
              'kinship' :{ 'pinkish', },
              'enlist'  :{ 'inlets', 'silent', 'tinsel', 'listen', 'elints', },
              'boaster' :{ 'borates', 'rebatos', 'sorbate', 'boaters', },
              'fresher' :{ 'refresh', },
              'sinks'   :{ 'skins', },
              'knits'   :{ 'stink', 'tinks', 'skint', },
              'rots'    :{ 'sort', 'orts','stor', 'tors', }, # example data incorrect, see egreps
        }
        for tk in self.testRoots.keys():
            anagramSet = self.af.getAnagrams(tk)
            self.assertEqual(self.testRoots[tk], anagramSet, "%s returned %s" %(tk, anagramSet))
            
    def test_anagrams_bulk2(self):
        # Check expected results
        self.testRoots = {
            'crepitus'  :{ 'cuprites','pictures','piecrust',},
            'paste'     :{ 'pates','peats','septa','spate','tapes','tepas',},
            'punctilio' :{ 'unpolitic',},
            'sunders'   :{ 'undress',},
        }
        for tk in self.testRoots.keys():
            anagramSet = self.af.getAnagrams(tk)
            self.assertEqual(self.testRoots[tk], anagramSet, "%s returned %s" %(tk, anagramSet))
aft = AnagramFinderTests()
suite = TestLoader().loadTestsFromModule(aft)
TextTestRunner().run(suite)
# In[7]:
''.join(sorted(list('knits')))
# In[8]:
{'skint', 'stink', 'tinks'} == {'skint', 'tinks', 'stink'}
# In[9]:
get_ipython().getoutput(" egrep '^tors$' ../data/wordlist.txt")
# In[10]:
get_ipython().getoutput(" egrep '^orts$' ../data/wordlist.txt")
# In[11]:
get_ipython().getoutput(" egrep '^stor$' ../data/wordlist.txt")
# In[12]:
get_ipython().getoutput(" egrep '^asdf$' ../data/wordlist.txt")
# In[5]:
get_ipython().run_line_magic('time', "af = AnagramFinder('../data/wordlist.txt', 'iso-8859-1')")
# In[6]:
get_ipython().run_line_magic('time', "af.getAnagrams('knits')")
# In[18]:
# Don't count lone words
# Maybe refactor so af.dic doesn't include anagramless keys
print("Found %d sets of anagrams" % len([k for k in af.dic.keys() if len(af.dic[k]) > 1]))
# In[14]:
maxKey= None
maxLen = 0
for k, v in af.dic.items():
    if len(v) > maxLen:
        maxKey = k
        maxLen = len(af.dic[k])
print("Largest set of anagrams is %s" %(af.dic[maxKey]))
        
# In[15]:
maxKey= None
maxLen = 0
tieBreak = 0
for k, v in af.dic.items():
    if ((len(k)) > maxLen) and len(af.dic[k])>1:
        maxLen = len(k)
        tieBreak = len(af.dic[k])
        maxKey = k
    elif ((len(k)) == maxLen):
        if len(af.dic[k]) > tieBreak:
            maxLen = len(k)
            tieBreak = len(af.dic[k])
            maxKey = k
        
print("Longest anagrams are %s " % (af.dic[maxKey]))