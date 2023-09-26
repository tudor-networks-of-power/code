echo
echo "Foreword/Chapter 1"
echo "========="
echo
echo "Number of letters in SP Tudor (after mappings and removal of duplicates)"
awk -F'\t' '{print $7}' fromto_all_place_mapped_sorted | sort | uniq | wc -l
echo "NOTE: Run peoplemap.py for detailed statistics on all removed letters."
echo "Number of letters in SP Tudor (non-empty sender & recipient fields in raw XML)"
awk -F'\t' '{print $7}' fromto_all_place | sort | uniq | wc -l
echo
echo "Network statistics:"
python network_stats.py
echo
python lettertime_stats.py
echo
echo "Letters examined in lettertimegaps_gaps_revised:"
grep '[*|+|%]' lettertimegaps_gaps_revised | awk -F'\t' '{print $2}' |  awk '{ sum+=$1} END {print sum}' 
echo  
echo "Duplicate letters removed:"
wc duplicate_ms_removals | awk '{print $1}'
echo
