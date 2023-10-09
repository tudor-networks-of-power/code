This folder contains the code underlying the research described in Chapter 5.

The pipeline for generating and cleaning the list of women in the data is as follows:

`./women_names.grep > women_people_docs`

This script uses `people_docs` in combination with a list of female Tudor names and titles derived from [this](https://web.archive.org/web/20161004064433/http://www.kateemersonhistoricals.com/TudorWomenIndex.htm) now-defunct online collection of Tudor women's biographies produced by Kate Emerson (preserved on the Internet Archive). The next step is:

`python make_women_check.py`

This generates a file called `women_list_to_be_checked` and a basic HTML page, `make_women_check.html`,for viewing contextual mapped person IDs and linked data.

We ran this cleaning step in 2016, producing the files `not_women_list`, which lists IDs to be removed, as well as `additional_women` and a supplementary removal list, `additional_men`.
For reproducibility of the results in Chapter 5 we enclose the version of `women_people_docs` produced in 2016 (`women_people_docs_2016`) and use it in `make_women_check.py`. (Re-running the pipeline with the up-to-date `people_docs` only changes results very slightly, removing two letters from individual 27863 from `fromto_all_place_mapped_sorted_wtm`.)

The next and final step for creating the list of women is:

`python final_women.py` - This combines `women_list_to_be_checked`, `not_women_list`, `additional_women`, and `additional_men` to produce `final_women.out`, which is the list of women used in further data analysis. This code also outputs `fromto_all_place_mapped_sorted_wtm` and fromto_all_place_mapped_sorted_mtw`, which are edgelists with female-to-male and male-to-female correspondence, as well as `fromto_all_place_mapped_sorted_women`, which provides the edge list of correspondence between women, and `fromto_all_place_mapped_sorted_at_least_one_woman`, which lists all edges with at least one female correspondent (and is the union of the preceding three files).

To enable the content analysis of the letters using `whindexfreq.py` (see below) first reassemble the index by running: 

`cat indexdir2_split/x* > indexdir2.tar.gz`

and then unpacking `indexdir2.tar.gz`.

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

- `comparewhfreqlists.py` - identifies the words that differ most in rank between two rankings, where the difference metric is the logarithms of the ranks. 

- `women_triangles.py` - Analysis of women's involvement in different triadic network structures. This takes some time to run. **Note:** This code requires Python 2.7.

- `women_hierarchies.py` - Analysis of women's positions in feedforward loops.

The script `chapter_5_results.sh` produces numerical results given in Chapter 5. As part of this it also runs `make_women_check.py` and `final_women.py`. It does not reassemble the index for `whindexfreq.py` (see above), which is a prerequisite for running this script.


