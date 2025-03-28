from tespy.networks import Network
from tespy.components import (
    Sink, Source,
    DiabaticCombustionChamber,
)
from tespy.connections import Connection

fluid_list = ['N2', 'O2', 'Ar', 'CO2', 'H2O', 'CH4']
gas_turbine = Network(fluids=fluid_list, p_unit='bar', T_unit='C')

air = {'N2': 0.7551, 'O2': 0.2314, 'Ar': 0.0129, 'CO2': 0.0006, 'H2O': 0, 'CH4': 0}
fuel = {'N2': 0, 'O2': 0, 'Ar': 0, 'CO2': 0, 'H2O': 0, 'CH4': 1}

src_air = Source('air')
src_fuel = Source('fuel')
snk_exhaust = Sink('exhaust')

cmp_CC = DiabaticCombustionChamber('combustion chamber')

c1 = Connection(src_air, 'out1', cmp_CC, 'in1', label='1')
c2 = Connection(src_fuel, 'out1', cmp_CC, 'in2', label='2')
c3 = Connection(cmp_CC, 'out1', snk_exhaust, 'in1', label='3')

gas_turbine.add_conns(c1, c2, c3)

cmp_CC.set_attr(eta=0.98, pr=0.95)

c1.set_attr(p=1.013, T=25, fluid=air)
c2.set_attr(p=1.013, T=25, fluid=fuel, m=1)
c3.set_attr(T=1000)

gas_turbine.solve('design')

gas_turbine.print_results()
