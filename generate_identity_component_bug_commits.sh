#!/bin/bash

# Generates a list of commits that reference bugs in an input buglist. The bugs
# should be listed one per line in the buglist.

if [ "$1" == "" ]; then
  echo "Need to supply path to chromium checkout"
  exit 1
fi

if [ "$2" == "" ]; then
  echo "Need to supply buglist"
  exit 1
fi

path_to_chromium=$1
buglist=$2

project_analysis_dir=`pwd`

# Create input to "git log --grep" that checks for the existence of any of the 
# bugs in the buglist. Concretely, it constructs a string of the following form:
# (<bug1> | <bug2> | <bug3> | ... | <bug_n>) .

bug_matcher=""
for b in `cat $buglist`
do
  if [ -z $bug_matcher ]
  then
    bug_matcher="\("$b
  else
    bug_matcher=$bug_matcher"\|"$b
  fi
done
bug_matcher=$bug_matcher"\)"

cd $path_to_chromium

# Do "git log --grep" searching for references to these bugs and extract the 
# hashes of the commits via finding the "commit: <sha1>" line and extracting the
# "<sha1>" field.
git log --grep "[Bb][Uu][Gg].*\<$bug_matcher\>" | grep "^commit" | cut -f 2 -d" "
