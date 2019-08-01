#!/usr/bin/python
import subprocess
import json
import os
import pprint
import re
import sys

if len(sys.argv) != 3:
  print "Need to pass two args: path to Chromium checkout and path to list of commits (one commit per line)"
  sys.exit(1)

path_to_chromium_checkout = sys.argv[1]
commits_file = sys.argv[2]

authors = {}
reviewers = {}
unique_changed_files = set()
file_moves = 0

commits = open(commits_file)
num_cls_without_reviewer_info = 0
total_lines_inserted = 0
total_lines_deleted = 0

for commit in commits:
  commit = commit[:-1]

  # Find the author.
  author = subprocess.check_output(
      ["git", "show", "-s", "--format=\"%ae\"", commit],
      cwd=path_to_chromium_checkout)

  # Strip off the surrounding quotes and newline from the email address.
  author = author[1:-2]
  if author not in authors:
    authors[author] = 0
  authors[author] += 1

  # Find the reviewers and the information about the files changed.
  commit_msg = subprocess.check_output(["git", "show", "--numstat", commit],
                            cwd=path_to_chromium_checkout)
  cl_reviewed = False
  for line in commit_msg.splitlines():
    if "Reviewed-by" in line:
      cl_reviewed = True

      # Find this reviewer's email address.
      email_matcher = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", line)
      email = email_matcher.group(0)
      if email not in reviewers:
        reviewers[email] = 0
      reviewers[email] += 1

    if len(line) and line[0].isdigit():
      # This is a line describing a changed file in the format
      # <num_insertions>\t<num_deletions>\t<filepath>.
      # Extract this information.
      file_change_matcher = re.search(r"([0-9]*)\t([0-9]*)\t(.*)", line)
      lines_inserted = file_change_matcher.group(1)
      lines_deleted = file_change_matcher.group(2)
      changed_file = file_change_matcher.group(3)

      if "=>" in changed_file:
        # This is a file move.
        file_moves += 1

        # Compute the before and after paths.
        if "{" in changed_file:
          # The two paths share a common prefix and /or suffix. Git shows this
          # as "prefix/{before_path => after_path}/common_suffix".
          move_matcher = re.search(r"(.*){(.*) => (.*)}(.*)", changed_file)
          common_prefix = move_matcher.group(1)
          common_suffix = move_matcher.group(4)
          before_move_path = common_prefix + move_matcher.group(2) + common_suffix
          after_move_path = common_prefix + move_matcher.group(3) + common_suffix
        else:
          # There is no common prefix or suffix. Git shows this as
          # "before_path => after_path".
          move_matcher = re.search(r"(.*) => (.*)", changed_file)
          before_move_path = move_matcher.group(1)
          after_move_path = move_matcher.group(2)

        unique_changed_files.add(before_move_path)
        unique_changed_files.add(after_move_path)
      else:
        unique_changed_files.add(changed_file)

      total_lines_inserted += int(lines_inserted)
      total_lines_deleted += int(lines_deleted)

  # Rietveld didn't add reviewer information to the commit description; count
  # the number of such CLs.
  if not cl_reviewed:
    num_cls_without_reviewer_info += 1

commits.close()

metadata = {}
metadata["authors"] = authors
metadata["reviewers"] = reviewers
metadata["total_lines_inserted"] = total_lines_inserted
metadata["total_lines_deleted"] = total_lines_deleted
metadata["unique_changed_files"] = list(unique_changed_files)
metadata["file_moves"] = file_moves
metadata["num_cls_without_reviewer_info"] = num_cls_without_reviewer_info

json.dump(metadata, sys.stdout)
