echo 
echo "Chapter 4"
echo "========="
echo
echo "Network signature for Tommaso Spinelli (30206) during reign of Henry VIII"
echo
python indivnetworkstats.py 30206 15090422 15470128
echo
grep hen bigrank.out | grep 30206 
echo
echo "Network signature for Robert Bowes (26415) during 1580s"
echo
python indivnetworkstats.py 26415 15800000 15900000
echo
grep Decade_8 bigrank.out | grep 26415 
echo
echo "Network signature for Edward Courtenay (7813) during reign of Mary I"
echo
python indivnetworkstats.py 7813 15530706 15581117
echo
grep mar bigrank.out | grep 7813 
echo
