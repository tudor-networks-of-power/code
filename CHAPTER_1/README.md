This folder contains the code underlying the research described in Chapter 1.

The subfolder `Disambiguation_Engine` contains the code for this tool, which creates a local web environment at [http://localhost:8081/](http://localhost:8081/). This relies on the XML and images of the State Papers Online for full functionality. The appropriate paths need to be inserted into the code at the indicated places. The file containing the mappings produced by the Disambiguation Engine is `people_docs`.

Note that `renamed_people` and `added_people` contain further amendments to the people identities in `people_docs`.

The rest of the pipeline for data processing is:

- `python autodisam.py` - This applies the disambiguation rules in `auto_mapping`, outputting `people_docs_auto`.

- `python peoplemap.py` - This applies the mappings of people identities in people_docs_auto to `fromto_all_place`, producing `fromto_all_place_mapped`.

- `sortfromto.sh` - This shell script sorts the letters by date (using the start of the date window in the case of uncertainty), producing `fromto_all_place_mapped_sorted`.

- `chapter_1_results.sh` - This script produces numerical results given in Chapter 1.

- `checkforchains.py` A tool for identifying errors produced in the manual disambiguation and deduplication process, where identities are mapped A -> B -> C or A -> B -> A. The output is checked manually and corrections are detailed in `checkforchains_straight_revised_190328_combined_edited` and `checkforchains_ambiguities_resolved`, which serve as input files for `peoplemap.py`.

- `lettertimegaps.py` - A tool for identifying errors in the XML metadata and the disambiguation and deduplication process which highlights large gaps in time between successive items of correspondence and large date uncertainty windows. The results are checked manually and changes are implemented through `specific_replace`, which serves as an input into `peoplemap.py`.

