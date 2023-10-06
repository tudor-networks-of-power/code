echo
echo "Chapter 5"
echo "========="
echo
echo "Number of nodes in network:"
python network_stats.py | grep 'Number of nodes'
echo
echo "Queen Elizabeth I's (24658) ranking by degree:"
grep all bigrank.out | sort -k 3 -nr | grep -n 24658 | head -n 1
echo
echo "Queen Mary I's (24679) ranking by degree:"
grep all bigrank.out | sort -k 3 -nr | grep -n 24679 | head -n 1
echo 
python make_women_check.py
python final_women.py
echo "Number of women in the data:"
wc -l final_women.out
echo
echo "Letters from or to women:"
wc -l fromto_all_place_mapped_sorted_at_least_one_woman 
echo
echo "Letters from or to women, excluding Elizabeth I and Mary I:"
awk '{print "@"$1"@ @"$2"@"}' fromto_all_place_mapped_sorted_at_least_one_woman | grep -v @24658@ | grep -v @24679@ | wc -l
echo
echo "Letters from men to women:"
wc -l fromto_all_place_mapped_sorted_mtw
echo
echo "Letters from women to men:"
wc -l fromto_all_place_mapped_sorted_wtm
echo
./exceptelizandbothmarys fromto_all_place_mapped_sorted_wtm
./exceptelizandbothmarys fromto_all_place_mapped_sorted_mtw
echo
echo "Letters from men to women excluding Elizabeth I, Mary I, and Mary Queen of Scots:"
wc -l fromto_all_place_mapped_sorted_mtw_wo_eliz_and_bothmarys
echo
echo "Letters from women to men excluding Elizabeth I, Mary I, and Mary Queen of Scots:"
wc -l fromto_all_place_mapped_sorted_wtm_wo_eliz_and_bothmarys
echo
awk -F'\t' '{print $7}' fromto_all_place_mapped_sorted_mtw_wo_eliz_and_bothmarys > fromto_all_place_mapped_sorted_mtw_wo_eliz_and_bothmarys.bare
awk -F'\t' '{print $7}' fromto_all_place_mapped_sorted_wtm_wo_eliz_and_bothmarys > fromto_all_place_mapped_sorted_wtm_wo_eliz_and_bothmarys.bare
python whindexfreq.py fromto_all_place_mapped_sorted_mtw_wo_eliz_and_bothmarys.bare 1000
python whindexfreq.py fromto_all_place_mapped_sorted_wtm_wo_eliz_and_bothmarys.bare 1000
python comparewhfreqlists.py fromto_all_place_mapped_sorted_mtw_wo_eliz_and_bothmarys.bare.whfreq fromto_all_place_mapped_sorted_wtm_wo_eliz_and_bothmarys.bare.whfreq
echo
echo "Words of note and their rankings in men-to-women and women-to-men correspondence:"
grep husband comparewhfreqlists.out
grep son comparewhfreqlists.out
grep children comparewhfreqlists.out
grep brother comparewhfreqlists.out
grep father comparewhfreqlists.out
grep family comparewhfreqlists.out
grep favour comparewhfreqlists.out
grep favor comparewhfreqlists.out
grep beg comparewhfreqlists.out
grep begs comparewhfreqlists.out
grep trouble comparewhfreqlists.out
grep suit comparewhfreqlists.out
grep help comparewhfreqlists.out
grep desires comparewhfreqlists.out
grep justice comparewhfreqlists.out
grep grant comparewhfreqlists.out
grep pray comparewhfreqlists.out
grep land comparewhfreqlists.out
grep house comparewhfreqlists.out
grep send comparewhfreqlists.out
grep remembrance comparewhfreqlists.out
grep money comparewhfreqlists.out
grep despatch comparewhfreqlists.out
grep things comparewhfreqlists.out
grep token comparewhfreqlists.out
grep cost comparewhfreqlists.out
grep news comparewhfreqlists.out
grep poor comparewhfreqlists.out
# THE NEXT LINES GIVE TRIAD STATISTICS
#tudor women_triangles.py > women_triangles_mediator_model_less_strict ### COMMENTED OUT AS TIME-CONSUMING TO RUN, OUTPUT FILES PROVIDED
tudor women_hierarchies.py | grep "Number"
echo "Number of triads with feedforward loops:"
grep '>' WOMEN_TRIANGLES/women_triangles.out | awk -F'\t' '{print $1"\t@"$2"@"}' | grep -v '@0f->1m 1m->2m 2m->0f @' | grep -v '@1m->2f 2f->0f 0f->1m @' | awk '{print $1}' | paste -sd+ - | bc
echo "Ranking of women involved in at least four triangles, by position score (column 7) and within that by number of triangles (column 5):"  
sort -k7g -k5gr women_hierarchies_excl_mon.out | awk '{if ($5 != "1" && $5 != "2" && $5 != "3") print $0}'
echo "Number of such women:"
sort -k7g -k5gr women_hierarchies_excl_mon.out | awk '{if ($5 != "1" && $5 != "2" && $5 != "3") print $0}' | wc -l
echo
echo "Number of triads in (less strict) mediator model:"
wc -l women_triangles_mediator_model_less_strict
echo
