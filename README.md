# Pi_WXRX
Receive and decode NOAA satellites with a Raspberry Pi.

This requires the following:
* Osmocom RTLSDR library: https://github.com/osmocom/rtl-sdr
* PyPredict: https://github.com/osmocom/rtl-sdr

To begin please run get_tle.py, preferably add it to a daily cron task. Afterwards run "bash sats.sh NOAA-##" for NOAA-15, -18, or -19 (your preference).

Occasionally things will get backed up and its best to clear everything in the pending At jobs with the following command:

   for i in `atq | awk '{print $1}'`;do atrm $i;done
