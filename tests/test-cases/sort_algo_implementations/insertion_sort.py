# py-sorting <http://github.com/gwtw/py-sorting>
# Copyright 2015 Daniel Imms <http://www.growingwiththeweb.com>
# Released under the MIT license <http://github.com/gwtw/py-sorting/blob/master/LICENSE>

from common.helpers import default_compare

def sort(array, compare=default_compare):
  for i in range(1, len(array)):
    item = array[i]
    indexHole = i
    while indexHole > 0 and compare(array[indexHole - 1], item) > 0:
      array[indexHole] = array[indexHole - 1]
      indexHole -= 1
    array[indexHole] = item
  return array
