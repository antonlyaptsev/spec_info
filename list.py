import os
import fitsio
import time
import datetime

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
				print(file + '\t' + imagetyp + '\t' + date)
				file_list.write(file + '\t' + imagetyp + '\t' + date + '\n')
				continue			
			time = current['UT']
			middle = middleTime(time, exp)
			print(file + '\t' + imagetyp + '\t' + date + '\t' + time + '\t' + str(exp) + '\t' + middle)
			file_list.write(file + '\t' + imagetyp + '\t' + date + '\t' + time + '\t' + str(exp) + '\t' + middle + '\n')
	file_list.close()

def toSeconds(time):
	hour = time[:2]
	minute = time[3:5]
	second = time[6:]
	inseconds = float(second) + float(minute)*60 + float(hour)*3600
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

if  __name__ ==  "__main__" :
    main()
