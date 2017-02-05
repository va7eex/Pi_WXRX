import predict
import json
import sys
import datetime

frequencies = {'NOAA-15':'137.620M', 'NOAA-18':'137.9125M', 'NOAA-19':'137.10M', 'METEOR-M2':'137.925M', 'ISS':'145.80M' } #Meteor M2 is also on 137.1M

tle_data = json.load(open('sat_tle.txt'))
default_predictions = 1
default_min_elevation = 30
suppress_low_passes = False


pass_elevation = default_min_elevation
if( len(sys.argv) > 1 ):
	pass_elevation = int(sys.argv[1])

if( pass_elevation == '' ):
	pass_elevation = default_min_elevation

predictions = default_predictions
if( len(sys.argv) > 2):
	predictions = int(sys.argv[2])

if( predictions == '' ):
	predictions = default_predictions

if( len(sys.argv) > 3 ):
	suppress_low_passes = True

def convert_time( unixtime ):
    return datetime.datetime.fromtimestamp(
        int(unixtime)
    ).strftime('%H:%M %Y-%m-%d')

def convert_time_short( unixtime ):
    return datetime.datetime.fromtimestamp(
        int(unixtime)
    ).strftime('%M')

def get_sat( sat ):
	return sat + '\n' + tle_data[sat]

qth = (49.32, 123.42, 49)  # lat (N), long (W), alt (meters)
qth_nw = (51.32, 125.42, 49)
qth_se = (47.32, 121.42, 49)

data = {}

for sat, freq in frequencies.iteritems():

	name = predict.observe(get_sat(sat), qth)['name'].strip()
	t = predict.transits(get_sat(sat), qth)
	t_nw = predict.transits(get_sat(sat), qth_nw)
	t_se = predict.transits(get_sat(sat), qth_se)

	count = 0
	while ( count < predictions ):
		p = t.next()
		p_nw = t_nw.next()
		p_se = t_se.next()

		while (p.peak()['elevation'] < default_min_elevation):
			p = t.next()
			p_nw = t_nw.next()
			p_se = t_se.next()
			if( not suppress_low_passes ):
				print name, "pass too low, recalculating"

		data[name] = {}
		data[name]['frequency'] = freq
		data[name]['start_unix'] = p.start
		data[name]['start'] = convert_time(data[name]['start_unix'])
		data[name]['duration_seconds'] = int(p.duration())
		data[name]['duration_minutes'] = convert_time_short(data[name]['duration_seconds'])
		data[name]['elevation'] = p.peak()['elevation']

		#This actually means nothing, feel free to ignore it
		data[name]['direction'] = 'S' #Assume northbound
		if( int(p_nw.start) > int(p.start) and int(p.start) > int(p_se.start) ): #This is the direction the satellite is travelling TO, not from.

			data[name]['direction'] = 'N'	

		print name, 'next pass at:', data[name]['start'], 'at', data[name]['elevation'], 'degrees.', data[name]['direction'] + '-bound'
		count = count + 1

import json

with open('satpredict.txt', 'w') as fp:
    json.dump(data, fp, indent=4)

