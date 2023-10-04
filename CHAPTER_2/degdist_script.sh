grep all ~/Dropbox/DropboxDisambiguation/bigrank_ruth.out.test2 | awk '{print $3}' > all.deg
grep hen ~/Dropbox/DropboxDisambiguation/bigrank_ruth.out.test2 | awk '{print $3}' > hen.deg
grep edw ~/Dropbox/DropboxDisambiguation/bigrank_ruth.out.test2 | awk '{print $3}' > edw.deg
grep mar ~/Dropbox/DropboxDisambiguation/bigrank_ruth.out.test2 | awk '{print $3}' > mar.deg
grep eli ~/Dropbox/DropboxDisambiguation/bigrank_ruth.out.test2 | awk '{print $3}' > eli.deg
python histogram.py all.deg > all.deg.hist
python histogram.py hen.deg > hen.deg.hist
python histogram.py edw.deg > edw.deg.hist
python histogram.py mar.deg > mar.deg.hist
python histogram.py eli.deg > eli.deg.hist
gnuplot ~/Dropbox/DropboxDisambiguation/degdist.plotscript
