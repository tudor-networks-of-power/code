echo
echo "Chapter 6"
echo "========="
echo
echo "Finding most changed words:"
echo
python extractchanges.py
echo
echo "Fractional ranking of 'divorce' in changed words:"
grep divorce -n extractchanges.out | head -n 1 | awk -F: '{print $1}' > tmp
wc -l extractchanges.out | awk '{print $1}' >> tmp
paste -sd/ tmp | bc -l
echo 
echo "Generating the peak figures..."
echo
./wordlist_script.sh 
echo 
echo "Generating the topic network figures..."
echo 
./extractwordnetwork_figure_script.sh
echo

