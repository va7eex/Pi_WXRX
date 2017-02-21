#!/bin/bash

#Satellite we want to plan to record. ex: NOAA-19
SAT=$1
#current unix time
TIEMSTAMP=$(date +%s)
#make a file
FILENAME="sat_schedules/schd-${SAT}-${TIEMSTAMP}"

rm reschd-$SAT.txt

#from here out we generate a bash script to be executed at the time of a satellite pass

echo "#!/bin/bash" > $FILENAME

#meat and potatoes of the program
python satpredict.py
python satschedule.py $SAT >> $FILENAME

#regenerate the bash script for the next pass afterwards
echo "sleep 30" >> $FILENAME
echo "echo bash sats.sh ${SAT} > reschd-${SAT}.txt" >> $FILENAME
echo "at now + 30 minutes -q z -M -f reschd-${SAT}.txt" >> $FILENAME

echo "rm ${FILENAME}" >> $FILENAME

TIEM=$(<"${SAT}_sched.txt")
echo $TIEM

#commit to the action
at -M -m $TIEM < $FILENAME
rm "${SAT}_sched.txt"
