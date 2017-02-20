
#!/bin/bash

#render_options=("ZA" "HVCT" "NO")
render_options=("HVCT")
render_options_night=("MCIR")

direction=${f:(-7):(-6)}
echo $1
#remove the directory structure from the first argument
file="${1#'/tmp/'}"

#Isolate data values from filename file should begin with YYYYMMDD-HHMM
dyear=${file:(0):(4)}
dmonth=${file:(4):(2)}
dday=${file:(6):(2)}
dhour=${file:(9):(2)}
dminute=${file:(11):(2)}

#Convert file date to unix timestamp, probably don't have to do this but I am.
unixtimestamp=$(date --date="${dyear}/${dmonth}/${dday} ${dhour}:${dminute}" +%s)

#Debug, make sure the file stripper works
echo "${dyear}/${dmonth}/${dday} ${dhour}:${dminute} /" $unixtimestamp

#Render options for all NOAA satellites in orbit
#Put a big cross on receiver's location
#-gRSCFH are for turning on/off the overlays such as long/lat, cities, lakes, borders, etc.
#-H selects the TLE file
#-o is when the satellite is overhead forward one minute from the filename just to ensure that the predictor wxmap uses agrees with the pypredict predictor
wxmap -T "NOAA 15" -T "NOAA 18" -T "NOAA 19" -n "Vancouver,Canada" -g 0 -R 0 -S 1 -C 1 -F 0 -H ~/satellites/weather.txt -o $(($unixtimestamp+60)) /tmp/passmap.png

#If pass is at night time render differently for daytime.
if [[ $dhour -le 8 ]] || [[ $dhour -ge 17 ]]
then
        echo "Pass is at night"
        for r in "${render_options_night[@]}"
        do
                echo "Now rendering option: ${r}"

                wxtoimg -e $r -ocK -m /tmp/passmap.png /tmp/$file /tmp/$file"_${r}".png
        done
else
        echo "Pass is in sun"
        for r in "${render_options[@]}"
        do
                echo "Now rendering option: ${r}"

                wxtoimg -e $r -ocK -m /tmp/passmap.png /tmp/$file /tmp/$file"_${r}".png
        done
fi

#Upload.
bash ~/satellites/ftp.sh /tmp/$file"_${r}".png
