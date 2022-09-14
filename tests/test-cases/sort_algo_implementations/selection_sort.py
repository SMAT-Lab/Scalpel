# py-sorting <http://github.com/gwtw/py-sorting>
# Copyright 2015 Daniel Imms <http://www.growingwiththeweb.com>
# Released under the MIT license <http://github.com/gwtw/py-sorting/blob/master/LICENSE>

from common.helpers import default_compare

def sort(array, compare=default_compare):
  for i in range(0, len(array)):
    min_index = i
    for j in range(i + 1, len(array)):
      if compare(array[j], array[min_index]) < 0:
        min_index = j
    if min_index != i:
      array[i], array[min_index] = array[min_index], array[i]
  return array
