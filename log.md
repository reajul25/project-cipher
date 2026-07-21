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
- Downloaded real H128W thrust curve from thrustcurve.org (certified RASP format)
- Updated flight_sim.py to load thrust curve from .eng file instead of hardcoded values
- Bug found: mass function still using hardcoded propellant mass, will fix next
- Updated results:
  - Apogee: 695 m (2281 ft)
  - Time to apogee: 10.04 s
  - Max velocity: 200.6 m/s (Mach 0.585)
- Velocity now much closer to OpenRocket (200.6 vs 196 m/s)
- Apogee higher than OpenRocket (695 vs 626 m) — likely due to Cd = 0.6 being too low

#### OpenRocket Model Update
- Found official LOC Precision RockSim file (.RKT) on product page
- Extracted exact manufacturer dimensions and updated all components
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
- Set boundary conditions: velocity inlet, pressure outlet, wall on rocket surfaces
- Set up drag force result control
- Mesh generation failed with self-intersection error in the STL
- Attempted trimesh convex-hull repair — fixed watertightness but destroyed fin geometry
- Decision: rebuild geometry in CAD for a clean STEP export instead of trying
  to repair the OpenRocket STL

### Week 2
#### CAD Rebuild — Switch to Onshape
- Originally planned in SolidWorks, but no Windows machine available on Mac
- Switched to Onshape (browser-based)
- Cross-checked all dimensions against the .ork file directly by unpacking the
  XML — confirmed nosecone shape (ogive, ShapeCode 1) and full fin/tube geometry

#### Onshape Model
- Nosecone: built as a tangent ogive using FeatureScript
  - Computed profile as spline through 21 calculated points
  - Tangent constraint at tip to avoid a sharp discontinuity for CFD
  - Rho = 799 mm, L = 228.6 mm, base radius = 33.401 mm
- Body tube: extruded as a solid cylinder (not hollow) since only the outer
  surface matters for external-flow CFD
- Fins: trapezoidal profile with correct interior angles (70°/80°/100°/110°)
  after removing the incorrect vertical trailing-edge constraint
  - Fin root extended ~3 mm into the body tube so the Boolean union has
    actual overlapping volume — this was the root cause of the earlier
    self-intersection failures with the OpenRocket STL export
  - Circular pattern for 3 fins at 120° spacing
- Verified as a single merged solid body in the feature tree
- Exported as STEP (AP242)

### Week 3
#### CFD — SimScale Rebuild
- Imported STEP file into SimScale — clean B-rep geometry, no triangulation issues
- Built external flow domain in SimScale's CAD Edit mode using the External tool
  - X: −700 to +2663.65 mm (700 mm upstream, 1400 mm downstream)
  - Y, Z: ±675 mm (~5× max diameter radial clearance)
- Deleted the solid rocket body after flow region extraction, leaving only the
  fluid domain (required for single-region incompressible analysis)
- Currently reassigning boundary conditions and result controls to the new
  flow region faces before running the mesh generation

