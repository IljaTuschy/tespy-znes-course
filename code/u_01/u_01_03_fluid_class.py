'''
module for starting with python in thermal engineering
a simple class to handle a fluid implemented for thermal properties of ideal gases
belongs to 
unit 1: calculation of thermal properties 
'''

class ThermalState():
    '''
    class for holding thermal properties of a fluid which are
    p: pressure in Pa
    t: temperature in K
    v: specific volume in m^3/kg
    '''
    def __init__(self, p=99., t=99., v=99.):
        self.p = p
        self.t = t
        self.v = v

class IdealGas():
    '''
    class to handle an ideal gas with its thermal properties
    state: object of class type ThemalState, containing the thermal properties
    r_i: individual gas constant in J/(kgK)
    '''
    def __init__(self, r_i=99.):
        self.state = ThermalState()
        self.r_i = r_i
        
    def set_pt(self, p, t):
        '''
        method to set and calculate the thermal properties based on
        p: pressure in Pa
        t: temperature in K

        v: specific volume in m^3/kg 
        is automatically calculated using method
        calc_v_pt() 
        '''
        self.state.p = p
        self.state.t = t
        self.calc_v_pt(p, t)

    def calc_v_pt(self, p, t):
        '''
        method to calculate specific volume  of ideal gas in m^3/kg using
        p: pressure in Pa
        t: temperature in K
        and the ideal gas objects attribute 
        r: gas constant in J/(kgK)
        '''
        self.state.p = p
        self.state.t = t
        self.state.v = self.r_i * self.state.t / self.state.p
        return self.state.v

air = IdealGas(287.)
air.set_pt(10**5, 293.15)
print(air.state.v)
