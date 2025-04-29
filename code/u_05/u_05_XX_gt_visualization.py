"""
Module for visualizing the influence of pressure ratio and maximum 
temperature on gas turbine performance 
"""

from dataclasses import dataclass
from tkinter import Tk, Scale, Checkbutton, BooleanVar
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.gridspec import GridSpec
import numpy as np

@dataclass
class State:
    """
    Dataclass for holding thermodynamic state variables
    """
    p: float
    t: float
    v: float
    h: float
    s: float


class PerfectGas():
    """
    Class for holding and calculating thermodynamic state variables of 
    perfect gases
    """

    def __init__(self, r_i=287., c_p=1050., s_0=6848.) -> None:
        self.r_i = r_i
        self.c_p = c_p
        self.ref_state = State((10**5), (273.15 + 20), 0, 0, s_0)
        self.state = State(self.ref_state.p,
                           self.ref_state.t,
                           self.calc_v_pt,
                           self.ref_state.h,
                           self.ref_state.s)
        self.calc_pt()

    def calc_v_pt(self):
        """
        calculate v in m^3/kg from p in Pa and t in K
        """
        self.state.v = self.r_i * self.state.t / self.state.p
        return self.state.v

    def calc_h_pt(self):
        """
        calculate h in J/kgK from p in Pa and t in K
        """
        self.state.h = self.ref_state.h + \
            self.c_p*(self.state.t-self.ref_state.t)
        return self.state.h

    def calc_s_pt(self):
        """
        calculate s in J/(kgK) from p in Pa and t in K
        """
        self.state.s = self.ref_state.s + self.c_p * \
            np.log((self.state.t)/(self.ref_state.t)) - \
            self.r_i*np.log(self.state.p/self.ref_state.p)
        return self.state.s

    def calc_pt(self):
        """
        calculate state from p in Pa and t in K
        """
        self.calc_v_pt()
        self.calc_h_pt()
        self.calc_s_pt()

    def set_pt(self, p, t):
        """
        set p in Pa and T in K and calculate v, h, s 
        """
        self.state.p = p
        self.state.t = t
        self.calc_pt()

    def set_pv(self, p, v):
        """
        set p in Pa and T in K and calculate v, h, s 
        """
        self.state.p = p
        self.state.t = p * v / self.r_i
        self.calc_pt()


@dataclass
class GTSimpleDesignData:
    """
    class for holding design data of a simple gas turbine
    """
    pi: float
    t_max: float
    eta_c: float
    eta_t: float
    dp_rel: float
    massflow: float


class GTSimple():
    """
    Simple Gas Turbine
    """

    def __init__(self, pi_init=10, t_max_init=1273.15, m_init=100):
        self.flows = [
            PerfectGas(),
            PerfectGas(),
            PerfectGas(),
            PerfectGas()
        ]
        self.designdata = GTSimpleDesignData(
            pi=pi_init,
            t_max=t_max_init,
            eta_c=0.9,
            eta_t=0.9,
            dp_rel=0.05,
            massflow=m_init
        )
        self.eta_th = 0.0
        self.w_cycle = 0.0

    def calc_gt(self):
        """
        calulate all process state variables and basic cycle performance data
        """
        c_in = self.flows[0].state
        c_out = self.flows[1].state
        t_in = self.flows[2].state
        t_out = self.flows[3].state
        d = self.designdata
        c_out.p = c_in.p * d.pi
        expo = self.flows[0].r_i / self.flows[0].c_p
        c_out.t = c_in.t * (1 + ((c_out.p/c_in.p)**(expo)-1)/d.eta_c)
        t_in.p = c_out.p * (1-d.dp_rel)
        t_in.t = d.t_max
        t_out.t = t_in.t * (1 + ((t_out.p/t_in.p)**(expo)-1)*d.eta_t)

        self.flows[0].set_pt(c_in.p, c_in.t)
        self.flows[1].set_pt(c_out.p, c_out.t)
        self.flows[2].set_pt(t_in.p, t_in.t)
        self.flows[3].set_pt(t_out.p, t_out.t)

        self.eta_th = ((t_in.t-t_out.t) - (c_out.t-c_in.t)) / (t_in.t-c_out.t)
        self.w_cycle = (t_in.h-t_out.h) - (c_out.h-c_in.h)

    def opt_eta(self):
        """
        find optimum pressure ratio pi with respect to cycle efficiency 
        """
        # lower and upper bound of search area
        pi_less = 1
        pi_more = (self.designdata.t_max /
                   self.flows[0].state.t)**(self.flows[0].c_p/self.flows[0].r_i)
        # long runtime but shortly told:
        # define fulcum
        eta_explore = np.zeros(5)
        eta_delta = np.zeros(4)
        # look for optimum in search area until less than 10^-4 relative difference in width
        while ((pi_more-pi_less)/pi_less) > 10**(-4):
            pi_explore = np.linspace(pi_less, pi_more, num=5)
            counter = 0
            for pi_test in pi_explore:
                self.designdata.pi = pi_test
                self.calc_gt()
                eta_explore[counter] = self.eta_th
                counter = counter + 1
            for counter in range(4):
                eta_delta[counter] = (
                    eta_explore[counter+1]-eta_explore[counter])
            if (eta_delta[0] * eta_delta[1]) < 0:
                pi_less = pi_explore[0]
                pi_more = pi_explore[2]
            elif (eta_delta[1] * eta_delta[2]) < 0:
                pi_less = pi_explore[1]
                pi_more = pi_explore[3]
            else:
                pi_less = pi_explore[2]
                pi_more = pi_explore[4]
        self.designdata.pi = (pi_less + pi_more) / 2
        self.calc_gt()

    def opt_w_cycle(self):
        """
        find optimum pressure ration with respect to cycle output
        """
        # lower and upper bound of search area
        pi_less = 1
        pi_more = (self.designdata.t_max /
                   self.flows[0].state.t)**(self.flows[0].c_p/self.flows[0].r_i)
        # long runtime but shortly told:
        # define fulcum
        w_explore = np.zeros(5)
        w_delta = np.zeros(4)
        # look for optimum in search area until less than 10^-4 relative difference in width
        while ((pi_more-pi_less)/pi_less) > 10**(-4):
            pi_explore = np.linspace(pi_less, pi_more, num=5)
            counter = 0
            for pi_test in pi_explore:
                self.designdata.pi = pi_test
                self.calc_gt()
                w_explore[counter] = self.w_cycle
                counter = counter + 1
            for counter in range(4):
                w_delta[counter] = w_explore[counter+1]-w_explore[counter]
            if (w_delta[0] * w_delta[1]) < 0:
                pi_less = pi_explore[0]
                pi_more = pi_explore[2]
            elif (w_delta[1] * w_delta[2]) < 0:
                pi_less = pi_explore[1]
                pi_more = pi_explore[3]
            else:
                pi_less = pi_explore[2]
                pi_more = pi_explore[4]
        self.designdata.pi = (pi_less + pi_more) / 2
        self.calc_gt()

    def get_temperatures(self):
        """
        return all process temperatures as numpy array 
        """
        return np.array([
            self.flows[0].state.t,
            self.flows[1].state.t,
            self.flows[2].state.t,
            self.flows[3].state.t,
        ])

    def get_pressures(self):
        """
        return all process temperatures as numpy array 
        """
        return np.array([
            self.flows[0].state.p,
            self.flows[1].state.p,
            self.flows[2].state.p,
            self.flows[3].state.p,
        ])


    def get_volumes(self):
        """
        return all process temperatures as numpy array 
        """
        return np.array([
            self.flows[0].state.v,
            self.flows[1].state.v,
            self.flows[2].state.v,
            self.flows[3].state.v,
        ])

    def get_entropies(self):
        """
        return all process entropies as numpy array 
        """
        return np.array([
            self.flows[0].state.s,
            self.flows[1].state.s,
            self.flows[2].state.s,
            self.flows[3].state.s,
        ])


# Slider ranges
T_MIN = 600       # min temperature in °C
T_MAX = 1200
PI_MIN = 5       # min pressure ratio
PI_MAX = 50

# plotting axex limits
S_LOW = 6.8
S_HIGH = 8.3
ETA_LOW = 0
ETA_HIGH = 70
W_LOW = 0
W_HIGH = 350


# All these values are given by default in GT and State classes
# C_P = 1050		# specific isobaric heat in J/(kgK)
# R_I = 287		# individual gas constant in J/(kgK)
# T_U = 20		# ambient temperature in °C
# P_U = 1			# ambient pressure in bar
# S_U = 6848		# ambient specific entropy in J/(kgK)

# ETA_SC = 0.9  # isentropic efficiency compressor
# ETA_ST = 0.9  # isemtropic efficiency turbine
# DP_REL = 0.05  # relative pressure loss heat supply

def update_ts():
    """
    plot optimized cycles in t,s diagram or not
    """
    plot()


def update_t_max(n):
    """
    updating GT calculations with new max temperature
    """
    # n stores the max temperature slider value as string
    gt_act.designdata.t_max = float(n) + 273.15
    gt_act.calc_gt()
    gt_eta.designdata.t_max = float(n) + 273.15
    gt_eta.opt_eta()
    gt_w.designdata.t_max = float(n) + 273.15
    gt_w.opt_w_cycle()

    plot()


def update_pi(n):
    """
    updating GT calculations with new pressure ratio
    """
    # n stores pressure ratio slider value as string
    gt_act.designdata.pi = float(n)
    gt_act.calc_gt()

    plot()


def plot():
    """
    plot after update
    """
    # plotting the graph after clearing the figure

    # only executed if plot containes lines
    for line in plot1.lines:
        line.remove()

    plot1.plot(gt_act.get_entropies()/1000,
               gt_act.get_temperatures()-273.15, 'r')
    if sh_eta.get():
        plot1.plot(gt_eta.get_entropies()/1000,
                   gt_eta.get_temperatures()-273.15, 'b')
    if sh_w.get():
        plot1.plot(gt_w.get_entropies()/1000,
                   gt_w.get_temperatures()-273.15, 'g')

    # only executed if plot containes bars
    for container in plot2.containers:
        container.remove()

    plot2.bar(['actual', 'max @ T_max'], [gt_act.eta_th * 100,
              gt_eta.eta_th * 100], color=['r', 'b'])

    # only executed if plot containes bars
    for container in plot3.containers:
        container.remove()

    plot3.bar(['actual', 'max @ T_max'], [gt_act.w_cycle/1000,
              gt_w.w_cycle/1000], color=['r', 'g'])

    canvas.draw()


# gt objects for actual and optimized pressure ratios
gt_act = GTSimple()
gt_eta = GTSimple()
gt_w = GTSimple()

# the main Tkinter window
root = Tk()
root.title('Gas Turbine Parameters')
root.geometry("900x800")

# scale for maximum GT temperature
scale_t_m = Scale(root, from_=T_MAX, to=T_MIN,
                  command=update_t_max, label="T_max")
scale_t_m.grid(row=0, column=0, rowspan=2, sticky='SN')
scale_t_m.set(int((T_MIN+T_MAX)/2))

# scale for compressor pressure ratio
scale_pi = Scale(root, from_=PI_MAX, to=PI_MIN, resolution=(
    PI_MAX-PI_MIN)/100, command=update_pi, label="pi")
scale_pi.grid(row=0, column=1, rowspan=2, sticky='SN')
scale_pi.set(int((PI_MIN+PI_MAX)/2))

# checkboxes for display of opitmized cycles in t,s-diagram
sh_eta = BooleanVar()
sh_w = BooleanVar()
show_eta = Checkbutton(root, text="Show optimum efficiency cycle",
                     variable=sh_eta, command=update_ts)
show_w = Checkbutton(root, text="Show optimum output cycle",
                     variable=sh_w, command=update_ts)
show_eta.grid(row=1, column=2, sticky='NEWS')
show_w.grid(row=1, column=3, sticky='NEWS')


# the figure that will contain the plot
fig = Figure(figsize=(5, 8),
             dpi=100)
# layout
gs = GridSpec(2, 2, figure=fig, height_ratios=(2, 1))

# adding the subplots for T,s, eta and w_cycle
plot1 = fig.add_subplot(gs[0, :])
plot2 = fig.add_subplot(gs[1, 0])
plot3 = fig.add_subplot(gs[1, 1])

plot1.set_xlim(S_LOW, S_HIGH)
plot1.set_ylim(0, T_MAX + 100)
plot1.set_xlabel('Entropy in kJ/kgK)')
plot1.set_ylabel('Temperature in °C')

plot2.set_ylabel('Efficiency in %')
plot2.set_ylim(ETA_LOW, ETA_HIGH)

plot3.set_ylabel('Specific work in kJ/(kgK)')
plot3.set_ylim(W_LOW, W_HIGH)

# creating the Tkinter canvas
# containing the Matplotlib figure
canvas = FigureCanvasTkAgg(fig,
                           master=root)

# placing the canvas on the Tkinter window
canvas.get_tk_widget().grid(row=0, column=2, columnspan=2, sticky='NEWS')

# layout details
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=1)
root.rowconfigure(0, weight=1)
fig.tight_layout()

# run the gui
root.mainloop()
