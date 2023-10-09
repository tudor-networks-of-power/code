This folder contains the code underlying the research described in Chapter 6.

To enable the content analysis of the letters using `whindexfreq.py` and `whindexsearch.py` (see below) first reassemble the index. This is done using the files in the folder /code/CHAPTER_5/indexdir_split, which are joined by running: 

`cat indexdir2_split/x* > indexdir2.tar.gz`

in the CHAPTER_5 directory. The resulting file, `indexdir2.tar.gz`, should then be copied into this (CHAPTER_6) directory and unpacked.

A further prerequisite for reproducing the results of this Chapter is:

`python trending_hr.py` 

This generates 

Further files in this folder are:

- `fromto_all_place_mapped_sorted` - Temporal edge list of correspondence with place of writing in plain text (see TNP_DATA for coded places)

- `people_docs_auto` - Output of the disambiguation and deduplication process.

- `added_people` - Added people labels created in the disambiguation and deduplication process.

- `renamed_people` - Modified people labels created in the disambiguation and deduplication process.

- `bigrank.out` - The overall file of network metrics for everyone in the dataset, produced by the Network Analysis Tool.

- `network_stats.py` - This calculates basic global network statistics. (Used in `chapter_5_results.sh`.)

- `exceptelizandbothmarys.sh` - This script removed Elizabeth I, Mary I, and Mary Queen of Scots from edge lists and produces new edgelists that end in `_wo_eliz_and_bothmarys`.

- `linked_data_consolidated_amend_all_final_edited` - Linked data providing biographical background on Wikipedia, Oxford Dictionary of National Biography, VIAF, or History of Parliament.

- `whindexfreq.py` - A tool that provides the *n* most significant words in a corpus of letters (passed as the first commandline argument, with *n* passed as the second) using the `key_terms` function of the `whoosh` [search engine library](https://pypi.org/project/Whoosh/).

- `comparewhfreqlists.py` - This code identifies the words that differ most in rank between two rankings, where the difference metric is the logarithms of the ranks. 

- `women_triangles.py` - Analysis of women's involvement in different triadic network structures. This takes some time to run. **Note:** This code requires Python 2.7.

- `women_hierarchies.py` - Analysis of women's positions in feedforward loops.

The script `chapter_5_results.sh` produces numerical results given in Chapter 5. As part of this it also runs `make_women_check.py` and `final_women.py`. It does not reassemble the index for `whindexfreq.py` (see above), which is a prerequisite for running this script.


