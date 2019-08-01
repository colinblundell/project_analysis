- identity_service_component_buglist.txt: A list of all of the bugs (with any
  status) with the Internals>Services>Identity component. Manually copied from
  the following view of these bugs with spaces transformed to newlines via your
  favorite editor:
  https://bugs.chromium.org/p/chromium/issues/list?can=1&q=component%3AInternals>Services>Identity+&colspec=ID+Pri+M+Stars+ReleaseBlock+Component+Status+Owner+Summary+OS+Modified&sort=&groupby=&mode=grid&y=--&x=--&cells=ids&nobtn=Update

- identity_service_component_commits.txt: A list of all the commits that
  reference one or more of the bugs in the buglist. Generated as follows in the
  parent directory of this one:
  ./generate_identity_component_bug_commits.sh path/to/chromium data/identity_service_component_buglist.txt > data/identity_service_component_commits.txt

The buglist was last generated on August 1, 2019.

The set of commits was last generated as of Chromium rev 6c90100 (August 1,
2019).
