# Scribble

## What to do

In theory you can calculate anything just using respective equations like 
$a^2+b^2=c^2$.

If you think you are firm in mathematics you may just switch to matrices: 

$$
\begin{matrix}
  a & b & c \\
  d & e & f \\
  g & h & i
\end{matrix}
$$

The partial derivates $\left(\frac{\partial h}{\partial T}\right)_p$ and $\left(\frac{\partial h}{\partial p}\right)_T$ can be used to describe how the enthalpy $h$ changes, if temperature $T$ and/or pressure $p$ changes. For this the total derivate of enthalpy is used:

$$
\mathrm{d}h=\left(\frac{\partial h}{\partial T}\right)_p\,\mathrm{d}T+ \left(\frac{\partial h}{\partial p}\right)_T\,\mathrm{d}p
$$

That looks good! 

$$
\left[\begin{array}{ccc}
\dfrac{\partial f_{1}(\mathbf{x})}{\partial x_{1}} & \cdots & \dfrac{\partial f_{1}(\mathbf{x})}{\partial x_{n}}  \\
\vdots & \ddots & \vdots \\
\dfrac{\partial f_{m}(\mathbf{x})}{\partial x_{1}} & \cdots & \dfrac{\partial f_{m}(\mathbf{x})}{\partial x_{n}}  
\end{array}\right]

\left[\begin{array}{ccc}
\mathrm{d}x_{1} & \cdots & \mathrm{d}x_{n} 
\end{array}\right]


=\left[\begin{array}{c}
\mathrm{d}f_{1}\\
\vdots\\
\mathrm{d}f_{m}
\end{array}\right]
$$

$$
\left[\begin{array}{ccc}
\dfrac{\partial f_{1}(\mathbf{x})}{\partial x_{1}} & \cdots & \dfrac{\partial f_{1}(\mathbf{x})}{\partial x_{n}}  \\
\vdots & \ddots & \vdots \\
\dfrac{\partial f_{m}(\mathbf{x})}{\partial x_{1}} & \cdots & \dfrac{\partial f_{m}(\mathbf{x})}{\partial x_{n}}  
\end{array}\right]
$$


Now some code that could be suggested for implementation

```
"""
module for starting with python in thermal engineering
a simple and straighht foreward calculation of an example property
belongs to 
unit 1: calculation of thermal properties
"""
p = 1 * 10**5 #pressure in Pa
t = 20 + 273.15 # temperature in K
r = 287 #gas constant in J/(kgK)

v =  r * t / p #specific volume in m^3/kg
print(v)
```
Explain what the code is all about...