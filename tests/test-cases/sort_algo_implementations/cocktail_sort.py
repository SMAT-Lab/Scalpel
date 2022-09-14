# py-sorting <http://github.com/gwtw/py-sorting>
# Copyright 2015 Daniel Imms <http://www.growingwiththeweb.com>
# Released under the MIT license <http://github.com/gwtw/py-sorting/blob/master/LICENSE>

import math

from common.helpers import default_compare

def sort(array, compare=default_compare):
  start = -1
  end = len(array) - 2
  swapped = True
  while swapped:
    swapped = False
    for i in range(start + 1, end):
      if compare(array[i], array[i + 1]) > 0:
        array[i], array[i + 1] = array[i + 1], array[i]
        swapped = True
    if not swapped:
      break
    swapped = False
    for i in range(end, start, -1):
      if compare(array[i], array[i + 1]) > 0:
        array[i], array[i + 1] = array[i + 1], array[i]
        swapped = True
  return array
