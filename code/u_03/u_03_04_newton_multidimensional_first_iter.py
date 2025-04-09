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


def temperature_residual(T, p, h, fluid):
    return props("T", "P", p, "H", h, fluid) - T


def duty_residual(W_dot, m, h_in, h_out):
    return W_dot - m * (h_out - h_in)


def pr_residual(pr, p_in, p_out):
    return p_in * pr - p_out


def eta_s_residual(eta_s, p_in, h_in, p_out, h_out, fluid):
    s_in = props("S", "H", h_in, "P", p_in, fluid)
    h_out_s = props("H", "S", s_in, "P", p_out, fluid)
    return eta_s * (h_out - h_in) - (h_out_s - h_in)


def variable_specified_residual(specification, var):
    return specification - var


def variable_equality_residual(var_1, var_2):
    return var_1 - var_2


import numpy as np

x = np.array([
    5, 1e5, 3e5, 5, 9e5, 7e5
])

residual = np.array([
    variable_specified_residual(m_1, x[0]),
    variable_specified_residual(p_1, x[1]),
    variable_equality_residual(x[0], x[3]),
    temperature_residual(t_1, x[1], x[2], fluid),
    temperature_residual(t_2_target, x[4], x[5], fluid),
    eta_s_residual(eta_c, x[1], x[2], x[4], x[5], fluid)
])

jacobian = np.zeros((6, 6))

jacobian[0, 0] = -1
jacobian[1, 1] = -1
jacobian[2, [0, 3]] = [1, -1]


def temperature_jacobian(p, h, fluid):
    d = 1e-1
    return [
        (props("T", "P", p + d, "H", h, fluid) - props("T", "P", p - d, "H", h, fluid)) / (2 * d),
        (props("T", "P", p, "H", h + d, fluid) - props("T", "P", p, "H", h - d, fluid)) / (2 * d)
    ]


def eta_s_jacobian(eta_s, p_in, h_in, p_out, h_out, fluid):
    d = 1e-1
    return [
        (eta_s_residual(eta_s, p_in + d, h_in, p_out, h_out, fluid)
        - eta_s_residual(eta_s, p_in - d, h_in, p_out, h_out, fluid))
        / (2 * d),
        (eta_s_residual(eta_s, p_in, h_in + d, p_out, h_out, fluid)
        - eta_s_residual(eta_s, p_in, h_in - d, p_out, h_out, fluid))
        / (2 * d),
        (eta_s_residual(eta_s, p_in, h_in, p_out + d, h_out, fluid)
        - eta_s_residual(eta_s, p_in, h_in, p_out - d, h_out, fluid))
        / (2 * d),
        eta_s
    ]


jacobian[3, [1, 2]] = temperature_jacobian(x[1], x[2], fluid)
jacobian[4, [4, 5]] = temperature_jacobian(x[4], x[5], fluid)
jacobian[5, [1, 2, 4, 5]] = eta_s_jacobian(eta_c, x[1], x[2], x[4], x[5], fluid)

increment = np.linalg.inv(jacobian).dot(residual)
x -= increment
print(x)
