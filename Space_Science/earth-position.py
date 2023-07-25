import spiceypy #SPICE toolkit offered in Python (Derived from CSPICE)
import datetime 
import math

date_today = datetime.datetime.today()
print(date_today)

date_today = date_today.strftime("%Y-%m-%dT00:00:00") #A different string representation of the date
print(date_today)

"""
SPICE stores data in files that are often referred to as kernels.
A kernel may store data in either text (ASCII) or binary format. 
In order to access data within a kernel an application program must "load" the kernel using a SPICE API ("furnsh").
"""

#Loading the kernels
spiceypy.furnsh("kernels/lsk/naif0012.tls") #Leap seconds kernel (lsk)
spiceypy.furnsh("kernels/spk/de432s.bsp") #SP kernel

#SPICE requires converting from UTC (Coordinated Universal Time) to Ephemeris Time
et_today_midnight = spiceypy.utc2et(date_today)
print(et_today_midnight) #Print out the Ephemeris Time

#spk is the kernel used for computing positions of spacecraft and natural bodies
earth_state_wrt_sun, earth_sun_light_time = spiceypy.spkgeo(targ=399, #Integer ID code of the center of Earth
                                                            et=et_today_midnight, #Ephemeris TIme
                                                            ref="ECLIPJ2000", #Reference frame based on the ecliptic plane
                                                            obs=10) #Integer ID code of the observer, in this case the sun


#earth_state_wrt_sun is a state vector containing the position and velocity information of the earth (length of 6 numbers)
#earth_sun_light_time is the light time in seconds that light gets to earth from the observer (sun)
print(earth_state_wrt_sun)
print(earth_sun_light_time)

#Calculate distance from sun to earth (in km)
earth_sun_distance = math.sqrt(earth_state_wrt_sun[0] ** 2
                               + earth_state_wrt_sun[1] ** 2
                               + earth_state_wrt_sun[2] ** 2)
print(earth_sun_distance)

#Convert km to AU
earth_sun_distance_au = spiceypy.convrt(earth_sun_distance, "km", "au")
print(earth_sun_distance_au)