apt-get update
apt-get install git cmake make libusb-1.0-0-dev python-dev
git clone https://github.com/nsat/pypredict
python pypredict/setup.py install
mkdir sat_scheds
mkdir sat_output
