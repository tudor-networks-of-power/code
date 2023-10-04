This folder contains the code underlying the research described in Chapter 2.

The subfolder `Network_Analysis_Tool` contains the code for this tool, which is run by typing

`python tudornetworks_bottle.py`. Note: This requires Python 2.7, which can e.g. be achieved by creating a dedicated conda environment.

This creates a local web environment at [http://localhost:8082/](http://localhost:8082/). The tool relies on the XML metadata and manuscript images of the Tudor State Papers Online database for full functionality. The appropriate paths need to be inserted into the code at the indicated places. The network metrics are output into the file `bigrank.out` (see below).

Other files in this folder:

- `indivnetworkstats.py` - calculates network statistics of an individual for a given time window or the entire period.

- `fromto_all_place_mapped_sorted` - Temporal edge list of correspondence with place of writing in plain text (see TNP_DATA for coded places)

- `people_docs_auto` - Output of the disambiguation and deduplication process.

- `added_people` - Added people labels created in the disambiguation and deduplication process.

- `renamed_people` - Modified people labels created in the disambiguation and deduplication process.

- `bigrank.out` - The overall file of network metrics for everyone in the dataset, produced by the Network Analysis Tool.

The script `chapter_2_results.sh` produces numerical results given in Chapter 2.


