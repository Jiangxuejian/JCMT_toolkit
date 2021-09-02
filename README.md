### eaosql.py

##### A one-line python script to quickly search the database and get a file list.

   >python eaosql.py -h

   usage: eaosql.py  eaosql.py [instrument] [-p project-ID] [-d utdate] [-n obsnum] [-o object] [-m molecule]

   This script generate a simple SQL file and search the JCMT database; if
   neither project ID nor UTdate is provided, return all entries of today if
   available. It also generate a txt file which lists all data file paths. For
   complex and advance query, please use SQL directly, or use the generated .sql
   file as a starting point.

   positional arguments:
     {UU,HARP,SCUBA2,AWEOWEO}
                           enter Uu, Aweoweo, HARP or SCUBA2 (required input)

   optional arguments:
     -h, --help            show this help message and exit
     -p PROJECT, --project PROJECT
                           project code
     -n OBSNUM, --obsnum OBSNUM
                           observation number
     -o OBJECT, --object OBJECT
                           observing target
     -m MOLECULE, --molecule MOLECULE
                           observing line
     -d UTDATE, --utdate UTDATE
                           UT date in format of YYYYMMDD

Example: 

>python eaosql.py Uu -d 20210901

### Polarization-separated reduction (Nāmakanui specific)

> sh ./acsis_pol_sep.sh

The Nāmakanui instruments produce data from both sidebands and polarizations. It is strongly recommended by the observatory that users check the data for each polarisation separately before combining them to use the total intensity spectra. To do this, one can make use of the [bad receptors](http://starlink.eao.hawaii.edu/devdocs/sc20.htx/sc20ch6.html#x7-420004) mask, and run this script. One need to provide a text file (*filelist.lis*) containing raw data files to be reduced. Then the spectra in P0-only, P1-only and combined (as normal pipeline would produce) are under the folders *p0/*, *p1/* and *both*, respectively. Note, for the receptors, N stands for Nāmakanui, the next letter is either A for Alaihi, U for ʻŪʻū or W for ʻĀweoweo. The number corresponds to polarization 0 or 1, and the final letter is L or U for Lower or Upper sideband.



### Intensity ratio analysis script

(1) you may run *eaosql.py* (see above) to get the file list of the data you want to reduce;

(2) run *acsis_pol_sep.sh* to reduce the data;

(3) run *extract_spec_max.sh* to extract  the peak intensity data as csv file(s).

(4) use the python notebook to analysis and produce figures.

The script can combine multiple standard peak intensity data files for following analysis, which explore the relationships between the peaks at LSB, USB, P0 & P1 and other parameters (LO frequency, Tsys, utdate, etc.).
**prerequisite**:  one has extracted the peak intensity data as one or multiple files (stats-max.csv) and one also the sql data files (sql.tsv) 