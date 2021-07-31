#!/usr/bin/env python
# coding: utf-8
# In[1]:
# 简单的余数
from struct import unpack_from
from hashlib import md5
N = 10000
def commom_hash(key, n):
    if isinstance(key, bytes):
        key = key.decode("utf-8")
    h = md5(str(key).encode("utf-8")).digest()
    i = unpack_from(">I", h)[0]
    return i % n
def cal_diff(hash_func, n, m):
    diffs = 0
    for i in range(N):
        if hash_func(i, n) == hash_func(i, m):
            continue
        diffs += 1
    return diffs / N
print(cal_diff(commom_hash, 100, 101))
# In[4]:
# 一致性哈希
from struct import unpack_from
from hashlib import md5
from collections import defaultdict
import bisect
class ConsistentHash:
    def __init__(self, nodes):
        self.nodes = nodes
        self.ring = []
        self.hash2node = {}
        self.init_ring()
    def init_ring(self):
        for n in range(self.nodes):
            h = self.cal_hash(n)
            self.ring.append(h)
            self.hash2node[h] = n
        self.ring.sort()
    def cal_hash(self, key):
        if isinstance(key, bytes):
            key = key.decode("utf-8")
        h = md5(str(key).encode("utf-8")).digest()
        i = unpack_from(">I", h)[0]
        return i
    def hash(self, key):
        h = self.cal_hash(key)
        i = bisect.bisect_left(self.ring, h) % self.nodes
        return self.hash2node[self.ring[i]]
ch = ConsistentHash(100)
ch101 = ConsistentHash(101)
n = 10000
diffs = 0
for i in range(n):
    if ch101.hash(i) != ch.hash(i):
        diffs += 1
print(diffs / n)
stat = defaultdict(int)
for i in range(10000):
    n = ch.hash(i)
    stat[n] += 1
max_ = 0
min_ = None
sum_ = 0
for n, count in stat.items():
    if count > max_:
        max_ = count
    if min_ is None or count < min_:
        min_ = count
    sum_ += count
print("max={} min={} avg={}".format(max_, min_, sum_ / len(stat)))