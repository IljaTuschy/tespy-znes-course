from tespy.networks import Network
from tespy.components import (
    Sink, Source,
    Compressor,
    DiabaticCombustionChamber,
    Turbine
)
from tespy.connections import Connection, Bus

import numpy as np
import pandas as pd

# general configurations
# substances, fluids, network, units
fluid_list = ['N2', 'O2', 'Ar', 'CO2', 'H2O', 'CH4']
gas_turbine = Network(fluids=fluid_list, p_unit='bar', T_unit='C', h_unit='kJ / kg')

# composition of given fluids
air = {'N2': 0.7551, 'O2': 0.2314, 'Ar': 0.0129, 'CO2': 0.0006, 'H2O': 0, 'CH4': 0}
fuel = {'N2': 0, 'O2': 0, 'Ar': 0, 'CO2': 0, 'H2O': 0, 'CH4': 1}

# define sources and sinks
src_air = Source('air')
src_fuel = Source('fuel')
snk_exhaust = Sink('exhaust')

# define components
cmp_AC = Compressor('air compressor')
cmp_CC = DiabaticCombustionChamber('combustion chamber')
cmp_EX = Turbine('expander')

# define connections
c1 = Connection(src_air, 'out1', cmp_AC, 'in1', label='1')
c2 = Connection(cmp_AC, 'out1', cmp_CC, 'in1', label='2')
c3 = Connection(src_fuel, 'out1', cmp_CC, 'in2', label='3')
c4 = Connection(cmp_CC, 'out1', cmp_EX, 'in1', label='4')
c5 = Connection(cmp_EX, 'out1', snk_exhaust, 'in1', label='5')

# add connections to network
gas_turbine.add_conns(c1, c2, c3, c4, c5)

# parameter of components
cmp_AC.set_attr(eta_s=0.85, pr=18)
cmp_CC.set_attr(eta=0.98, pr=0.95)
cmp_EX.set_attr(eta_s=0.9)

# parameter of connections
c1.set_attr(p=1.013, T=25, fluid=air)
c3.set_attr(p=20, T=25, fluid=fuel)
c4.set_attr(T=1400)
c5.set_attr(p=1.013)

# busses
work_net = Bus('work netto')
fuel_in = Bus('fuel input')

work_net.add_comps(
    {'comp': cmp_AC, 'base': 'bus', 'char': 1},
    {'comp': cmp_EX, 'char': 1})

fuel_in.add_comps(
    {'comp': cmp_CC, 'base': 'bus'}
)

gas_turbine.add_busses(work_net, fuel_in)

# parameter of busses
work_net.set_attr(P=-150e6)

# solve network
gas_turbine.solve('design')

# print network results
gas_turbine.print_results()

# save to file
gas_turbine.save('results-design/')

# parameter study: pressure ratio and expander inlet temperature

# create data ranges and frames
pr_range = np.array([5, 10, 15, 20, 25, 30])
it_range = np.array([900.0, 1000.0, 1110.0, 1200.0, 1300.0, 1400.0])
df_eta = pd.DataFrame(columns=pr_range)
df_swk = pd.DataFrame(columns=pr_range)

# update parameter, solve all cases, results to csv data
for j in it_range:
    eta = []
    swk = []

    for i in pr_range:
        # update parameter
        cmp_AC.set_attr(pr=i)
        c3.set_attr(p=1.013*i+1e-9)
        c4.set_attr(T=j)

        # solve case
        gas_turbine.solve(mode='design', init_path='results-design/')

        # calculate efficiency
        eta.append(abs(work_net.P.val)/fuel_in.P.val)
        # calculate specific work
        swk.append(abs(work_net.P.val)*1E-3/c1.m.val)

    # results to csv data
    df_eta.loc[j] = eta
    df_swk.loc[j] = swk
    df_eta.to_csv('data/eta.csv')
    df_swk.to_csv('data/swk.csv')
