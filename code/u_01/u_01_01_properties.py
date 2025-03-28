"""
module for starting with python in thermal engineering
a simple and straighht foreward calculation of an example property
belongs to 
unit 1: calculation of thermal properties
"""
p = 1 * 10**5 #pressure in Pa
t = 20 + 273.15 # temperature in K
r = 287 #gas constant in J/(kgK)

v =  r * t / p #specific volume in m^3/kg
print(v)
