import requests
import json
import array
import sys

web_tle = [ 'http://www.celestrak.com/NORAD/elements/weather.txt', 'https://www.celestrak.com/NORAD/elements/stations.txt' ]

sats_of_interest = { 'NOAA-15':'NOAA 15', 'NOAA-18':'NOAA 18', 'NOAA-19':'NOAA 19', 'METEOR-M1':'METEOR-M 1', 'METEOR-M2':'METEOR-M 2', 'ISS':'ISS (ZARYA)' }
#sats_of_interest = { 'NOAA-15':'NOAA 15' }


#page = urllib2.urlopen(web_noaa_tle)
#page = requests.get(web_noaa_tle, stream=True)

#NOAA 15 [B]             
#1 25338U 98030A   16173.50363904  .00000079  00000-0  52195-4 0  9991
#2 25338  98.7825 177.6616 0010829 167.3279 192.8174 14.25734916941605

data = {}
line_num = 0
cur_sat_line = -1
cur_sat = ""

def check_line1(str):
	if( len(str) == 69 ):
		fields = {}
		fields['line number'] = int(str[0:1])
		fields['satellite number + classification'] = str[3:9]
		fields['international designator'] = str[10:17]
		fields['epoch'] = float(str[19:32])
		fields['1st mean motion'] = float(str[34:43])
		fields['2nd mean motion'] = str[45:52]
		fields['BSTAR drag term'] = str[54:61]
		fields['the number 0'] = int(str[62:63])
		fields['element set number + checksum'] = int(str[65:69])
		
	else:
		return False
	return True

def check_line2(str):
	if( len(str) == 69 ):
		fields = {}
		fields['line number'] = str[0:1]
		fields['satellite number'] = str[3:7]
		fields['inclination'] = str[9:16]
		fields['right ascension'] = str[18:25]
		fields['eccentricity'] = str[27:33]
		fields['argument of perigee'] = str[35:42]
		fields['mean anomaly'] = str[44:51]
		fields['mean motion + revolution number + checksum'] = str[53:69]
		print fields
		return fields

		for field, data in fields.iteritems():
                        if( not float(data).isnum() ):
                                print field, data, "is not an number!"
                                return False
	else:
		return False
	return True

for tle in web_tle:
	page = requests.get(tle, stream=True)
	for line in page.iter_lines():
		#print '>>', line
		for hsat, sat in sats_of_interest.iteritems():
			if( line.startswith(sat) ):
				cur_sat_line = line_num
				cur_sat = hsat

		if( line_num == cur_sat_line + 1 and cur_sat_line >= 0 ):
			if( check_line1(line) ):
				data[cur_sat] = line
#			else:
#				sys.exit("Malformed Data (Line 1), Exiting. " + line)

		if( line_num == cur_sat_line + 2 and cur_sat_line >= 0 ):
			if( check_line2(line) ):
				data[cur_sat] = data[cur_sat] + '\n' + line
#			else:
#				sys.exit("Malformed Data (Line 2), Exiting. " + line)

		line_num = line_num + 1


for s, tle in data.iteritems():
	print s, '\n', tle

with open('sat_tle.txt', 'w') as fp:
	json.dump(data, fp)
