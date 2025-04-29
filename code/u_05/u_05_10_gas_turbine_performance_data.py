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
import pandas as pd

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
n_TIT = 2
n_Pi = 5
eta = np.empty([n_TIT, n_Pi])
wp = np.empty([n_TIT, n_Pi])

TIT_range = np.linspace(800+273.15, 1200+273.15, n_TIT)
Pi_range = np.linspace(5, 50, n_Pi)

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
    i +=1

#bring data into pandas dataframe and save
df_eta = pd.DataFrame(columns=Pi_range, index=TIT_range, data=eta)
df_wp = pd.DataFrame(columns=Pi_range, index=TIT_range, data=wp)
df_eta.to_csv('code/u_05/data/eta.csv')
df_wp.to_csv('code/u_05/data/wp.csv')

#read and plot from saved data
#read data from files
eta_df = pd.read_csv('code/u_05/data/eta.csv', index_col=0)
wp_df =pd.read_csv('code/u_05/data/wp.csv', index_col=0)
data_eta = eta_df.to_numpy()
data_wp =wp_df.to_numpy()
ratios = eta_df.columns.to_numpy(dtype=float)
TITs = eta_df.index.to_numpy()

# prepare plot
fig = plt.figure()
ax_eta =fig.add_subplot(211)
ax_wp =fig.add_subplot(212)
# plot in a loop
i = 0
for TIT_n in TITs:
    ax_eta.plot(ratios, data_eta[i])
    ax_wp.plot(ratios, data_wp[i])
    i +=1

ax_eta.set_title('Gas Turbine Performance for different Turbine Inlet Temperatures')
ax_eta.set_ylabel('Efficiency')
ax_wp.set_xlabel('Compressor Presure Ratio')
ax_wp.set_ylabel('Specific Work in kJ/kg')
labels = [f'T = {TIT_n} K' for TIT_n in TITs]
ax_eta.legend(labels, loc='lower left', ncols=2)
ax_eta.grid(True)
ax_wp.grid(True)
ax_eta.sharex(ax_wp)
ax_eta.tick_params(labelbottom=False)
plt.show()
