"""
module for starting with python in thermal engineering
calculate property using a very simple self defined function
belongs to 
unit 1: calculation of thermal properties
"""
def calc_v(p, t, r):
    """
    function to calculate specific volume of ideal gas in m^3/kg using
    p: pressure in Pa
    t: temperature in K
    r: gas constant in J/(kgK)
    """
    return r * t / p


p_out = 1 * 10**5 #pressure in Pa
t_out = 20 + 273.15 # temperature in K
r_out = 287.15 #gas constant in J/(kgK)

print(calc_v(p_out, t_out, r_out))
