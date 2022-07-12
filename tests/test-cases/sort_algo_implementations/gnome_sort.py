# py-sorting <http://github.com/gwtw/py-sorting>
# Copyright 2015 Daniel Imms <http://www.growingwiththeweb.com>
# Released under the MIT license <http://github.com/gwtw/py-sorting/blob/master/LICENSE>

from common.helpers import default_compare

def sort(array, compare=default_compare):
  pos = 1
  while pos < len(array):
    if compare(array[pos], array[pos - 1]) >= 0:
      pos += 1
    else:
      array[pos], array[pos - 1] = array[pos - 1], array[pos]
      if pos > 1:
        pos -= 1
  return array
