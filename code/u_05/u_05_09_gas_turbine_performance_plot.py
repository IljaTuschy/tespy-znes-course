'''
calculation and plotting of 
gas turbine performance for
different turbine inlet temperatures
and compressor pressure ratios
belongs to 
unit 5: Cycles I (gas turbines)
'''

from tespy.networks import Network
from tespy.connections import Connection
from tespy.components import(
    Source,
    Compressor,
    DiabaticCombustionChamber,
    Turbine,
    Sink    
)
import numpy as np
import matplotlib.pyplot as plt

#create network
gt = Network()

#create components w/o parameters
amb = Source('ambient')
tank = Source('fuel tank')
comp = Compressor('compressor')
cc = DiabaticCombustionChamber('combustion chamber')
turb = Turbine('turbine')
stack = Sink('stack')

#set up topology
ai = Connection(amb, 'out1', comp, 'in1', 'air inlet')
co = Connection(comp, 'out1', cc, 'in1', 'compressor outlet')
cf = Connection(tank, 'out1', cc, 'in2', 'combustion fuel')
ti = Connection(cc, 'out1', turb, 'in1', 'turbine inlet')
ex = Connection(turb, 'out1', stack, 'in1', 'exhaust')

gt.add_conns(ai, co, cf, ti, ex)

#stable parametrization
Pi = 10
TIT = 1273.15
p_amb = 1e5
T_amb = 293.15
air = {'N2': 0.79, 'O2': 0.21}
fuel = {'H2':1}
ai.set_attr(m=100, p=p_amb, T=T_amb, fluid=air)
cf.set_attr(p=p_amb*Pi, T=T_amb, fluid=fuel)
ex.set_attr(p=p_amb)
comp.set_attr(pr=Pi, eta_s=0.9)
cc.set_attr(eta=1, lamb=3, pr=0.95)
turb.set_attr(eta_s=0.9)

#solve stable configuration
gt.solve(mode='design')
gt.print_results()

#prepare new parametrization
cc.set_attr(lamb=None)
ti.set_attr(T=TIT)

gt.solve(mode='design')
gt.print_results()

# prepare parameter matrix and result array
n_TIT = 5
n_Pi = 20
eta = np.empty([n_TIT, n_Pi])
wp = np.empty([n_TIT, n_Pi])

TIT_range = np.linspace(800+273.15, 1200+273.15, n_TIT)
Pi_range = np.linspace(5, 50, n_Pi)

# prepare plot
fig = plt.figure(figsize=[6,6])
ax_eta =fig.add_subplot(211)
ax_wp =fig.add_subplot(212)

# simulate and plot in a loop
i = 0
for TIT_n in TIT_range:
    j = 0
    ti.set_attr(T=TIT_n)
    for Pi_n in Pi_range:
        comp.set_attr(pr=Pi_n)
        cf.set_attr(p=p_amb*Pi_n)
        gt.solve(mode='design')
        eta[i, j]=(abs(turb.get_attr('P').val) - comp.get_attr('P').val) / cc.calc_ti()
        wp[i, j]=(abs(turb.get_attr('P').val) - comp.get_attr('P').val) / ai.get_attr('m').val / 1e3
        j +=1
    ax_eta.plot(Pi_range, eta[i])
    ax_wp.plot(Pi_range, wp[i])
    i +=1

#format plot and show
fig.suptitle('Gas Turbine Performance for different Turbine Inlet Temperatures')
ax_eta.set_ylabel('Efficiency')
ax_wp.set_xlabel('Compressor Presure Ratio')
ax_wp.set_ylabel('Specific Work in kJ/kg')
labels = [f'T = {TIT_n:.0f} K' for TIT_n in TIT_range]
ax_eta.legend(labels, loc='lower left', ncols=2)
ax_eta.grid(True)
ax_wp.grid(True)
ax_eta.sharex(ax_wp)
ax_eta.tick_params(labelbottom=False)
plt.show()

#save figure
plt.savefig('docs/img/gt_performance.png')
