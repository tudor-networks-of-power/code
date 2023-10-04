echo "Chapter 2"
echo "========="
echo
echo "Degree distributions:"
./degdist_script.sh
open degdist.ps
echo
python cumuldeg.py > cumuldeg.out
echo "Total numbers of people in each reign network:"
grep '100\.0%' cumuldeg.out | grep 'greater' | awk -F'people' '{print $1}'
echo
echo "Note: The figure for the entire Tudor period differs slightly from the 20560 individuals in the full edge list as the network analysis code filters out 27 people whose only letters either have no dates in the original State Papers Online XML metadata, or whose date fields in this data contain a particular error, namely that the tdate precedes the fdate." 
echo
echo 
echo "Top three for degree in Henry's reign:"
grep hen bigrank.out | sort -n -k3 -r | head -n 3 | awk '{print $2"\t"$3}'
echo "IDs decoded:"
grep hen bigrank.out | sort -n -k3 -r | head -n 3 | awk '{print $2}' | xargs -I{} grep @{}@ namelist
echo
echo "Top three for degree in Edward's reign:"
grep edw bigrank.out | sort -n -k3 -r | head -n 3 | awk '{print $2"\t"$3}'
echo "IDs decoded:"
grep edw bigrank.out | sort -n -k3 -r | head -n 3 | awk '{print $2}' | xargs -I{} grep @{}@ namelist
echo
echo "Top three for degree in Mary's reign:"
grep mar bigrank.out | sort -n -k3 -r | head -n 3 | awk '{print $2"\t"$3}'
echo "IDs decoded:"
grep mar bigrank.out | sort -n -k3 -r | head -n 3 | awk '{print $2}' | xargs -I{} grep @{}@ namelist
echo
echo "Top three for degree in Elizabeth's reign:"
grep eli bigrank.out | sort -n -k3 -r | head -n 3 | awk '{print $2"\t"$3}'
echo "IDs decoded:"
grep eli bigrank.out | sort -n -k3 -r | head -n 3 | awk '{print $2}' | xargs -I{} grep @{}@ namelist
echo
echo "For details of cumulative distribution, see cumuldeg.out."
echo
echo "Top ten for degree in Edward's reign:"
grep edw bigrank.out | sort -n -k3 -r | head -n 10 | awk '{print $2"\t"$3}'
echo "IDs decoded:"
grep edw bigrank.out | sort -n -k3 -r | head -n 10 | awk '{print $2}' | xargs -I{} grep @{}@ namelist
echo
echo "In-strength versus out-strength:"
./inoutstr_script.sh
open inoutstr.ps
open inoutstr_all.ps
echo
echo "Number of people in the network analysis dataset (see Note above):"
grep all bigrank.out | wc -l 
grep all bigrank.out | wc -l > a
echo
echo "Number of people in the archive whose out-strength exceeds their in-strength:"
grep all bigrank.out | awk '$7 > $8 {print "0"} $7 <= $8 {print "1"}' | grep 0 | wc -l
grep all bigrank.out | awk '$7 > $8 {print "0"} $7 <= $8 {print "1"}' | grep 0 | wc -l > b
echo
paste a b > c
echo "Percentage of people in the archive whose out-strength exceeds their in-strength:"
awk '{print "100.0*"$2"/"(1.0*$1)}' c | bc -l
echo
echo "Maximum out-strength among individuals who receive exactly one letter (in-strength = 1):"
grep all bigrank.out | awk '$8 == 1 && $7 >= 1 {print $7}' | sort -n | tail -n 1
echo 
echo "Number of individuals who receive exactly one letter (in-strength = 1) and send at least one letter:"
grep all bigrank.out | awk '$8 == 1 && $7 >= 1 {print $7}' | wc -l
echo
echo "Top 15 for in-strength in Henry's reign (with out-strength given too):"
grep hen bigrank.out | sort -n -k8 -r | head -n 15 | awk '{print $2"\t"$8"\t"$7}'
echo "IDs decoded:"
grep hen bigrank.out | sort -n -k8 -r | head -n 15 | awk '{print $2}' | xargs -I{} grep @{}@ namelist
echo
echo "Top ten for in-strength in Edward's reign (with out-strength given too):"
grep edw bigrank.out | sort -n -k8 -r | head -n 10 | awk '{print $2"\t"$8"\t"$7}'
echo "IDs decoded:"
grep edw bigrank.out | sort -n -k8 -r | head -n 10 | awk '{print $2}' | xargs -I{} grep @{}@ namelist
echo
echo "Top ten for in-strength in Mary's reign (with out-strength given too):"
grep mar bigrank.out | sort -n -k8 -r | head -n 10 | awk '{print $2"\t"$8"\t"$7}'
echo "IDs decoded:"
grep mar bigrank.out | sort -n -k8 -r | head -n 10 | awk '{print $2}' | xargs -I{} grep @{}@ namelist
echo
echo "Top ten for in-strength in Elizabeth's reign (with out-strength given too):"
grep eli bigrank.out | sort -n -k8 -r | head -n 10 | awk '{print $2"\t"$8"\t"$7}'
echo "IDs decoded:"
grep eli bigrank.out | sort -n -k8 -r | head -n 10 | awk '{print $2}' | xargs -I{} grep @{}@ namelist
echo
echo "Top thirty out-strength outliers above the diagonal line with in-degree >= 3 and out-degree > 150:"
grep hen bigrank.out | awk '{if($7*$8 > 0 && $8 >= 3 && $7 > 150){a = log($7/$8);printf($2" %0.4f "$7" "$8"\n",a)}}' | sort -k2 -r -n | head -n 30 > a
grep hen bigrank.out | awk '{if($7*$8 > 0 && $8 >= 3 && $7 > 150){a = log($7/$8);printf($2" %0.4f\n",a)}}' | sort -k2 -r -n | head -n 30 | awk '{print $1}' | xargs -I{} grep @{}@ namelist > b
paste a b
echo
echo "Statistics for Secretaries of State:"
echo
echo "Dates in office      degree      in-strength      name"
#33300   Thomas Ruthall, Bishop of Durham
python indivnetworkstats.py 33300 15000000 15161231 | grep -v ID | grep -v brackets | awk -F'\t' '{print $2"-"$3"\t"$4"\t"$9"\t"$10}'
#25883   Richard Pace
python indivnetworkstats.py 25883 15160101 15261231 | grep -v ID | grep -v brackets | awk -F'\t' '{print $2"-"$3"\t"$4"\t"$9"\t"$10}'
#35636   William Knight, Bishop of Bath and Wells
python indivnetworkstats.py 35636 15260101 15290805 | grep -v ID | grep -v brackets | awk -F'\t' '{print $2"-"$3"\t"$4"\t"$9"\t"$10}'
#30994   Stephen Gardiner, Bishop of Winchester
python indivnetworkstats.py 30994 15290805 15340430 | grep -v ID | grep -v brackets | awk -F'\t' '{print $2"-"$3"\t"$4"\t"$9"\t"$10}'
#32545   Thomas Cromwell, Earl of Essex
python indivnetworkstats.py 32545 15340101 15400430 | grep -v ID | grep -v brackets | awk -F'\t' '{print $2"-"$3"\t"$4"\t"$9"\t"$10}'
#33564   Thomas Wriothesley, Earl of Southampton
python indivnetworkstats.py 33564 15400401 15440131 | grep -v ID | grep -v brackets | awk -F'\t' '{print $2"-"$3"\t"$4"\t"$9"\t"$10}'
#29617   Sir Ralph Sadler
python indivnetworkstats.py 29617 15400401 15430423 | grep -v ID | grep -v brackets | awk -F'\t' '{print $2"-"$3"\t"$4"\t"$9"\t"$10}'
#35838   Sir William Paget
python indivnetworkstats.py 35838 15430423 15480430 | grep -v ID | grep -v brackets | awk -F'\t' '{print $2"-"$3"\t"$4"\t"$9"\t"$10}'
#30594   Sir William Petre
python indivnetworkstats.py 30594 15440101 15570331 | grep -v ID | grep -v brackets | awk -F'\t' '{print $2"-"$3"\t"$4"\t"$9"\t"$10}'
#30198   Sir Thomas Smith
python indivnetworkstats.py 30198 15480417 15491015 | grep -v ID | grep -v brackets | awk -F'\t' '{print $2"-"$3"\t"$4"\t"$9"\t"$10}'
#23020   Nicholas Wotton
python indivnetworkstats.py 23020 15491015 15500905 | grep -v ID | grep -v brackets | awk -F'\t' '{print $2"-"$3"\t"$4"\t"$9"\t"$10}'
#30478   Sir William Cecil, Lord Burghley
python indivnetworkstats.py 30478 15500905 15530731 | grep -v ID | grep -v brackets | awk -F'\t' '{print $2"-"$3"\t"$4"\t"$9"\t"$10}'
#29093   Sir John Cheke
python indivnetworkstats.py 29093 15530601 15530731 | grep -v ID | grep -v brackets | awk -F'\t' '{print $2"-"$3"\t"$4"\t"$9"\t"$10}'
#29066   Sir John Bourne
python indivnetworkstats.py 29066 15530701 15580430 | grep -v ID | grep -v brackets | awk -F'\t' '{print $2"-"$3"\t"$4"\t"$9"\t"$10}'
#29067   Sir John Boxall
python indivnetworkstats.py 29067 15570301 15581130 | grep -v ID | grep -v brackets | awk -F'\t' '{print $2"-"$3"\t"$4"\t"$9"\t"$10}'
#30478   Sir William Cecil, Lord Burghley
python indivnetworkstats.py 30478 15581101 15720713 | grep -v ID | grep -v brackets | awk -F'\t' '{print $2"-"$3"\t"$4"\t"$9"\t"$10}'
#30198   Sir Thomas Smith
python indivnetworkstats.py 30198 15720713 15760331 | grep -v ID | grep -v brackets | awk -F'\t' '{print $2"-"$3"\t"$4"\t"$9"\t"$10}'
#28530   Sir Francis Walsingham
python indivnetworkstats.py 28530 15731220 15900430 | grep -v ID | grep -v brackets | awk -F'\t' '{print $2"-"$3"\t"$4"\t"$9"\t"$10}'
#6482    Dr Thomas Wilson
python indivnetworkstats.py 6482 15771112 15810616 | grep -v ID | grep -v brackets | awk -F'\t' '{print $2"-"$3"\t"$4"\t"$9"\t"$10}'
#35310   William Davison
python indivnetworkstats.py 35310 15860930 15870228 | grep -v ID | grep -v brackets | awk -F'\t' '{print $2"-"$3"\t"$4"\t"$9"\t"$10}'
#30478   Sir William Cecil, Lord Burghley
python indivnetworkstats.py 30478 15900705 15960731 | grep -v ID | grep -v brackets | awk -F'\t' '{print $2"-"$3"\t"$4"\t"$9"\t"$10}'
#29809   Sir Robert Cecil, Earl of Salisbury
python indivnetworkstats.py 29809 15960701 16120524 | grep -v ID | grep -v brackets | awk -F'\t' '{print $2"-"$3"\t"$4"\t"$9"\t"$10}'
#29181   Sir John Herbert
python indivnetworkstats.py 29181 16000510 16170709 | grep -v ID | grep -v brackets | awk -F'\t' '{print $2"-"$3"\t"$4"\t"$9"\t"$10}'
echo
echo "Further statistics for Ruthall, Pace, Knight, and Gardiner:"
echo "Dates in office    total strength      name"
python indivnetworkstats.py 33300 15000000 15161231 | grep -v ID | grep -v brackets | awk -F'\t' '{print $2"-"$3"\t"$7"\t"$10}'
python indivnetworkstats.py 25883 15160101 15261231 | grep -v ID | grep -v brackets | awk -F'\t' '{print $2"-"$3"\t"$7"\t"$10}'
python indivnetworkstats.py 35636 15260101 15290805 | grep -v ID | grep -v brackets | awk -F'\t' '{print $2"-"$3"\t"$7"\t"$10}'
python indivnetworkstats.py 30994 15290805 15340430 | grep -v ID | grep -v brackets | awk -F'\t' '{print $2"-"$3"\t"$7"\t"$10}'
echo
echo "Rankings during their time in office:"
echo
echo "Ruthall:"
python indivnetworkstats.py 15000000 15161231 
head -n 10 ins_wdeg_15000000_15161231 
echo 
echo "Pace:"
python indivnetworkstats.py 15160101 15261231
head -n 10 ins_wdeg_15160101_15261231 
echo 
echo "Knight:"
python indivnetworkstats.py 15260101 15290805 
head -n 10 ins_wdeg_15260101_15290805 
echo 
echo "Gardiner:"
python indivnetworkstats.py 15290805 15340430
head -n 10 ins_wdeg_15290805_15340430

