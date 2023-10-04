echo
echo "Chapter 3"
echo "========="
echo 
echo "Top thirty individuals by betweenness in first decade of Henry VIII's reign:"
echo
grep Decade_1 bigrank.out | sort -g -k10 -r | head -n 30 | awk '{print $2"\t"$10}' > cc
grep Decade_1 bigrank.out | sort -g -k10 -r | head -n 30 | awk '{print $2}' | xargs -I{} grep @{}@ namelist > aa
echo
paste cc aa > dd
head -n 30 dd
echo
echo "Top thirty individuals by betweenness in the 1580s:"
echo
grep Decade_8 bigrank.out | sort -g -k10 -r | head -n 30 | awk '{print $2"\t"$10}' > cc
grep Decade_8 bigrank.out | sort -g -k10 -r | head -n 30 | awk '{print $2}' | xargs -I{} grep @{}@ namelist > aa
echo
paste cc aa > dd
head -n 30 dd
echo
echo
echo "Top twenty links by strength in first decade of Henry VIII's reign:"
grep Decade_1 bigedgerank.out | sort -n -k4 -r | head -n 25 | awk '{print $2"\t"$3"\t"$4}' > cc
grep Decade_1 bigedgerank.out | sort -n -k4 -r | head -n 25 | awk '{print $2}' | xargs -I{} grep @{}@ namelist > aa
echo
grep Decade_1 bigedgerank.out | sort -n -k4 -r | head -n 25 | awk '{print $3}' | xargs -I{} grep @{}@ namelist > bb
paste cc aa bb > dd
head -n 25 dd
echo
echo "Note that the above list shows 25 entries to allow for the inclusion of multiple people with equal rank at position 20."
echo
echo 
echo "Spinelli's eigenvector centrality during Henry VIII's reign:"
echo
grep hen bigrank.out | grep 30206 | awk '{print $9" rank: "$11}' 
echo
echo "Number of correspondents in Henry VIII's reign:"
echo
grep hen bigrank.out | wc | awk '{print $1}'
echo
