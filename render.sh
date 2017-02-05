
#!/bin/bash

render_options=("ZA" "HVCT" "NO")

f=$1

echo $f
f1="${f:0:(-4)}"
f2="${f1#'/tmp/'}"

echo $f2

wxmap -T "NOAA-15" -T "NOAA-18" -T "NOAA-19" -n "Spuzzum,Canada" -H ~/sat_tle.txt -o "${2}" /tmp/passmap.png

for r in "${render_options[@]}"
do
	echo "Now rendering option: ${r}"
	wxtoimg -e $r -ocK -m /tmp/passmap.png /tmp/$f2.wav /tmp/$f2"_${r}".png

	bash ~/ftp.sh /tmp/$f2"_${r}".png
done
