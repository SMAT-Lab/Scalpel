#!/usr/bin/env python
# coding: utf-8
# In[70]:
fields = ['ITERATION', 'ENERGY', '1e-ENERGY', '2e-ENERGY', 'NORM[dD(SAO)]', 'TOL',
          'Exc', 'N', 'Norm[diis error]']
from fortranformat import FortranRecordReader
FortranRecordReader('(I4,F18.11,F17.7,F17.7,E13.3,E10.2)').read(lines[4])
# In[71]:
from io import StringIO
from pyparsing import Word, nums, Literal, LineStart, LineEnd, OneOrMore
from fortranformat import FortranRecordReader
import pandas as pd
# In[72]:
class FortranLineParser(object):
    def __init__(self, pattern, name=None,
                 skip=None, strip_whitespace=True, map_values=None,
                 after_read_hook=None):
        self._reader = FortranRecordReader(pattern)
        self.name = name
        self._skip = [skip] if isinstance(skip, int) else skip
        self._strip_whitespace = strip_whitespace
        self._map_values = map_values if isinstance(map_values, dict) else None
        self._after_read_hook = after_read_hook
    
    def __call__(self, line):
        data = self._reader.read(line)
        if self._skip:
            skip = self._skip
            data = [_ for i, _ in enumerate(data) if i not in skip]
        if self._strip_whitespace:
            data = [(_.strip() if isinstance(_, str) else _) for _ in data]
        if self._map_values:
            _map = self._map_values
            data = [(_map[_] if _ in _map else _) for _ in data]
        if self._after_read_hook:
            data = self._after_read_hook(data)
        return data
# In[73]:
l = [1,2,3,4,5]
skip = [0,3]
l += skip
l
# In[74]:
class BaseParser(object):
    def __init__(self, raw):
        self.raw = StringIO(raw)
    
    def _scan_forward(self, anchor, before_match=False):
        loc = self.raw.tell()
        scanner = anchor.scanString(self.raw.read())
        match, start, end = next(scanner)
        scanner.close()
        if before_match:
            self.raw.seek(loc + start)
        else:
            self.raw.seek(loc + end)
    
    def _next_content_line(self, skip=0):
        while True:
            line = self.raw.readline()
            if line is '':
                raise RuntimeError('EOF reached')
            if line.strip() is not '':
                if skip > 0:
                    skip -= 1
                else:
                    return line
    
    def _chunks(self, sequence, n):
        """Yield successive n-sized chunks from sequence."""
        for i in range(0, len(sequence), n):
            yield sequence[i:i+n]
# In[75]:
from collections import defaultdict
class VibrSpectrum(BaseParser):
    _anchors = {
        'MAIN': LineStart() + Word('-') + Literal('NORMAL MODES and VIBRATIONAL FREQUENCIES (cm**(-1))') + Word('-') + LineEnd(),
        'MODE': LineStart() + Literal('mode') + OneOrMore(Word(nums)) + LineEnd(),
    }
    
    _parser = {
        'MODE': FortranLineParser('(A20,6I9)', skip=0),
        'FREQUENCY': FortranLineParser('(A20,6F9.2)', skip=0),
        'IR': FortranLineParser('(A20,6A9)', skip=0, map_values={'YES': True, '-': False}),
    }
    
    def __init__(self, raw, natoms):
        self.raw = StringIO(raw)
        self.natoms = natoms
        self.nmodes = natoms * 3
        self._data = None
        self._parse('_data')
        print(self._data)
    
    def _parse(self, datastore_key):
        NCOLS = 6
        self._scan_forward(VibrSpectrum._anchors['MAIN'])
        datastore = defaultdict(list)
        for chunk in self._chunks(range(self.nmodes), NCOLS):
            self._parse_block(chunk, datastore)
        self.__dict__[datastore_key] = pd.DataFrame(datastore)
    
    def _parse_block(self, mode_indices, datastore):
        self._scan_forward(VibrSpectrum._anchors['MODE'], before_match=True)
        line = self._next_content_line()
        datastore['MODE'] += self._parser['MODE'](line)
        line = self._next_content_line()
        datastore['FREQUENCY'] += self._parser['FREQUENCY'](line)
        line = self._next_content_line(skip=1)
        datastore['IR'] += self._parser['IR'](line)
        
# In[96]:
raw.seek(0)
df = VibrSpectrum(raw.getvalue(), 24)
# In[104]:
'_chunks' in dir(VibrSpectrum.__mro__[0])
# In[106]:
hasattr(VibrSpectrum.__mro__[0], '_chunks')
# In[107]:
import inspect
# In[115]:
_class = VibrSpectrum.__mro__[0]
_method = '_parse'
_method in _class.__dict__ and callable(getattr(_class, _method))