echo
echo "Chapter 8"
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
echo "Run places_book_script in PLACES folder for more results used in Chapter 8."
