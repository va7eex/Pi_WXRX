import array
import json
import sys
import time
import datetime


ppmshift = '1'			
name = sys.argv[1].upper()
input_sample_rate = '48000'
output_sample_rate = '11025'
gain = '40'
gain_lower_pass = gain
gain_lower_pass_requirement = 40

data = json.load(open('satpredict.txt'))

af_folder = '/tmp/'
output_folder = '~/sat_output/'

wxtoimg_options = ['HVCT', 'MCIR', 'NO'] #['ZA', 'HVCT', 'therm']

rtl_fm_options = {	'-f':data[name]['frequency'],
			'-M':'fm',
			'-p':ppmshift,
			'-F':'9',
			'-s':input_sample_rate,
			'-g':gain,
			'-E': 'dc',
			'-A': 'fast' }

rtl_power_options = {	'-f':'137M:138M:4k',
			'-g':gain,
			'-i':'1s',
			'-e':str(data[name]['duration_seconds']) + 's',
			'-p':ppmshift,
			'-c':'0.2' }

sox_options = [		'-b16',
			'-c1',
			'-V1',
			'-es',
			'-r ' + input_sample_rate,
			'-t raw' ]

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

if( data[name]['elevation'] < gain_lower_pass_requirement ):
	gain = gain_lower_pass

timeoutstr = 'timeout ' + str(data[name]['duration_seconds'])
filename = datestamp(data[name]['start_unix']) + name + '_' + data[name]['direction'] + str(int(data[name]['elevation']))

if( len(wxtoimg_options) == 0 ):

	rtlpower = 'rtl_power -f 137M:138M:4k -g ' + gain + ' -i 1s -e ' + str(data[name]['duration_seconds']) + 's -p ' + ppmshift + ' -c 0.2 ' + output_folder + filename + '.csv'
	heatmap = 'python heatmap.py ' + output_folder + name + '_' + data[name]['direction'] + str(int(data[name]['elevation'])) + '_' + timestamp + '.csv ' + output_folder + name + '_' + data[name]['direction'] + str(int(data[name]['elevation'])) + '_' + timestamp + '.png'

	print timeoutstr, rtlpower
	print heatmap
	print 'bash ftp.sh ' + output_folder + name + '_' + data[name]['direction'] + str(int(data[name]['elevation'])) + '_' + timestamp + '.png'

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
	print 'bash', 'render.sh', af_folder + filename + '.wav', data[name]['start_unix']+60 #+60 is just for wxmap to work properly
		
f = open(name + '_sched.txt', 'w')
f.write(convert_time(data[name]['start_unix']))

#for opt in wxtoimg_options:
#	filename = datestamp(data[name]['start_unix']) + name + '_' + data[name]['direction'] + str(int(data[name]['elevation']))
#
#	print 'wxtoimg -' + data[name]['direction'] + ' -e', opt, af_folder + filename + '.wav', output_folder + filename + '_' + opt + '.png'
#
#	if( data[name]['direction'] == "S" ): #southbound images are upside down
#		print 'convert', output_folder + filename + '_' + opt + '.png', '-rotate 180', output_folder + filename + '_' + opt + '.png'
#
#	print 'bash ftp.sh', output_folder + filename + '_' + opt + '.png'
