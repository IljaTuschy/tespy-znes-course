# use CoolProp
from CoolProp.CoolProp import PropsSI as props

# fluid information
fluid = 'air'

# inlet conditions
m_1 = 10 # mass flow in kg/s
p_1 = 1 * 10**5 # inlet pressure in Pa
t_1 = 293.15 #inlet temperature in K

# compressor data
eta_c = 0.9 # compressor isentropic efficiency

# outlet conditions
t_2_target = 573.15 # target compressor outlet tempertature in K


# calculate missing properties
h_1 = props('H', 'P', p_1, 'T', t_1, fluid)
s_1 = props('S', 'P', p_1, 'H', h_1, fluid)

# calculate outlet temperature
def calc_t_out_pr(pr, eta, p_in, h_in, medium):
    '''
    function for calculating outlet temperatures
    as a function of pressure ratio
    '''
    s_in = props('S', 'P', p_in, 'H', h_in, medium)
    h_out_s = props('H', 'P', p_in*pr, 'S', s_in, medium)
    h_out = h_in + (h_out_s - h_in) / eta
    t_out = props('T', 'P', p_in*pr, 'H', h_out, medium)
    return t_out

# guess for the pressure ratio
pr_guess = 4
d = 1e-2  # Delta for change of variable pr

while True:

    residual = calc_t_out_pr(pr_guess, eta_c, p_1, h_1, fluid) - t_2_target
    derivative = (
        calc_t_out_pr(pr_guess + d, eta_c, p_1, h_1, fluid)
         - calc_t_out_pr(pr_guess - d, eta_c, p_1, h_1, fluid)
    ) / (2 * d)

    increment = residual / derivative
    pr_guess -= increment

    # stop the simulation once the difference between the target temperature
    # and the actual temperature is small enough
    if abs(residual) < 1e-6:
        break

pr_guess