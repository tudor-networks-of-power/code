echo
echo "Chapter 7"
echo "========="
echo
echo "Letters written by Burghley from named origins (unique MS):"
awk -F'\t' '{print "@"$1"\t"$6"\t"$7}' fromto_all_place_mapped_sorted | grep '@30478\t' | grep -v '\t-\t' | awk -F'\t' '{print $3}' | sort | uniq | wc | awk '{print $1}'
echo "Letters written by Charles V from named origins (unique MS):"
awk -F'\t' '{print "@"$1"\t"$6"\t"$7}' fromto_all_place_mapped_sorted | grep '@12113\t' | grep -v '\t-\t' | awk -F'\t' '{print $3}' | sort | uniq | wc | awk '{print $1}'
echo "Rank of Erasmus in distances:" # we subtract one from the actual rank below, due to Privy Council at top of ranking, which we ignore
awk -F@ '{print "@"$1}' distances_final | grep -n '@6113\t'  | awk -F: '{print $1-1}'
echo "Letters written by Erasmus from named origins (unique MS):"
awk -F'\t' '{print "@"$1"\t"$6"\t"$7}' fromto_all_place_mapped_sorted | grep '@6113\t' | grep -v '\t-\t' | awk -F'\t' '{print $3}' | sort | uniq | wc | awk '{print $1}'
echo "Letters written by Erasmus in total (unique MS):"
awk -F'\t' '{print "@"$1"\t"$6"\t"$7}' fromto_all_place_mapped_sorted | grep '@6113\t' | awk -F'\t' '{print $3}' | sort | uniq | wc | awk '{print $1}'
echo "Note, by contrast: Out-strength of Erasmus (i.e. treating letters with multiple senders/recipients as separate):"
awk -F'\t' '{print "@"$1"\t"$6"\t"$7}' fromto_all_place_mapped_sorted | grep '@6113\t' | wc | awk '{print $1}'
echo
echo "Number of itineraries (people who wrote from more than one location):"
awk '{if ($3 > 1) print $3}' mobilities_final_final | wc -l 
echo "Maximum distance (miles):"
sort -gk2 mobilities_final_final | tail -n 1 | awk '{print $2}'
echo "Maximum number of journey legs:"
sort -gk4 mobilities_final_final | tail -n 1 | awk '{print $4}'
echo "Maximum number of unique places:"
sort -gk3 mobilities_final_final | tail -n 1 | awk '{print $3}'
echo "Number of itineraries with 10 or more separate locations:"
awk '{if ($3 > 9) print $3}' mobilities_final_final | wc -l
echo "Number of itineraries longer than 1,000 miles:"
awk '{if ($2 > 1000) print $2}' mobilities_final_final | wc -l
echo
echo "Number of letters with locations (i.e. legs) for Burghley:"
grep Burghley mobilities_final_final | awk '{print $4}'
echo "Number of letters with locations (i.e. legs) for the Emperor Charles V:"
grep 'Emperor Charles V' mobilities_final_final | awk '{print $4}'
echo
echo "Erasmus's rank, number of letters with locations, and total distance:"
sort -grk2 mobilities_final_final | grep -n Eras | awk -F: '{print $1}'
sort -grk2 mobilities_final_final | grep -n Eras | awk '{print $4}'
sort -grk2 mobilities_final_final | grep -n Eras | awk '{print $2}'

echo "Top ten for total miles travelled"
sort mobilities_final_final -k2nr | head -n 10 | awk -F'\t' '{print $2"\t"$10"\t"$11}'
echo
echo "Top 30 for miles per letter"
sort mobilities_final_final -k5nr | head -n 30 | awk -F'\t' '{print $2"\t"$4"\t"$5"\t"$10"\t"$11}'
echo
echo "Number of overlaps"
wc placeoverlap.out_final_final | awk '{print $1"/2 due to double counting"}'
echo
echo "Number of significant overlaps (Bonferroni & p-value threshold of 0.05)"
awk '{print $12}'  placeoverlap.out_final_final  | sort --sort=general-numeric | grep -B 1 -n '0\.05' | head -n 1 | awk -F'-' '{print $1"/2 due to double counting"}'  
echo
echo "Plotting distribution of number of letters for all places of writing... Note: This requires Python 2.7 and gnuplot."
python placehist.py
gnuplot placehist.plotscript
open placehist.ps
echo
echo "Top twenty places by number of letters"
head -n 20 placehist_rank.out | awk '{print $2}' > tmp
head -n 20 placehist_rank.out | awk '{print "@"$1"@"}' | xargs -I{} pname {} | awk '{print $2" ["$1"]"}' > tmp2
paste tmp2 tmp 
echo
echo "Number of letters with origin of writing"
awk -F'\t' '{print "@"$6"@"}' ../fromto_all_place | grep -v '-' | wc | awk '{print $1}'
echo
echo "Total number of letters"
wc ../fromto_all_place | awk '{print $1}'
echo
echo "Note: Total number of letters after mapping, which separates out multiple senders and recipients"
wc fromto_all_place_mapped_sorted_wplm_itineraries_final_final | awk '{print $1}'
echo 
python greater_london.py
echo
echo "Number of people with overlaps"
wc overlapstats_final_final.out | awk '{print $1}'
echo 
echo "Top twenty people by number of people they overlap with"
#sort -k3 -nr overlapstats_final_final.out | head -n 20 | awk '{print $2" ["$1"]\t"$3}' | sed s/'_'/' '/g
sort -k3 -nr overlapstats_final_final.out | head -n 20 | awk '{print $2"\t("$3")"}' | sed s/'_'/' '/g
echo
echo "Number of overlaps without communication and with mentions"
sed s/'> - '/'@'/g  OVERLAP7/mindex.html | tr @ '\n' | grep -v '<html>' | awk '{print $1}' | paste -sd+ - | bc | awk '{print $1"/2"}' | bc
echo
echo "Seth Cocks [27756] originally mentioned in these two MS (among others):"
grep Cocks fromto_all_place | grep 159307
echo
echo "These two MS are in fact duplicates (same MS ID, sender and recipient) and are collapsed to the one with the smaller date range:"
grep 27756 fromto_all_place_mapped | grep 159307
echo 
echo "Using the duplicate MS we know that Cocks was probably in Prague on 15930726. This places him within eight days of Christopher Parkins [4381] in Prague:"
grep 4381 fromto_all_place_mapped | grep Prague
echo
echo "This is interesting because Cocks and Parkins also had a significant overlap in Cracow on April 8th, 1595:"
grep 27756 placeoverlap.out_final_final | grep 4381
echo
echo "Note that Seth Cocks [27756] was also in Padua, but that this information has also been removed by collapsing these duplicate MS:"
grep Cocks fromto_all_place | grep 15931209
echo
echo "...into one (because of same MS ID, sender and recipient) with the smaller date range:"
grep 27756 fromto_all_place_mapped | grep 15931209
echo
