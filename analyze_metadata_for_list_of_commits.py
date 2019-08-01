#!/usr/bin/python
import subprocess
import json
import operator
import os
import pprint
import re
import sys

def top_n_from_dict_by_value(d, n):
  d_with_numbers = {}
  for key, value in d.iteritems():
    d_with_numbers[key] = int(value)
  sorted_d = sorted(d_with_numbers.items(), key=operator.itemgetter(1), reverse=True)
  elements_to_return = sorted_d[:n]
  return elements_to_return

if len(sys.argv) != 2:
  print "Need to pass one arg: path to file with metadata in JSON representation"
  sys.exit(1)

metadata_file = sys.argv[1]
with open(metadata_file, 'r') as f:
  metadata = json.load(f)

authors = metadata["authors"]
num_cls = sum([int(v) for v in authors.values()])
print "Number of CLs: ", num_cls

print "Unique authors:", len(authors.keys())

top_10_authors = top_n_from_dict_by_value(authors, 10)
print "Top 10 authors:"
for author, num_cls in top_10_authors:
  print str(author) + ": " + str(num_cls) + " CLs"

reviewers = metadata["reviewers"]

unique_changed_files = metadata["unique_changed_files"]


