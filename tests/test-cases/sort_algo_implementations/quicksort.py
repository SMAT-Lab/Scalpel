# py-sorting <http://github.com/gwtw/py-sorting>
# Copyright 2015 Daniel Imms <http://www.growingwiththeweb.com>
# Released under the MIT license <http://github.com/gwtw/py-sorting/blob/master/LICENSE>

import math
import random

from common.helpers import default_compare

def sort(array, compare=default_compare):
  return inner_sort(array, 0, len(array) - 1, compare)

def inner_sort(array, left, right, compare=default_compare):
  if left < right:
    pivot = partition_random(array, left, right, compare)
    inner_sort(array, left, pivot - 1, compare)
    inner_sort(array, pivot + 1, right, compare)
  return array

def partition_random(array, left, right, compare):
  pivot = left + math.floor(random.random() * (right - left))
  if pivot != right:
    array[right], array[pivot] = array[pivot], array[right]
  return partition_right(array, left, right, compare)

def partition_right(array, left, right, compare):
  pivot = array[right]
  mid = left
  for i in range(mid, right):
    if compare(array[i], pivot) <= 0:
      if i != mid:
        array[i], array[mid] = array[mid], array[i]
      mid += 1
  if right != mid:
    array[right], array[mid] = array[mid], array[right]
  return mid
