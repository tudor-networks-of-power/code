This folder contains the code underlying the research described in Chapter 7.

The pipeline for generating and analysing the datasets relating to places of writing is as follows:

1. `python placesmap.py`

This produces an temporal edge list of correspondence with cleaned up places of writing, denoted by unique IDs, in `fromto_all_place_mapped_sorted_wplm`

2. `python mapitineraries.py` 

This constructs approximate itineraries of all individuals in the data, based on their successive places of writing over time. Note: This can take approximately an hour to run.

3. `python mobility.py`

This produces mobility metrics, such as the number of places visited, average and total distance travelled, etc.

4. `python placeoverlap_final_final.py`

This produces a list of overlaps between individual itineraries including a very conservative statistical significance estimate (in form of a Bonferroni-corrected p-value).

5. `gunzip mentions.gz`

This needs to be unpacked for the next step.

6. `python overlaphtml7.py`

This produces a rudimentary HTML interface for exploration of the overlapping itineraries. Contextual information includes whether the overlapping individuals corresponded before or after the overlap, and whether they may have mentioned each other in their correspondence to others.

Further files in this folder are:

- `fromto_all_place_mapped_sorted` - Temporal edge list of correspondence with place of writing in plain text (see TNP_DATA for coded places)

- `people_docs_auto` - Output of the disambiguation and deduplication process.

- `added_people` - Added people labels created in the disambiguation and deduplication process.

- `renamed_people` - Modified people labels created in the disambiguation and deduplication process.

- `placeshist.py` - examines the distribution of letters per place

- `greater_london.py` - constructs an estimate of the number of letters sent from locations within a ten-mile radius of the City of London.

- `velocity.py` - This calculates 'velocities', dividing distances between successive places of writing by the time elapsed. This highlights impossible itineraries, which in turn highlight likely errors in the person- or place-related metadata, or possible attempts at deception by the letter author.
 
The script `chapter_7_results.sh` produces numerical results and figures in Chapter 7. 


