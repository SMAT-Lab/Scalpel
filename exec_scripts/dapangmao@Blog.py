#!/usr/bin/env python
# coding: utf-8
# In[14]:
from functools import lru_cache
small_test_nums = (1, 1, 1, 1, 1)
small_test_S = 3
big_test_nums = tuple(range(100))
big_test_S = sum(range(88))
# In[15]:
def findTargetSumWays_1(nums, S):
    """
    :type nums: Tuple[int]
    :type S: int
    :rtype: int
    """
    if not nums:
        if S == 0:
            return 1
        else:
            return 0
    return findTargetSumWays_1(nums[1:], S+nums[0]) + findTargetSumWays_1(nums[1:], S-nums[0]) 
get_ipython().run_line_magic('time', 'findTargetSumWays_1(small_test_nums, small_test_S)')
# In[16]:
def findTargetSumWays_2(nums, S):
    if not nums:
        return 0
    dic = {nums[0]: 1, -nums[0]: 1} if nums[0] != 0 else {0: 2}
    for i in range(1, len(nums)):
        tdic = {}
        for d in dic:
            tdic[d + nums[i]] = tdic.get(d + nums[i], 0) + dic.get(d, 0)
            tdic[d - nums[i]] = tdic.get(d - nums[i], 0) + dic.get(d, 0)
        dic = tdic
    return dic.get(S, 0)
get_ipython().run_line_magic('time', 'findTargetSumWays_2(big_test_nums, big_test_S)')
# In[17]:
@lru_cache(10000000)
def findTargetSumWays_3(nums, S):
    if not nums:
        if S == 0:
            return 1
        else:
            return 0
    return findTargetSumWays_3(nums[1:], S+nums[0]) + findTargetSumWays_3(nums[1:], S-nums[0]) 
get_ipython().run_line_magic('time', 'findTargetSumWays_3(big_test_nums, big_test_S)')