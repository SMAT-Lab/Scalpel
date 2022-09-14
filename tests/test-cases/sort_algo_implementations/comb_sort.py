# py-sorting <http://github.com/gwtw/py-sorting>
# Copyright 2015 Daniel Imms <http://www.growingwiththeweb.com>
# Released under the MIT license <http://github.com/gwtw/py-sorting/blob/master/LICENSE>

import math

from common.helpers import default_compare

def sort(array, compare=default_compare):
  gap = len(array)
  shrinkFactor = 1.3
  swapped = False

  while gap > 1 or swapped:
    if gap > 1:
      gap = math.floor(gap / shrinkFactor)
    swapped = False
    for i in range(len(array) - gap):
      if compare(array[i], array[i + gap]) > 0:
        array[i], array[i + gap] = array[i + gap], array[i]
        swapped = True

  return array
