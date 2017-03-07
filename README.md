# Pi_WXRX
Receive and decode NOAA satellites with a Raspberry Pi.

This requires the following:
* Osmocom RTLSDR library: https://github.com/osmocom/rtl-sdr
* PyPredict: https://github.com/nsat/pypredict

Edit satpredict.py and change the "qth" variable to your lat/long/alt.

To begin please run get_tle.py, preferably add it to a daily cron task. Afterwards run "bash sats.sh NOAA-##" for NOAA-15, -18, or -19 (your preference). The sats.sh file runs itself after completion so there are few reasons to run it twice. If you must rerun the sats.sh script you will need to wipe the At Queue, see below.

Occasionally things will get backed up and its best to clear everything in the pending At jobs with the following command:

   for i in `atq | awk '{print $1}'`;do atrm $i;done
