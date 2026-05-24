import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# rocket properties
mass_dry = 0.555

diameter = 0.0668
radius = diameter / 2
area = np.pi * radius**2

Cd = 0.6
rho = 1.225
g = 9.81

# load real thrust curve from .eng file
def load_eng_file(filepath):
    times = []
    forces = []
    prop_mass_eng = None
    motor_mass_eng = None
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith(';') or line == '':
                continue
            parts = line.split()
            if len(parts) == 7:
                prop_mass_eng = float(parts[4])
                motor_mass_eng = float(parts[5])
                continue
            if len(parts) == 2:
                times.append(float(parts[0]))
                forces.append(float(parts[1]))
    return np.array(times), np.array(forces), prop_mass_eng, motor_mass_eng

thrust_time, thrust_force, prop_mass, mass_motor = load_eng_file('H128W.eng')
burn_time = thrust_time[-1]
mass_total = mass_dry + mass_motor

def thrust(t):
    return np.interp(t, thrust_time, thrust_force)

# bug: still using hardcoded prop mass and burn time, need to fix
def mass(t):
    burn_time = 1.2
    prop_mass = 0.095
    if t < burn_time:
        return mass_total - (prop_mass * t / burn_time)
    else:
        return mass_total - prop_mass

def rocket_flight(t, y):
    alt = y[0]
    vel = y[1]
    F_thrust = thrust(t)
    F_gravity = mass(t) * g
    F_drag = 0.5 * rho * Cd * area * vel**2 * np.sign(vel)
    accel = (F_thrust - F_gravity - F_drag) / mass(t)
    return [vel, accel]

t_span = (0, 60)
t_eval = np.linspace(0, 60, 6000)
y0 = [0.0, 0.0]

solution = solve_ivp(rocket_flight, t_span, y0, t_eval=t_eval, method='RK45')

time = solution.t
altitude = solution.y[0]
velocity = solution.y[1]

above_ground = altitude >= 0
time = time[above_ground]
altitude = altitude[above_ground]
velocity = velocity[above_ground]

apogee = np.max(altitude)
apogee_time = time[np.argmax(altitude)]
max_vel = np.max(velocity)

print(f"Apogee: {apogee:.1f} m ({apogee * 3.281:.0f} ft)")
print(f"Time to apogee: {apogee_time:.2f} s")
print(f"Max velocity: {max_vel:.1f} m/s (Mach {max_vel/343:.3f})")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
fig.suptitle('Project Cipher - Flight Simulation', fontsize=14)

ax1.plot(time, altitude, 'b-', linewidth=2, label='Altitude')
ax1.axvline(x=apogee_time, color='r', linestyle='--', alpha=0.7, label=f'Apogee: {apogee:.0f}m')
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Altitude (m)')
ax1.legend()
ax1.grid(True, alpha=0.3)

ax2.plot(time, velocity, 'orange', linewidth=2, label='Velocity')
ax2.axhline(y=0, color='k', linestyle='-', alpha=0.3)
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Velocity (m/s)')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/Users/reajuljannat/project-cipher/analysis/python_simulation_v2.png', dpi=150, bbox_inches='tight')
plt.show()