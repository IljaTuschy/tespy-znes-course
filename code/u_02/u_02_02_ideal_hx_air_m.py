'''
simple heat exchanger calculation for
single sided HX to heat up air as an ideal gas
straight forward calculation of mass flow for 
given in- and outlet state and given duty
belongs to 
unit 2: single components
'''
# ideal gas parameters
c_p = 1100 # specific heat of air in J/(kgK)

# inlet conditions
t_1 = 293.15 # temperature in K

# outlet conditions
t_2 = 393.15 # temperature in K

q = 1000000 # heat exchanger duty in W

# calculate mass flow in kg/s 
m = q / (c_p * (t_2 - t_1))

print(m)
