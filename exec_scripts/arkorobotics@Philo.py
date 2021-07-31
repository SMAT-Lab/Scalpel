#!/usr/bin/env python
# coding: utf-8
# In[1]:
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
# In[2]:
# Environment Properties
p_atm = 101325           # Pa (Ambient Pressure)
t_atm = 298.15           # K (Ambient Temperature)
t_o = 298.15             # K (Tank Temperature)
R = 8.314                # J/(K*mol)
g = 9.81                 # m/s^2
# Propellant Properties  (Air)
cp = 1.005                     # Constant pressure specific heat
cv = 0.718                     # Constant volume specific heat
molar_mass = 0.02897           # kg/mol
gamma = cp/cv                  # Specific Heat Ratio
# Tank Properties
tank_pressure = 3.1026e7            # Pa
tank_volume = 0.00147484            # m^3
tank_temp = t_o                     # K
# Regulator Properties
p_reg_min = 2.068e6                 # Pa
# Vehicle Properties
dry_mass = 1.89                     # kg (rough estimation based on current design)
prop_mass = (tank_pressure*tank_volume*molar_mass)/(R*tank_temp) # kg
wet_mass = dry_mass + prop_mass     # kg
# In[3]:
v_e_expected = 1000   # m/s (APPROXIMATION, SOURCE R.P.E.)
delta_v = v_e_expected * np.log(wet_mass/dry_mass)
print ("Delta V: %0.2f m/s" % delta_v)
# In[4]:
t_theoretical = delta_v / g
print ("Theoretical Flight Time: %0.2f sec" % t_theoretical)
# In[5]:
def area_ratio(ma):
    
    a_ratio = (1/ma)*(((1+((gamma-1)/2)*(ma**2))/(1+((gamma-1)/2)))**((gamma+1)/(2*(gamma-1))))
    
    return a_ratio
ma_array = np.arange(0.1, 4, 0.01)
a_array = area_ratio(ma_array)
plt.figure(1,figsize=(10,6))
plt.xlabel('Mach Number')
plt.ylabel('A/A*')
plt.title('Area Ratio vs Mach Number')
plt.plot(ma_array, a_array)
plt.show()
# In[6]:
# Calculate Minimum Chamber Properties
ma_t = 1.0     # Minimum mach number required to achieve choked flow is 1
p_b = p_atm    # Back pressure is pressure at sea level
p_o = p_b*((1+((gamma-1)/2)*(ma_t**2))**(gamma/(gamma-1)))
t_b = t_o/(1+(((gamma-1)/2)*(ma_t)))
p_o_critical = p_o
print ("Choked Flow:")
print ("Ma_t: %.2f" % ma_t)
print ("Given Exit/Throat Pressure: %.2f Pa" % p_b)
print ("Calculated Minimum Chamber Pressure (Critical Pressure): %.2f Pa" % p_o)
print ("Given Chamber Temperature: %.2f K" % t_o)
print ("Calculated Exit/Throat Temperature: %.2f K" % t_b)
# In[7]:
v_th = np.sqrt(((t_b * R) / molar_mass)       * ((2 * gamma) / (gamma - 1))       * ((p_o / p_b) ** (
        (gamma - 1) / gamma)) -1 )
isp = v_th / g
print ("Velocity at throat: %.2f m/s" % v_th)
print ("Specific Impulse (throat only): %2f sec" % isp)
# In[8]:
f_nom = wet_mass * g
print ("Wet Mass: %.2f kg" % wet_mass)
print ("Nominal Engine Thrust: %.2f N" % f_nom)
# In[9]:
mass_flow = f_nom / v_th         # kg/s
print ("Mass Flow Rate: %.6f kg/s" % mass_flow)
# In[10]:
p_e = p_b
t_e = t_b
a_e = (mass_flow*(1+(gamma-1)*((ma_t**2)/2))**((gamma+1)/(2*(gamma-1))))/(ma_t*p_o*np.sqrt((molar_mass*gamma)/(R*t_o)))
print ("Cross-sectional Area at Exit: %.8f m^2" % a_e)
print ("Cross-sectional Area at Exit: %.2f mm^2" % (a_e*1e6))
print ("Exit Diameter: %.2f mm" % (2*(np.sqrt((a_e*1e6)/np.pi))) )
# In[11]:
t_flight = prop_mass / mass_flow    # sec
print ("Time of Flight: %0.2f sec" % t_flight)
# In[12]:
# Functions for previously defined equations
def calc_tank_pressure(prop_mass, molar_mass, tank_t, tank_v):
    tank_p = ((prop_mass/molar_mass)*R*tank_t)/tank_v
    return tank_p                       # Pa
def calc_mach(p_o, p_b, gamma):
    ma_e = np.sqrt((2 / (gamma - 1))       * (((p_o / p_b) ** (                   (gamma - 1) / gamma))-1))  
    return ma_e                         # mach
        
def calc_t_b(t_o, ma_e, gamma):
    t_b = t_o/(1+(((gamma-1)/2)*(ma_e)))
    return t_b                          # K
def calc_v_e(p_o, p_b, t_b, molar_mass, gamma):
    v_e = np.sqrt(((t_b * R) / molar_mass)       * ((2 * gamma) / (gamma - 1))       * ((p_o / p_b) ** (               (gamma - 1) / gamma))-1)        
    return v_e                          # m/s 
def calc_isp(v_e):
    isp = v_e / g
    return isp                          # sec
def calc_f_nom(wet_mass):
    f_nom = wet_mass * g
    return f_nom                        # N
def calc_mass_flow(f_nom, v_e):
    mass_flow = f_nom / v_e              
    return mass_flow                    # kg/s 
def calc_area_exit(p_o, t_o, ma_e, mass_flow, molar_mass, gamma):
    a_e = (mass_flow*(1+(gamma-1)*((ma_e**2)/2))**((gamma+1)/(2*(gamma-1))))/(ma_e*p_o*np.sqrt((molar_mass*gamma)/(R*t_o)))
    return a_e                          # m^2
def calc_time_of_flight(prop_mass, mass_flow):
    t_flight = prop_mass / mass_flow    
    return t_flight                     # sec
# Time of Flight vs Chamber Pressure
# Note: We assume constant thrust for simplcity (compensated later in step 9 for greater accuracy)
def calc_engine_params(p_o):
    ma_e = calc_mach(p_o, p_b, gamma)
    t_b = calc_t_b(t_o, ma_e, gamma)
    v_e = calc_v_e(p_o, p_b, t_b, molar_mass, gamma)
    isp = calc_isp(v_e)
    f_nom = calc_f_nom(wet_mass)
    mass_flow = calc_mass_flow(f_nom, v_e)
    a_e = calc_area_exit(p_o, t_o, ma_e, mass_flow, molar_mass, gamma)
    t_flight = calc_time_of_flight(prop_mass, mass_flow)
    
    return t_flight, a_e, ma_e
# p_o_min calculated above
p_step = 10000
p_o_min = p_o_critical  # Minimum pressure for choked flow state
# Sweep the pressure and plot the time of flight
p_array = np.arange(int(p_o_min), int(p_reg_min), p_step)
tof_array, ae_array, mae_array = calc_engine_params(p_array)
ae_array *= 1e6     # Convert from m^2 to mm^2
plt.figure(2,figsize=(10,6))
plt.xlabel('Pressure (Pa)')
plt.ylabel('Time of Flight (sec)')
plt.title('ToF vs Pressure')
plt.plot(p_array, tof_array)
plt.show()
plt.figure(3,figsize=(10,6))
plt.xlabel('Pressure (Pa)')
plt.ylabel('Area at Exit (mm^2)')
plt.title('A_e vs Pressure')
plt.plot(p_array, ae_array)
plt.show()
plt.figure(4,figsize=(10,6))
plt.xlabel('Pressure (Pa)')
plt.ylabel('Mach Number')
plt.title('Mach vs Pressure')
plt.plot(p_array, mae_array)
plt.show()
# In[13]:
p_chamber = 5e5 # Pa (~70psi), this value assumes the needle valve regulates 300psi (bottle reg) down to 70psi
tof, a_e, ma_e = calc_engine_params(p_chamber)
print ("Selected Chamber Pressure: %.2f Pa" % p_chamber)
print ("Calculated ToF: %0.2f sec" % tof)
print ("Calculated A_e: %0.8f m^2" % a_e)
print ("Calculated A_e: %.2f mm^2" % (a_e*1e6))
print ("Calculated Exit Diameter: %.2f mm" % (2*(np.sqrt((a_e*1e6)/np.pi))) )
# In[14]:
print ("Exit Mach: %.2f\n" % ma_e)
a_t = (a_e*ma_e)*(((2/(gamma+1))*(1+((gamma-1)/2)*(ma_e**2)))**((-(gamma+1))/(2*(gamma-1))))
print ("Area at Throat: %0.8f m^2" % a_t)
print ("Area at Throat: %.2f mm^2" % (a_t*1e6))
print ("Throat Diameter: %.2f mm \n" % (2*(np.sqrt((a_t*1e6)/np.pi))) )
print ("Area at Exit: %0.8f m^2" % a_e)
print ("Area at Exit: %.2f mm^2" % (a_e*1e6))
print ("Exit Diameter: %.2f mm \n" % (2*(np.sqrt((a_e*1e6)/np.pi))) )
# Ae/At Ratio
a_e_a_t = a_e / a_t
print ("Ae/At Ratio: %0.2f" % a_e_a_t)
# In[15]:
def tank_sim(t_i, tank_volume, prop_mass, mass_flow, dt):
        
    tank_time = 0.0
    
    tank_t_i = tank_t_f = t_i
    
    tank_p_i = tank_p_f = ((prop_mass/molar_mass)*R*(tank_t_i))/tank_volume
    
    time, tank_p, tank_t = [0],[tank_p_f],[tank_t_f]
    
    while tank_p_f >= p_reg_min:
        tank_p_i = tank_p_f
        tank_t_i = tank_t_f
        prop_mass = prop_mass - (mass_flow*dt)
        tank_time = tank_time + dt
        
        tank_p_f = ((prop_mass/molar_mass)*R*tank_t_f)/tank_volume
        tank_t_f = tank_t_i/((tank_p_i/tank_p_f)**((gamma-1)/gamma))
        
        time.append(tank_time)
        tank_p.append(tank_p_f)
        tank_t.append(tank_t_f)
        
    return time, tank_p, tank_t
time, tank_p, tank_t = tank_sim(tank_temp, tank_volume, prop_mass, mass_flow, 0.1)
plt.figure(5,figsize=(10,6))
plt.xlabel('Time (sec)')
plt.ylabel('Pressure (Pa)')
plt.title('Pressure vs Time')
plt.plot(time, tank_p)
plt.show()
plt.figure(6,figsize=(10,6))
plt.xlabel('Time (sec)')
plt.ylabel('Temperature (K)')
plt.title('Temperature vs Time')
plt.plot(time, tank_t)
plt.show()
# In[16]:
def vehicle_sim(molar_mass, prop_mass_init, tank_t_init, tank_v, dt):   
    
    # Initialize Tank
    tank_pressure = calc_tank_pressure(prop_mass_init, molar_mass, tank_t_init, tank_v)
    tank_volume = tank_v
    tank_prop_mass = prop_mass_init
    tank_temp = tank_t_init
    
    #Initialize Engine
    engine_p_o = p_chamber
    engine_t_o = tank_temp
    
    # Calculate Initial Engine State
    ma_e = calc_mach(engine_p_o, p_b, gamma)
    t_b = calc_t_b(engine_t_o, ma_e, gamma)
    v_e = calc_v_e(engine_p_o, p_b, t_b, molar_mass, gamma)
    isp = calc_isp(v_e)
    wet_mass = dry_mass + tank_prop_mass
    f_nom = calc_f_nom(wet_mass)
    mass_flow = calc_mass_flow(f_nom, v_e)
    a_e = calc_area_exit(p_o, t_o, ma_e, mass_flow, molar_mass, gamma)
    t_flight = calc_time_of_flight(tank_prop_mass, mass_flow)  
    
    # Simulation Initialization
    time = 0
    sim_time, sim_tank_p, sim_tank_t, sim_f_nom, sim_a_e, sim_ma_e = [time],                                                            [tank_pressure],                                                            [tank_temp],                                                            [f_nom],                                                            [a_e],                                                            [ma_e]
    # Simulation Loop
    while tank_pressure >= p_reg_min:
        # Calculate Tank State
        tank_p_i = tank_pressure
        tank_t_i = tank_temp
        tank_prop_mass = tank_prop_mass - (mass_flow*dt)
        time = time + dt
        
        tank_pressure = ((tank_prop_mass/molar_mass)*R*tank_temp)/tank_volume
        tank_temp = tank_t_i/((tank_p_i/tank_pressure)**((gamma-1)/gamma))
        
        sim_time.append(time)
        sim_tank_p.append(tank_pressure)
        sim_tank_t.append(tank_temp)
        
        # Calculate Engine State
        engine_t_o = tank_t_i
        
        ma_e = calc_mach(engine_p_o, p_b, gamma)
        t_b = calc_t_b(engine_t_o, ma_e, gamma)
        v_e = calc_v_e(engine_p_o, p_b, t_b, molar_mass, gamma)
        isp = calc_isp(v_e)
        wet_mass = dry_mass + tank_prop_mass
        f_nom = calc_f_nom(wet_mass)
        mass_flow = calc_mass_flow(f_nom, v_e)
        a_e = calc_area_exit(p_o, t_o, ma_e, mass_flow, molar_mass, gamma)
        t_flight = calc_time_of_flight(tank_prop_mass, mass_flow)   
        
        sim_f_nom.append(f_nom)
        sim_a_e.append(a_e)
        sim_ma_e.append(ma_e)
        
    return sim_time, sim_tank_p, sim_tank_t, sim_f_nom, sim_a_e, sim_ma_e
time, tank_p, tank_t, f_nom, a_e, ma_e = vehicle_sim(molar_mass, prop_mass, t_o, tank_volume, 0.1)
plt.figure(7,figsize=(10,6))
plt.xlabel('Time (sec)')
plt.ylabel('Pressure (Pa)')
plt.title('Tank Pressure vs Time')
plt.plot(time, tank_p)
plt.show()
plt.figure(8,figsize=(10,6))
plt.xlabel('Time (sec)')
plt.ylabel('Tank Temperature (K)')
plt.title('Tank Temperature vs Time')
plt.plot(time, tank_t)
plt.show()
plt.figure(9,figsize=(10,6))
plt.xlabel('Time (sec)')
plt.ylabel('Exit Area at Exit (mm^2)')
plt.title('A_e vs Time')
plt.plot(time, a_e)
plt.show()
plt.figure(10,figsize=(10,6))
plt.xlabel('Time (sec)')
plt.ylabel('Force (N)')
plt.title('F nominal vs Time')
plt.plot(time, f_nom)
plt.show()
# In[17]:
# Print out final parameters
print ("Nominal Chamber Pressure: %.2f Pa\n" % p_o)
print ("Exit Mach Number: %.2f\n" % ma_e[0])
print ("Time of Flight: %0.2f sec\n" % time[len(time)-1])
print ("A_e: %.2f mm^2" % (a_e[0]*1e6))
print ("Exit Diameter: %.2f mm\n" % (2*(np.sqrt((a_e[0]*1e6)/np.pi))) )
print ("A_t: %.2f mm^2" % (a_t*1e6))
print ("Throat Diameter: %.2f mm \n" % (2*(np.sqrt((a_t*1e6)/np.pi))) )
print ("Ae/At Ratio: %0.2f" % a_e_a_t)