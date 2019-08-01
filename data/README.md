- identity_service_component_buglist.txt: A list of all of the bugs (with any
  status) with the Internals>Services>Identity component. Manually copied from
  the following view of these bugs with spaces transformed to newlines via your
  favorite editor:
  https://bugs.chromium.org/p/chromium/issues/list?can=1&q=component%3AInternals>Services>Identity+&colspec=ID+Pri+M+Stars+ReleaseBlock+Component+Status+Owner+Summary+OS+Modified&sort=&groupby=&mode=grid&y=--&x=--&cells=ids&nobtn=Update

- identity_service_component_commits.txt: A list of all the commits that
  reference one or more of the bugs in the buglist. Generated as follows in the
  parent directory of this one:
  ./generate_commits_for_buglist.sh path/to/chromium data/identity_service_component_buglist.txt > data/identity_service_component_commits.txt

- identity_service_components_commit_metadata.txt: Metadata about the set of
  commits in JSON format. Generated as follows in the parent directory of this
  one:
  /generate_metadata_for_list_of_commits.py path/to/chromium data/identity_service_component_commits.txt > data/identity_service_component_commits_metadata.txt

- To analyze the commit metadata, run the following in the parent directory of
  this one:
  ./analyze_metadata_for_list_of_commits.py data/identity_service_component_commits_metadata.txt
  
The buglist was last generated on August 1, 2019.

The set of commits and metadata for those commits were last generated as of
Chromium rev 6c90100 (August 1, 2019).
