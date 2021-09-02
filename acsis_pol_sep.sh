# Note that this script use the REDUCE_SCIENCE_NARROWLINE recipe for the
# pipeline, if you want to use other recipes please change the recipe
# accordingly.
recipe=REDUCE_SCIENCE

#!/bin/bash
export STARLINK_DIR=/stardev
source $STARLINK_DIR/etc/profile

for dir in p0 p1 both
do
	if [ -e "$dir" ]; then
    	echo "Directory $dir exists."
	else
		mkdir $dir
	fi
done


oracdr_acsis

# reduce only P0
ORAC_DATA_IN=$(pwd)
ORAC_DATA_OUT=$(pwd)/p0
# define P1 as "bad receptor"
echo "NW1L NW1U NU1L NU1U NA1L NA1U" >> $ORAC_DATA_OUT/bad_receptors.lis 
echo "=================================================================="
echo " mask NW1L NW1U NU1L NU1U NA1L NA1U from the reduction "
echo "=================================================================="

oracdr -loop file -file "$ORAC_DATA_IN"/filelist.lis -nodisplay -log sf\
 -verbose -calib bad_receptors=FILE "$recipe"

echo "=================================================================="
echo "            P0 reduction completed "
echo "=================================================================="

# reduce only P1
export ORAC_DATA_IN=$(pwd)
export ORAC_DATA_OUT=$(pwd)/p1
# define P0 as "bad receptor"
echo "NW0L NW0U NU0L NU0L NA0L NA0U" >> $ORAC_DATA_OUT/bad_receptors.lis 
echo "=================================================================="
echo " mask NW0L NW0U NU0L NU0L NA0L NA0U from the reduction "
echo "=================================================================="

oracdr -loop file -file $ORAC_DATA_IN/filelist.lis -nodisplay -log sf\
 -verbose -calib bad_receptors=FILE "$recipe"
echo "=================================================================="
echo "            P1 reduction completed "
echo "=================================================================="
 
# reduce both pol
export ORAC_DATA_IN=$(pwd)
export ORAC_DATA_OUT=$(pwd)/both

oracdr -loop file -file $ORAC_DATA_IN/filelist.lis -nodisplay -log sf\
 -verbose "$recipe"
echo "=================================================================="
echo "            both reduction completed "
echo "=================================================================="
