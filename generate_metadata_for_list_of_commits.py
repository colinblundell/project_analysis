#!/usr/bin/python
import subprocess
import json
import os
import pprint
import sys

authors = {}
reviewers = {}
files_changed = []

# TODO: Pass via arg
commits = open("test_commits.txt")
authors_file = open("/usr/local/google/home/blundell/identity_component_commit_authors.txt", "w")
reviewers_file = open("/usr/local/google/home/blundell/identity_component_commit_reviewers.txt", "w")
files_changed_file = open("/usr/local/google/home/blundell/identity_component_commit_files_changed.txt", "w")
num_cls_with_reviews = 0
for commit in commits:
  commit = commit[:-1]
  author = subprocess.check_output(["git", "show", "-s", "--format=\"%ae\"", commit],
                            cwd="/usr/local/google/home/blundell/clankium/src")
  author = author[:-1]

  if author not in authors:
    authors[author] = 0
  authors[author] += 1

  commit_msg = subprocess.check_output(["git", "show", "--numstat"],
                            cwd="/usr/local/google/home/blundell/clankium/src")
  cl_reviewed = False
  for line in commit_msg.splitlines():
    # TODO: Count the # of CLs with no "Reviewed-by". I think
    # that rietveld didn't add this information.
    # TODO: Generate total unique files changed.
    if "Reviewed-by" in line:
      cl_reviewed = True
      if line not in reviewers:
        reviewers[line] = 0
      reviewers[line] += 1
    if len(line) and line[0].isdigit():
      files_changed.append(line)
  if cl_reviewed:
    num_cls_with_reviews += 1

commits.close()

metadata = {}
metadata["authors"] = authors
metadata["reviewers"] = reviewers
metadata["files_changed"] = files_changed
json.dump(metadata, sys.stdout)
#print "Num CLs with reviews: " + str(num_cls_with_reviews)
#pprint.pprint(authors, stream=authors_file)
#pprint.pprint(reviewers, stream=reviewers_file)
#pprint.pprint(files_changed, stream=files_changed_file)
