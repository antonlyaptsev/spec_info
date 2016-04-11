from math import sin, cos, tan, atan, asin, radians, degrees

jd = 2457224.348273						#current julian date
obj_alpha = 17 + 13/60.0 + 23/3600.0
obj_delta = 33 + 31/60.0 + 01/3600.0
c = 299792458							#speed of light(meters per square second)

n = jd - 2451545.0						#num of days after J2000.0
l = (280.460 + 0.9856474*n) % 360 		#mean longitude of Sun (corrected for the abberation of light)
g = (357.528 + 0.9856003*n) % 360 		#mean anomaly of the Sun

e = 23.439 - 0.0000004*n 				#obliquity of ecliptic

#distance of the Sun from the Earth (in au)
r_au = 1.00014 - 0.01671*cos(radians(g)) - 0.00014*cos(radians(2*g))
#distance in meters
r_m = r_au * 149597870700						

#ecliptic latitude of the Sun
sun_lambda = l + 1.915*sin(radians(g)) + 0.020*sin(radians(2*g))

#ecliptic latitude of the sun_beta
sun_beta = 0.0


#Sun alpha in degrees
if (sun_lambda < 90 and sun_lambda > 0): 
	sun_alpha_deg = degrees(atan(cos(radians(e)) * tan(radians(sun_lambda))))
elif (sun_lambda > 90 and sun_lambda < 270):
	sun_alpha_deg = 180 + degrees(atan(cos(radians(e)) * tan(radians(sun_lambda))))
elif (sun_lambda > 270 and sun_lambda < 360):
	sun_alpha_deg = 360 + degrees(atan(cos(radians(e)) * tan(radians(sun_lambda))))

#Sun alpha in hours
sun_alpha = (24*(sun_alpha_deg))/360

#Sun delta
sun_delta = degrees(asin(sin(radians(e)) * sin(radians(sun_lambda))))

#Object alpha in degrees
obj_alpha_deg = (obj_alpha*360)/24

#Heliocentric Julian Date
hjd = jd - ((r_m/c) * (sin(radians(obj_delta))*sin(radians(sun_delta)) + 
	cos(radians(obj_delta))*cos(radians(sun_delta))*
	cos(radians(obj_alpha_deg - sun_alpha_deg))))/(24*3600)

print("Sun_alpha(in hours) = " + str(sun_alpha))
print("Sun_alpha(in deg) = " + str(sun_alpha_deg))
print("HJD = " + str(hjd))
print("HJD - JD = " + str(hjd-jd))
print("HJD - JD (in minutes) = " + str((hjd-jd)*24*60))

