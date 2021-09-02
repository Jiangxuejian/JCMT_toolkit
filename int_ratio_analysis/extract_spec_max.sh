#!/bin/bash
# Xue-Jian Jiang

# This script use kappa/stats to extract a table consisting
# of basic info and the maximum value (peak) of the reduced spectra.
# returns a stats-max.csv file

source /star/etc/profile
kappa
[ ! -e stats-max.txt ] || rm stats-max.txt
for d in p0 p1 both     # replace "p0 p1 both" with the folder(s) that contains your data 
do
    for r in $d/a*reduced001.sdf
   	do
		echo $r
        echo $r >> stats-max.txt
        fitsval $r object | sed "s/ /-/g" >> stats-max.txt
    	fitsval $r molecule >> stats-max.txt
    	fitsval $r TRANSITI >> stats-max.txt
    	fitsval $r OBS_SB >> stats-max.txt
       	fitsval $r BWMODE >> stats-max.txt
    #   this line extract the maximal value (peak) of a spectrum.
       	stats $r | grep "Max" | awk '{print $5}' >> stats-max.txt
		rr=$(basename $r .sdf)
    #	This line extract the TSYS value
    	hdstrace $d/$rr.MORE.SMURF.TSYS.DATA_ARRAY.DATA  | grep "DATA(" | awk '{print $2}' | sed 's/,/\n/g' | sed -n 1p >> stats-max.txt
    done
done



# https://www.folkstalk.com/2013/03/sed-remove-lines-file-unix-examples.html
sed -i "/^$/d" stats-max.txt                                            # remove empty lines
sed -i "s/ - /-/g" stats-max.txt                                        # remove empty lines
sed -i "s/\(a\s*\|reduced001\s*\|sm\s*\|.sdf\s*\)//g" stats-max.txt     # remove certain words
sed -i "s/\(\/\s*\|_\s*\)/ /g" stats-max.txt                            # replace _ with space
cat stats-max.txt | xargs -n8 -d'\n' > stats-max.dat    # merge every 8 lines

# now make a CSV table
echo "pol,utdate,obsnum,subsysnr,object,molecule,transition,obs_sb,bwmode,peak,tsys" > stats-max.csv    # table header
sed -e "s/[[:space:]]\+/,/g" stats-max.dat >> stats-max.csv             # replace space with comma.
rm stats-max.txt
