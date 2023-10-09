This folder contains the code underlying the research described in Chapter 6.

To enable the content analysis of the letters using `whindexfreq.py` and `whindexsearch.py` (see below) first reassemble the index. This is done using the files in the folder /code/CHAPTER_5/indexdir_split, which are joined by running: 

`cat indexdir2_split/x* > indexdir2.tar.gz`

in the CHAPTER_5 directory. The resulting file, `indexdir2.tar.gz`, should then be copied into this (CHAPTER_6) directory and unpacked.

A further prerequisite for reproducing the results of this Chapter is:

`python trending_hr.py` 

This generates the FREQ_HR_OUT subfolder.

Further files in this folder are:

- `fromto_all_place_mapped_sorted` - Temporal edge list of correspondence with place of writing in plain text (see TNP_DATA for coded places)

- `people_docs_auto` - Output of the disambiguation and deduplication process.

- `added_people` - Added people labels created in the disambiguation and deduplication process.

- `renamed_people` - Modified people labels created in the disambiguation and deduplication process.

- `whindexfreq.py` - A tool that provides the *n* most significant words in a corpus of letters (passed as the first commandline argument, with *n* passed as the second) using the `key_terms` function of the `whoosh` [search engine library](https://pypi.org/project/Whoosh/).

- `whindexsearch.py` - A tool that searches the letters for any term passed as the commandline argument and returns a list of letter IDs. This too uses the `whoosh` library. **Note:** This requires Python 2.7.

- `multitrend.py` - Returns a figure showing rank over time of one or more words passed as commandline arguments, e.g. `python multitrend.py king queen`. Requires `gnuplot` to produce the visualisation.

- `extractchanges.py` - Measures the extent to which word ranks change over time.

- `extractwordnetwork.py` - Extracts the network of letters for a word and (optionally) a time window. Requires the commandline network layout tool `neato` to produce a network visualisation of this network.
 
The script `chapter_6_results.sh` produces the figures in Chapter 6. The script `chapter_6_peak_networks.sh' provides further code for the word networks created from extracted word frequency peaks. This script requires a longer runtime (in the region of hours).


