from tespy.networks import Network
from tespy.components import (
    Sink, Source,
    Compressor,
    DiabaticCombustionChamber,
    Turbine
)
from tespy.connections import Connection

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
cmp_AC.set_attr(eta_s=0.85)
cmp_CC.set_attr(eta=0.98, pr=0.95)
cmp_EX.set_attr(eta_s=0.9)

# parameter of connections
c1.set_attr(p=1.013, T=25, fluid=air)
c2.set_attr(p=10.13)
c3.set_attr(p=20, T=25, fluid=fuel, m=1)
c4.set_attr(T=1000)
c5.set_attr(p=1.013)

# solve network
gas_turbine.solve('design')

# print network results
gas_turbine.print_results()
