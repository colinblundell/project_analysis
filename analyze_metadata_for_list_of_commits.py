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

def print_metadata_about_involved_parties(input_data, element_name, involved_parties_name, involved_parties_action):
  print
  total_num_values = sum([int(v) for v in input_data.values()])
  print "Number of " + element_name + ": ", total_num_values

  print "Unique " + involved_parties_name + ": ", len(input_data.keys())

  top_10 = top_n_from_dict_by_value(input_data, 10)
  print
  print "Top 10 " + involved_parties_name + ":"
  for involved_party, num in top_10:
    print str(involved_party) + ": " + str(num) + " CLs " + involved_parties_action

if len(sys.argv) != 2:
  print "Need to pass one arg: path to file with metadata in JSON representation"
  sys.exit(1)

metadata_file = sys.argv[1]
with open(metadata_file, 'r') as f:
  metadata = json.load(f)

print_metadata_about_involved_parties(metadata["authors"], "CLs", "authors", "authored")
print_metadata_about_involved_parties(metadata["reviewers"], "reviews", "reviewers", "reviewed")

reviewers = metadata["reviewers"]

unique_changed_files = metadata["unique_changed_files"]
print
print "# of unique files changed:", len(unique_changed_files)
print "# of LOC inserted: ", metadata["total_lines_inserted"]
print "# of LOC deleted: ", metadata["total_lines_deleted"]
