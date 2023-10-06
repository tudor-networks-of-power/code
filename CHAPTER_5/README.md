This folder contains the code underlying the research described in Chapter 5.

The pipeline for generating and cleaning the list of women in the data is as follows:

`./women_names.grep > women_people_docs`

This script uses a list of female Tudor names and titles collected on this now-defunct [https://web.archive.org/web/20161004064433/http://www.kateemersonhistoricals.com/TudorWomenIndex.htm](online collection of Tudor women's biographies produced by Kate Emerson).

`python make_women_check.py`

This generates a file called `women_list_to_be_checked` and a basic HTML page, `make_women_check.html`,for viewing contextual mapped person IDs and linked data.

We ran this cleaning step in 2016, producing the files `not_women_list`, which lists IDs to be removed, as well as `additional_women` and a supplementary removal list, `additional_men`.
For reproducibility of the results in Chapter 5 we enclose the version of `women_people_docs` produced in 2016 (`women_people_docs_2016`) and use it in `make_women_check.py`. 

Re-running the pipeline with the up-to-date `people_docs` only changes results very slightly, removing two letters from individual 27863.

The files in this folder:

- `indivnetworkstats.py` - calculates network statistics of an individual for a given time window or the entire period.

- `fromto_all_place_mapped_sorted` - Temporal edge list of correspondence with place of writing in plain text (see TNP_DATA for coded places)

- `people_docs_auto` - Output of the disambiguation and deduplication process.

- `added_people` - Added people labels created in the disambiguation and deduplication process.

- `renamed_people` - Modified people labels created in the disambiguation and deduplication process.

- `bigrank.out` - The overall file of network metrics for everyone in the dataset, produced by the Network Analysis Tool.

The script `chapter_5_results.sh` produces numerical results given in Chapter 5.


