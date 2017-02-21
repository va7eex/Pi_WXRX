import array
import json
import sys
import time
import datetime


ppmshift = '1' #adjust this if you don't have a TCXO equipped RTLSDR	
name = sys.argv[1].upper() #what satellite we're using
input_sample_rate = '48000' #actually the bandwidth of the audio sample we're taking from the RTLSDR
output_sample_rate = '11025' #what we downconvert to to play nicely with wxtoimg
gain = '40' #software gain
gain_lower_pass = gain #we can add more or less gain if a satellite is at a lower elevation, currently disabled
gain_lower_pass_requirement = 40

data = json.load(open('satpredict.txt'))

af_folder = '/tmp/'
output_folder = '~/sat_output/'

#this line is depreciated, make it a zero element array to do rtl_power surveys of the downline band
wxtoimg_options = ['HVCT', 'MCIR', 'NO']

#set options for various to-bash lines
#I don't recommend touching any of these
rtl_fm_options = {	'-f':data[name]['frequency'],
			'-M':'fm',
			'-p':ppmshift,
			'-F':'9',
			'-s':input_sample_rate,
			'-g':gain,
			'-E': 'dc',
			'-A': 'fast' }

rtl_power_options = {	'-f':'136.9M:138.1M:4k',
			'-g':gain,
			'-i':'1s',
			'-e':str(data[name]['duration_seconds']) + 's',
			'-p':ppmshift,
			'-c':'0.2' }

#I REALLY don't recommend touching these, stuff breaks without it and I can't explain why
sox_options = [		'-b16',
			'-c1',
			'-V1',
			'-es',
			'-r ' + input_sample_rate,
			'-t raw' ]

#depreciated
def filename(satname, part):
	if(part != ''):
		return satname + '_' + part + '.wav'
	return satname + '.wav'

def datestamp( unixtime ):
    return datetime.datetime.fromtimestamp(
        int(unixtime)
    ).strftime('%Y%m%d-%H%M_')

def convert_time( unixtime ):
    return datetime.datetime.fromtimestamp(
        int(unixtime)
    ).strftime('%H:%M %Y-%m-%d')

#gain adjustment based on pass elevationg
if( data[name]['elevation'] < gain_lower_pass_requirement ):
	gain = gain_lower_pass

#a bash line
timeoutstr = 'timeout ' + str(data[name]['duration_seconds'])
#a filename
filename = datestamp(data[name]['start_unix']) + name + '_' + str(int(data[name]['elevation']))

#I may or may not have forgotten to specify you need the heatmap.py from the rtl_power page on keenerd.
if( len(wxtoimg_options) == 0 ):

	rtlpower = 'rtl_power -f 137M:138M:4k -g ' + gain + ' -i 1s -e ' + str(data[name]['duration_seconds']) + 's -p ' + ppmshift + ' -c 0.2 ' + output_folder + filename + '.csv'
	heatmap = 'python heatmap.py ' + output_folder + name + '_' + str(int(data[name]['elevation'])) + '_' + timestamp + '.csv ' + output_folder + name + '_' + data[name]['direction'] + str(int(data[name]['elevation'])) + '_' + timestamp + '.png'

	print timeoutstr, rtlpower
	print heatmap
	print 'bash ftp.sh ' + output_folder + name + '_' + str(int(data[name]['elevation'])) + '_' + timestamp + '.png'

else:

	timeoutstr = 'timeout ' + str(data[name]['duration_seconds'])

	rtlstr = 'rtl_fm'
	for k, v in rtl_fm_options.iteritems():
		rtlstr = rtlstr + ' ' + k + ' ' + v

	soxstr = 'sox'
	for v in sox_options:
		soxstr = soxstr + ' ' + v

	print timeoutstr, rtlstr, af_folder + filename + '.raw'
	print soxstr, af_folder + filename + '.raw', af_folder + filename + '.wav', 'rate 11025'
	print 'touch -r', af_folder + filename + '.raw', af_folder + filename + '.wav'
	print 'bash', 'render.sh', af_folder + filename + '.wav'
		
f = open(name + '_sched.txt', 'w')
f.write(convert_time(data[name]['start_unix']))

#Depreciated, use render.sh
#for opt in wxtoimg_options:
#	filename = datestamp(data[name]['start_unix']) + name + '_' + str(int(data[name]['elevation']))
#
#	print 'wxtoimg' + ' -e', opt, af_folder + filename + '.wav', output_folder + filename + '_' + opt + '.png'
#
#	print 'bash ftp.sh', output_folder + filename + '_' + opt + '.png'
