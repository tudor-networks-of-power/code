awk -F'\t' '{print $3"\t"$1"\t"$2"\t"$4"\t"$5"\t"$6"\t"$7"\t"$8}' fromto_all_place_mapped | sort -n | awk -F'\t' '{print $2"\t"$3"\t"$1"\t"$4"\t"$5"\t"$6"\t"$7"\t"$8}' > fromto_all_place_mapped_sorted