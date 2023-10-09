echo "This is a second script for Chapter 6 that extracts networks for the most prominent peaks and measures their modularity."
echo "It takes a while to run and has therefore been separated from the main Chapter 6 results script."
echo 
echo "Generating networks for the most significant peaks..."
echo
mkdir CHANGE_PROFILES
./extractchanges_profiles.script.sh
python extractpeaks.py
echo
echo "Ranking words according to modularity:"
echo 
./make_time_communities_list.sh
python word_network_comm_time.py
sort -grk4 word_network_comm_time.out 
