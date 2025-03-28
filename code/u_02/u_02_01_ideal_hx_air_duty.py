'''
simple heat exchanger calculation for
single sided HX to heat up air as an ideal gas
straight forward calculation of duty for 
given in- and outlet conditions
belongs to 
unit 2: single components
'''
# ideal gas parameters
c_p = 1100 # specific heat of air in J/(kgK)

# inlet conditions
m_1 = 10 # mass flow in kg/s
t_1 = 293.15 # temperature in K

# outlet conditions
t_2 = 393.15 # temperature in K

# calculate heat exchanger duty in W
q = m_1 * c_p * (t_2 - t_1)

print(q)
