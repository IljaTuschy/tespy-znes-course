"""
module for starting with python in thermal engineering
calculate property using coolprop
belongs to 
unit 1: calculation of thermal properties
"""

from CoolProp.CoolProp import PropsSI as prop

p = 1 * 10**5 #Pressure in Pa
t = 20 + 273.15 #Temperature in K

fluid = 'Air'

v = 1/prop('D','P',p ,'T', t, fluid)

print(v)
