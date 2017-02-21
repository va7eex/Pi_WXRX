import predict
import json
import sys
import datetime

#Frequencies that satellites transmit on.
frequencies = {'NOAA-15':'137.620M', 'NOAA-18':'137.9125M', 'NOAA-19':'137.10M', 'METEOR-M2':'137.925M', 'ISS':'145.80M' } #Meteor M2 is also on 137.1M

tle_data = json.load(open('sat_tle.txt'))
default_predictions = 1 #how many predictions do we want to predict in advance
default_min_elevation = 30 #how low the angle of the satellitie pass is allowed to be if we want to record a pass
suppress_low_passes = False #Less console spam if you enable this.

#You can change the default elevation with the first parameter
pass_elevation = default_min_elevation
if( len(sys.argv) > 1 ):
	pass_elevation = int(sys.argv[1])

if( pass_elevation == '' ):
	pass_elevation = default_min_elevation

#you can change the number of predictions per satellite with the second parameter
predictions = default_predictions
if( len(sys.argv) > 2):
	predictions = int(sys.argv[2])

if( predictions == '' ):
	predictions = default_predictions

#anything in the third parameter will turn off console spam
if( len(sys.argv) > 3 ):
	suppress_low_passes = True

#format a unix timestamp in a time appropriate for the 'at' command
def convert_time( unixtime ):
    return datetime.datetime.fromtimestamp(
        int(unixtime)
    ).strftime('%H:%M %Y-%m-%d')

#format the unix timestamp for minutes, used to determine length of recording
def convert_time_short( unixtime ):
    return datetime.datetime.fromtimestamp(
        int(unixtime)
    ).strftime('%M')

def get_sat( sat ):
	return sat + '\n' + tle_data[sat]

#Where on the earth you are. Change this to your location
qth = (49.5, 123.5, 50)  # lat (N), long (W), alt (meters)

data = {}

for sat, freq in frequencies.iteritems():

	name = predict.observe(get_sat(sat), qth)['name'].strip()
	t = predict.transits(get_sat(sat), qth)

	count = 0
	while ( count < predictions ):
		p = t.next()
		p_nw = t_nw.next()
		p_se = t_se.next()

		#peak check. PEAK CHECK!
		while (p.peak()['elevation'] < default_min_elevation):
			p = t.next()
			p_nw = t_nw.next()
			p_se = t_se.next()
			if( not suppress_low_passes ):
				print name, "pass too low, recalculating"

		#this is the data we want to pass on to the rest of the program
		data[name] = {}
		data[name]['frequency'] = freq
		data[name]['start_unix'] = p.start
		data[name]['start'] = convert_time(data[name]['start_unix'])
		data[name]['duration_seconds'] = int(p.duration())
		data[name]['duration_minutes'] = convert_time_short(data[name]['duration_seconds'])
		data[name]['elevation'] = p.peak()['elevation']

		print name, 'next pass at:', data[name]['start'], 'at', data[name]['elevation'], 'degrees.'
		count = count + 1

import json

with open('satpredict.txt', 'w') as fp:
    json.dump(data, fp, indent=4)

