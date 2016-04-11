import os
import fitsio
import time
import datetime
from math import sin, cos, tan, atan, asin, radians, degrees

def main():
	spec_names = os.listdir()
	spec_names.sort()
	file_list = open('list.txt', 'w')
	for file in spec_names:
		if file.endswith('.fit'):
			current = fitsio.read_header(file)
			imagetyp = current['IMAGETYP']
			date = current['DATE']
			exp = current['EXPTIME']
			if imagetyp == 'zero':
				file_list.write(file + '\t' + imagetyp + '\t' + date + '\n')
				continue			
			time = current['UT']
			ra = current['RA']
			dec = current['DEC']
			jd = current['JDMID']
			middle = middleTime(time, exp)
			hjd = heliocentricJD(jd, ra, dec)
			file_list.write(file + '\t' + imagetyp + '\t' + date + '\t' + '\t'
				+ time + '\t' + str(exp) + '\t' + middle 
				+ '  ' + str(hjd) + '\n')
	file_list.close()

def toSeconds(time):
	inseconds = float(time[6:]) + float(time[3:5])*60 + float(time[:2])*3600
	return inseconds

def toString(seconds):
	hour = int(seconds//3600.0)
	minute = int((seconds/3600 - hour)*60)
	second = round(((seconds/3600 - hour)*60 - minute)*60, 2)
	hf = '0' + str(hour) if len(str(hour)) == 1 else str(hour)
	mf = '0' + str(minute) if len(str(minute)) == 1 else str(minute)
	sf = '0' + str(second) if len(str(int(second))) == 1 else str(second)
	time = hf + ':' + mf + ':' + sf
	return time

def middleTime(time, exp):
	middle_seconds = toSeconds(time) + (float(exp)/2)
	middle_time = toString(middle_seconds)
	return middle_time

def heliocentricJD(jd, ra, dec):
	obj_alpha = parseCoord(ra)
	obj_delta = parseCoord(dec)
	obj_alpha_deg = (obj_alpha*360)/24
	c = 299792458
	n = float(jd) - 2451545.0
	l = (280.460 + 0.9856474*n) % 360
	g = (357.528 + 0.9856003*n) % 360
	e = 23.439 - 0.0000004*n
	r = (1.00014 - 0.01671*cos(radians(g)) - 0.00014*cos(radians(2*g)))*149597870700
	sun_lambda = l + 1.915*sin(radians(g)) + 0.020*sin(radians(2*g))
	sun_beta = 0.0
	if (sun_lambda < 90 and sun_lambda > 0): 
		sun_alpha_deg = degrees(atan(cos(radians(e)) * tan(radians(sun_lambda))))
	elif (sun_lambda > 90 and sun_lambda < 270):
		sun_alpha_deg = 180 + degrees(atan(cos(radians(e)) * tan(radians(sun_lambda))))
	elif (sun_lambda > 270 and sun_lambda < 360):
		sun_alpha_deg = 360 + degrees(atan(cos(radians(e)) * tan(radians(sun_lambda))))
	sun_delta = degrees(asin(sin(radians(e)) * sin(radians(sun_lambda))))
	hjd = jd - ((r/c) * (sin(radians(obj_delta))*sin(radians(sun_delta)) + 
		cos(radians(obj_delta))*cos(radians(sun_delta))*
		cos(radians(obj_alpha_deg - sun_alpha_deg))))/(24*3600)
	return hjd

def parseCoord(coord):
	if (coord[0] == '+' or coord[0] == '-'):
		result = float(coord[1:3]) + float(coord[4:6])/60 + float(coord[7:])/3600
		if coord[0] == '-':
			result = result*(-1)
	else:
		result = float(coord[:2]) + float(coord[3:5])/60 + float(coord[6:])/3600
	return result

if  __name__ ==  "__main__" :
    main()
