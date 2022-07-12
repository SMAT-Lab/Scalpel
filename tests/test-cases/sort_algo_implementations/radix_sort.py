# py-sorting <http://github.com/gwtw/py-sorting>
# Copyright 2016 Daniel Imms <http://www.growingwiththeweb.com>
# Released under the MIT license <http://github.com/gwtw/py-sorting/blob/master/LICENSE>

import math

def sort(array, radix=10):
  if len(array) == 0:
    return array

  # Determine minimum and maximum values
  minValue = array[0];
  maxValue = array[0];
  for i in range(1, len(array)):
    if array[i] < minValue:
      minValue = array[i]
    elif array[i] > maxValue:
      maxValue = array[i]

  # Perform counting sort on each exponent/digit, starting at the least
  # significant digit
  exponent = 1
  while (maxValue - minValue) / exponent >= 1:
    array = countingSortByDigit(array, radix, exponent, minValue)
    exponent *= radix

  return array

def countingSortByDigit(array, radix, exponent, minValue):
  bucketIndex = -1
  buckets = [0] * radix
  output = [None] * len(array)

  # Count frequencies
  for i in range(0, len(array)):
    bucketIndex = math.floor(((array[i] - minValue) / exponent) % radix)
    buckets[bucketIndex] += 1

  # Compute cumulates
  for i in range(1, radix):
    buckets[i] += buckets[i - 1]

  # Move records
  for i in range(len(array) - 1, -1, -1):
    bucketIndex = math.floor(((array[i] - minValue) / exponent) % radix)
    buckets[bucketIndex] -= 1
    output[buckets[bucketIndex]] = array[i]

  return output
