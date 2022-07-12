# py-sorting <http://github.com/gwtw/py-sorting>
# Copyright 2015 Daniel Imms <http://www.growingwiththeweb.com>
# Released under the MIT license <http://github.com/gwtw/py-sorting/blob/master/LICENSE>

from common.helpers import default_compare

def sort(array, compare=default_compare):
  for i in range(0, len(array) - 1):
    for j in range(1, len(array) - i):
      if compare(array[j - 1], array[j]) > 0:
        array[j], array[j - 1] = array[j - 1], array[j]
  return array
