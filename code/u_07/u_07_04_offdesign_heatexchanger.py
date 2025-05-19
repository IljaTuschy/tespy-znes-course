'''
script to simulate off-design operation of a 

steam condenser

belongs to 

Unit 07: Design and Off-Design
'''

from tespy.networks import Network
from tespy.connections import Connection
from tespy.components import(
    Source,
    HeatExchanger,
    Sink
)

#create network
condn = Network()

#create components
ex = Source('steam turbine exhaust')
cw = Source('cooling water inlet')
hx = HeatExchanger('steam condenser')
cs = Sink('condendate')
co = Sink('cooling water outlet')

#set up topology
s01 = Connection(ex, 'out1', hx, 'in1', 's01')
s02 = Connection(hx, 'out1', cs, 'in1', 's02')
w01 = Connection(cw, 'out1', hx, 'in2', 'w01')
w02 = Connection(hx, 'out2', co, 'in1', 'w02')

condn.add_conns(s01, s02, w01, w02)


