# py-sorting <http://github.com/gwtw/py-sorting>
# Copyright 2016 Daniel Imms <http://www.growingwiththeweb.com>
# Released under the MIT license <http://github.com/gwtw/py-sorting/blob/master/LICENSE>

import math

def sort(array, maxValue=None):
  if maxValue is None:
    maxValue = 0
    for i in range(0, len(array)):
      if array[i] > maxValue:
        maxValue = array[i]

  buckets = [0] * (maxValue + 1)
  sortedIndex = 0

  for i in range(0, len(array)):
    buckets[array[i]] += 1

  for i in range(0, len(buckets)):
    while (buckets[i] > 0):
      array[sortedIndex] = i
      sortedIndex += 1
      buckets[i] -= 1

  return array
