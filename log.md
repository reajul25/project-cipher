# Project Cipher — Build Log

## May 2026
### Week 1
- Set up GitHub repo and project structure
- Downloaded OpenRocket
- Ordered LOC Hi-Tech kit and Eggtimer ION

### Week 2
### OpenRocket Simulation — Baseline Results
- Apogee: 626 m 
- Max velocity: 196 m/s (Mach 0.577)
- Max acceleration: 242 m/s²
- Stability: 3.31 cal / 18.8%
- Motor: Aerotech H128W-6
- Notes: Initial simulation with nominal dimensions, mass will be updated once rocket is under construction 

### Python Simulation — Version 1
- Created flight_sim.py with basic physics model from scratch
- Implemented thrust, gravity, and drag forces using Newton's second law
- Used simplified hardcoded thrust curve for H128W (approximate values)
- Used scipy solve_ivp with RK45 to numerically integrate equations of motion
- Results:
  - Apogee: 624m (2047 ft)
  - Time to apogee: 10.04s
  - Max velocity: 168 m/s (Mach 0.490)
- Apogee close to OpenRocket (624 vs 626m), velocity lower due to simplified thrust curve

## Week 3
### Python Simulation — Version 2
- Downloaded real H128W thrust curve from thrustcurve.org (certified RASP format)
- Updated flight_sim.py to load thrust curve from .eng file instead of hardcoded values
- Bug found: mass function still using hardcoded propellant mass, will fix next
- Updated results:
  - Apogee: 695m (2281 ft)
  - Time to apogee: 10.04s
  - Max velocity: 200.6 m/s (Mach 0.585)
- Velocity now much closer to OpenRocket (200.6 vs 196 m/s)
- Apogee higher than OpenRocket (695 vs 626m) — likely due to Cd = 0.6 being too low

### OpenRocket Model Update
- Found official LOC Precision RockSim file (.RKT) on product page
- Extracted exact manufacturer dimensions and updated all components
- Key corrections: nosecone length 13.97→22.86cm, fin root chord 14→12.7cm,
  fin sweep 8.89→3.696cm, motor mount length 30.48→25.4cm
- Updated simulation results:
  - Apogee: 614m (2014 ft)
  - Max velocity: 201 m/s (Mach 0.592)
  - Max acceleration: 251 m/s²
  - Stability: 3.13 cal / 16.6%
