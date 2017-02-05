#!/bin/bash

SAT=$1
TIEMSTAMP=$(date +%s)
FILENAME="sat_schedules/schd-${SAT}-${TIEMSTAMP}"

rm reschd-$SAT.txt

echo "#!/bin/bash" > $FILENAME

echo 'bash wol_fastserv.sh' >> $FILENAME

python satpredict.py 25 1 true
python satschedule.py $SAT >> $FILENAME

echo "sleep 30" >> $FILENAME
echo "echo bash sats.sh ${SAT} > reschd-${SAT}.txt" >> $FILENAME
echo "at now + 30 minutes -q z -M -f reschd-${SAT}.txt" >> $FILENAME

echo "rm ${FILENAME}" >> $FILENAME

TIEM=$(<"${SAT}_sched.txt")
echo $TIEM

at -M -m $TIEM < $FILENAME
rm "${SAT}_sched.txt"
