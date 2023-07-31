import spiceypy #SPICE toolkit offered in Python (Derived from CSPICE)
import datetime 
import math
import numpy as np

date_today = datetime.datetime.today()
print("Time:", date_today)

date_today = date_today.strftime("%Y-%m-%dT00:00:00") #A different string representation of the date
print("UTC: " + date_today)

"""
SPICE stores data in files that are often referred to as kernels.
A kernel may store data in either text (ASCII) or binary format. 
In order to access data within a kernel an application program must "load" the kernel using a SPICE API ("furnsh").
"""

#Loading the kernels
spiceypy.furnsh("kernels/lsk/naif0012.tls") #Leap seconds kernel (lsk)
spiceypy.furnsh("kernels/spk/de432s.bsp") #SP kernel (This file records Earth's position over the last 100 years)
spiceypy.furnsh("kernels/pck/gm_de431.tpc") #Physical constants kernel

#SPICE requires converting from UTC (Coordinated Universal Time) to Ephemeris Time
et_today_midnight = spiceypy.utc2et(date_today)
print("Ephemeris Time", et_today_midnight) #Print out the Ephemeris Time

#spk is the kernel used for computing positions of spacecraft and natural bodies
earth_state_wrt_sun, earth_sun_light_time = spiceypy.spkgeo(targ=399, #Integer ID code of the center of Earth
                                                            et=et_today_midnight, #Ephemeris TIme
                                                            ref="ECLIPJ2000", #Reference frame based on the ecliptic plane
                                                            obs=10) #Integer ID code of the observer, in this case the sun


"""
earth_state_wrt_sun is a 6D state vector containing 
the position and velocity information of the earth 

earth_sun_light_time is the time in seconds 
that light gets to earth from the sun
"""
print("Position and velocity vectors of the Earth:", earth_state_wrt_sun)
print("The time it takes light to reach Earth from the sun:", earth_sun_light_time)

#Calculate distance from sun to earth (in km)
earth_sun_distance = math.sqrt(earth_state_wrt_sun[0] ** 2
                               + earth_state_wrt_sun[1] ** 2
                               + earth_state_wrt_sun[2] ** 2)
print("Current distance of Earth to sun in km:", earth_sun_distance)

#Convert km to AU
earth_sun_distance_au = spiceypy.convrt(earth_sun_distance, "km", "au")
print("Current distance of Earth to sun in AU:", earth_sun_distance_au)

earth_state_wrt_sun = np.array(earth_state_wrt_sun)
earth_orbit_vel_wrt_sun = np.linalg.norm(earth_state_wrt_sun[3:]) #Calculate the norm of the velocity vector

print("Earth's orbital velocity in km/s:", earth_orbit_vel_wrt_sun) #Print out the velocity of the Earth w.r.t. the sun

"""
bodvcd extracts 2 values from SPICE (let's igore the first one)

The second paramter is the gravitational constant G * the mass of the sun
bodyid = 10 is the sun's integer ID
item = GM is G * sun mass
maxn = 1 means the value has 1 dimension
"""
_, GM_SUN = spiceypy.bodvcd(bodyid=10, item="GM", maxn=1)

#Computing the theoretical function of the velocity
v_orb_func = lambda gm, r: math.sqrt(gm/r)
earth_orb_speed_wrt_sun_theory = v_orb_func(GM_SUN[0], earth_sun_distance)
print("Theoretical velocity in km/s:", earth_orb_speed_wrt_sun_theory)

#Taking the Earth's position vector and normalizing it
earth_position_wrt_sun_normed = earth_state_wrt_sun[:3] / earth_sun_distance

"""
Let's calculate the angle of change from Autumn to now.

If we treat the position vector of Earth at the Autumnal equinox 
as the "starting point" then our vector is (1, 0, 0)

We can calculate the angle by taking the arccos 
of the dot product of the two vectors divided by their norms
(which is why we normalized the vectors)
"""
earth_position_wrt_sun_normed_autumn = np.array([1.0, 0.0, 0.0])
ang_dist_deg = np.degrees(np.arccos(np.dot(earth_position_wrt_sun_normed, earth_position_wrt_sun_normed_autumn)))

print("Angular distance in degrees:", 360 - ang_dist_deg)