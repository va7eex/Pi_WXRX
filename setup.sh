apt-get update
apt-get install git cmake make libusb-1.0-0-dev python-dev
git clone https://github.com/nsat/pypredict
python pypredict/setup.py install
mkdir sat_scheds
mkdir sat_output
python get_tle.py
bash sats.sh NOAA-15
bash sats.sh NOAA-18
bash sats.sh NOAA-19
