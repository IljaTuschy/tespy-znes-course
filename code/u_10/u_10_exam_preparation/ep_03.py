'''
script to calculate the performance of a
closed cycle gas turbine 
based on known 
component performance data

Modify and use the model to determine the
compressor pressure ratio for optimum efficiency
at given maximum temperature
HINT: the optimum ration is within the range [1.5 ... 5.5]
'''

from tespy.networks import Network
from tespy.connections import Connection
from tespy.components import(
    Compressor,
    HeatExchanger,
    SimpleHeatExchanger,
    Turbine,
    CycleCloser
)

# create network and set unit system
rccgt = Network(p_unit='bar', T_unit='C')

# create components without parametrization
comp = Compressor('compressor')
heat = SimpleHeatExchanger('heater')
recu = HeatExchanger('recuperator')
turb = Turbine('turbine')
cool = SimpleHeatExchanger('cooler')
cc = CycleCloser('cycle closer')

# define topology:
# c1: compressor inlet
# c2: compressor outlet
# c3: preheated fluid
# c4: turbine inlet
# c5: turbine outlet
# c6: cooler inlet
# c7: cooler outlet
c1 = Connection(cc, 'out1', comp, 'in1', 'c1')
c2 = Connection(comp, 'out1', recu, 'in2', 'c2')
c3 = Connection(recu, 'out2', heat, 'in1', 'c3')
c4 = Connection(heat, 'out1', turb, 'in1', 'c4')
c5 = Connection(turb, 'out1', recu, 'in1', 'c5')
c6 = Connection(recu, 'out1', cool, 'in1', 'c6')
c7 = Connection(cool, 'out1', cc, 'in1', 'c7')

rccgt.add_conns(c1, c2, c3, c4, c5, c6, c7)

# parametrize
# component efficiencies
comp.set_attr(eta_s=0.9)
heat.set_attr(pr=0.95)
turb.set_attr(eta_s=0.9)
cool.set_attr(pr=0.95)
recu.set_attr(pr1=0.95, pr2=0.95, ttd_u=10)

# conditions:
# compressor inlet conditions
# turbine inlet pressure and temperature
c1.set_attr(fluid={'He':1}, m=10, p=5, T=30)
c4.set_attr(p=20, T=850)

# simulate and print results
rccgt.solve(mode='design')
rccgt.print_results()
