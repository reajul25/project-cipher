# Project Cipher — Build Log

## May 2026

### Week 1
- Set up GitHub repo and project structure
- Downloaded OpenRocket
- Ordered LOC Hi-Tech kit and Eggtimer ION

### Week 2
#### OpenRocket Simulation — Baseline Results
- Apogee: 626 m
- Max velocity: 196 m/s (Mach 0.577)
- Max acceleration: 242 m/s²
- Stability: 3.31 cal / 18.8%
- Motor: Aerotech H128W-6
- Notes: Initial simulation with nominal dimensions, mass will be updated once rocket is under construction

#### Python Simulation — Version 1
- Created flight_sim.py with basic physics model from scratch
- Implemented thrust, gravity, and drag forces using Newton's second law
- Used simplified hardcoded thrust curve for H128W (approximate values)
- Used scipy solve_ivp with RK45 to numerically integrate equations of motion
- Results:
  - Apogee: 624 m (2047 ft)
  - Time to apogee: 10.04 s
  - Max velocity: 168 m/s (Mach 0.490)
- Apogee close to OpenRocket (624 vs 626 m), velocity lower due to simplified thrust curve

### Week 3
#### Python Simulation — Version 2
- Updated flight_sim.py to load thrust curve from .eng file instead of hardcoded values
- Bug found: mass function still using hardcoded propellant mass, will fix next
- Updated results:
  - Apogee: 695 m (2281 ft)
  - Time to apogee: 10.04 s
  - Max velocity: 200.6 m/s (Mach 0.585)
- Velocity now much closer to OpenRocket (200.6 vs 196 m/s)
- Apogee higher than OpenRocket (695 vs 626 m) — likely due to Cd = 0.6 being too low

#### OpenRocket Model Update
- Found and extracted exact manufacturer dimensions and updated all components
- Key corrections: nosecone length 13.97→22.86 cm, fin root chord 14→12.7 cm,
  fin sweep 8.89→3.696 cm, motor mount length 30.48→25.4 cm
- Updated simulation results:
  - Apogee: 614 m (2014 ft)
  - Max velocity: 201 m/s (Mach 0.592)
  - Max acceleration: 251 m/s²
  - Stability: 3.13 cal / 16.6%

## June 2026

### Week 1
#### Rocket Build — Phase 1 & Phase 2
- Dry fit all parts to verify fit before any epoxy
- Sanded all mating surfaces with 120 grit for better epoxy adhesion
- Marked fin alignment on booster tube
- Slid centering rings onto 38mm motor mount tube
- Positioned front and aft centering rings
- Motor mount assembly in progress — epoxy cure underway

#### Python Simulation — Version 3
- Fixed mass function bug: now pulling propellant mass directly from .eng file
  so thrust and mass are internally consistent
- Updated Cd from 0.6 to 0.75 using FixedCd value from manufacturer RockSim data
- Results:
  - Apogee: 608 m
  - Max velocity: 194 m/s (Mach 0.566)
- Now within ~1% of OpenRocket apogee (608 vs 614 m)
- Key takeaway: manufacturer Cd was the dominant lever, reducing error from
  ~11% down to under 1%

## July 2026

### Week 1
#### CFD — First Attempt (Failed)
- Exported rocket from OpenRocket as OBJ → converted to STL using trimesh
- Uploaded to SimScale, geometry loaded with correct shape
- Configured Incompressible analysis (Compressible requires paid plan):
  k-omega SST turbulence, steady-state, Air material
- Set boundary conditions and result control
- Mesh generation failed with self-intersection error in the STL
- Attempted trimesh convex-hull repair — fixed watertightness but destroyed fin geometry
- Decision: rebuild geometry in CAD for a clean STEP export instead of trying
  to repair the OpenRocket STL

### Week 2
#### CAD Rebuild — Switch to Onshape
- Originally planned in SolidWorks, but don't have access to a Windows computer
- Switched to Onshape (browser-based)
- Cross-checked all dimensions against the .ork file directly by unpacking the
  XML — confirmed nosecone shape (ogive, ShapeCode 1) and full fin/tube geometry

#### Onshape Model
- Nosecone: built as a tangent ogive using FeatureScript
  - Rho = 799 mm, L = 228.6 mm, base radius = 33.401 mm
- Body tube: extruded as a solid cylinder since only the outer
  surface matters for external-flow CFD
- Fins: trapezoidal profile with correct interior angles (70°/80°/100°/110°)
  - Fin root extended ~3 mm into the body tube so the Boolean union has
    actual overlapping volume — figured this was the root cause of the earlier
    self-intersection failures with the OpenRocket STL export

### Week 3
#### CFD — Setup in SimScale
- Imported the Onshape STEP into SimScale and built the external flow
  domain around the rocket
- Deleted the solid rocket body since incompressible needs only the fluid
  domain
- Set up boundary conditions - velocity inlet at 100 m/s, pressure outlet,
  slip walls on the outer sides of the box (so the flow doesn't stick
  to them). Left the rocket surfaces alone (SimScale treats
  unassigned faces as no-slip walls by default)
- Set up force and moment coefficients on the rocket surfaces to get Cd

### Week 4
#### CFD — First Run
- Ran a standard mesh with ~450k cells for 1000 iterations
- **Cd = 0.37** — converged but way lower than manufacturer's 0.75

#### Understanding by Cd converged so low
After some research and help, I learned: 
Rocket drag has two big components: pressure drag (air pushing against the nose and getting stuck behind the fins) and skin friction drag (friction between the air and the rocket surface). Skin friction happens in the boundary layer, which is a super thin layer of air (~1-2mm) right against the surface where the flow slows down from 100 m/s to 0.

#### CFD — Second Run With Refined Mesh
- Added a surface refinement and boundary layer inflation on the rocket walls to put smaller cells at the surface, which allowed the sim to actually calculate the skin friction and add it to the total drag
- First attempt at the boundary layer settings gave really bad cell
  aspect ratios so I bumped up the relative thickness until it looked normal
- **Cd = 0.50** — big jump from 0.37, now within ~33% of manufacturer 0.75

#### Takeaways
- STEP from the clean CAD rebuild fixed all the self-intersection stuff
  that broke the STL attempt
- Boundary layer refinement was the main lever, without it the sim was
  missing a big chunk of the drag
- Not going to keep pushing on this. The remaining gap to 0.75 probably
  comes from stuff my sim doesn't have — no launch lug, no rail buttons,
  incompressible only (real peak is Mach 0.59), and no surface roughness
- Good place to stop and get back to the physical build
