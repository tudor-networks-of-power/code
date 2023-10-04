grep all ~/Dropbox/DropboxDisambiguation/bigrank_ruth.out.test2 | awk '{print $7"\t"$8}' > all.inoutstr
grep hen ~/Dropbox/DropboxDisambiguation/bigrank_ruth.out.test2 | awk '{print $7"\t"$8}' > hen.inoutstr
grep edw ~/Dropbox/DropboxDisambiguation/bigrank_ruth.out.test2 | awk '{print $7"\t"$8}' > edw.inoutstr
grep mar ~/Dropbox/DropboxDisambiguation/bigrank_ruth.out.test2 | awk '{print $7"\t"$8}' > mar.inoutstr
grep eli ~/Dropbox/DropboxDisambiguation/bigrank_ruth.out.test2 | awk '{print $7"\t"$8}' > eli.inoutstr
gnuplot inoutstr.plotscript
