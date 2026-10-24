<div align="center">

# awesome-verified-scientific-computing

### Small, honestly verified scientific codes — where every accuracy claim is measured

**Solvers whose numbers you can actually check: benchmarks against exact solutions,
independent formulations, or hand computation — with tests, raw data and stated limits.**

</div>

---

## Why this list

Most scientific example code shows a pretty picture and stops. The projects
collected here go further: they state what they claim, measure it, and say what
they do *not* claim. Criteria for inclusion:

- ✅ verification against an exact/analytic reference, an independent method,
  or a hand-computed case, with the measured error reported
- ✅ automated tests (unit and/or CI)
- ✅ honest limitations section
- ✅ reproducible results (scripts + raw data)

## Contents

- [Why this list](#why-this-list)
- [CFD — lattice-Boltzmann, finite volume, spectral](#cfd--lattice-boltzmann-finite-volume-spectral)
- [Physics-informed & reduced-order machine learning](#physics-informed--reduced-order-machine-learning)
- [Classical numerical analysis](#classical-numerical-analysis)
- [Thermal & transport](#thermal--transport)
- [Geometry, data & tooling](#geometry-data--tooling)
- [Contributing](#contributing)
- [License](#license)

## CFD — lattice-Boltzmann, finite volume, spectral

| Project | What it verifies |
| --- | --- |
| [Vortex Notebook](https://github.com/khalil-work/vortex-notebook) | 2-D Navier–Stokes spectral solver; Taylor–Green at the roundoff floor, nonlinear operator vs 3/2-rule padded reference to 1e-12 |
| [Channel Lattice](https://github.com/khalil-work/channel-lattice) | D2Q9 LBM channel flow; emergent Poiseuille profile vs analytic parabola, measured 2nd-order convergence |
| [Shockline](https://github.com/khalil-work/shockline-euler) | 1-D Euler Rusanov + MUSCL/SSP-RK3 vs exact Newton-iteration Riemann solver; measured orders 1 and 2 |
| [Dedalus Project](https://github.com/DedalusProject/dedalus) | Spectral PDE framework with extensive test suite against analytic solutions (large project) |

## Physics-informed & reduced-order machine learning

| Project | What it verifies |
| --- | --- |
| [Droplet PINN Studio](https://github.com/khalil-work/droplet-pinn-studio) | PINN IC-handling study on a law with a free exact solution; equal budgets, 3 seeds |
| [Modal Current](https://github.com/khalil-work/modal-current) | POD + exact DMD recovering known synthetic frequencies/growth rates to ~1e-14 |
| [DeepXDE](https://github.com/lululxvi/deepxde) | The reference PINN library (large project) |

## Classical numerical analysis

| Project | What it verifies |
| --- | --- |
| [Quadrature Workbench](https://github.com/khalil-work/quadrature-workbench) | Adaptive Simpson with honest termination statuses; bounded benchmark enforced by regression (C++17) |
| [Bracket Root](https://github.com/khalil-work/bracket-root-fortran) | Bisection/Illinois/safeguarded secant with iteration counts measured vs published roots (Fortran 2018) |
| [Cooling Curve Inverse](https://github.com/khalil-work/cooling-curve-inverse) | Levenberg–Marquardt with analytic Jacobian vs finite differences; exact noise-free recovery (C++) |
| [Trajectory Fusion](https://github.com/khalil-work/trajectory-fusion-c) | Kalman filter: Joseph form, NIS/NEES chi-square consistency, Riccati vs Kalata closed form (C99) |
| [Variance Compass](https://github.com/khalil-work/variance-compass) | Sobol' sensitivity indices vs analytic Ishigami values with bootstrap errors |

## Thermal & transport

| Project | What it verifies |
| --- | --- |
| [Thermal Streams](https://github.com/khalil-work/thermal-streams) | eps-NTU rating cross-checked against an independent LMTD formulation (770 tests) |
| [Thermal Pathways](https://github.com/khalil-work/thermal-pathways) | Wall networks solved two independent ways; exact straight-fin analytics, three tip treatments |
| [Pipeflow Bench](https://github.com/khalil-work/pipeflow-bench) | Implicit Colebrook solved by bracketed bisection; root verified to 1e-12 vs its own equation |
| [Ignition Zero](https://github.com/khalil-work/ignition-zero) | 0-D Arrhenius ignition; energy invariant conserved to roundoff through runaway (C++) |
| [Heatwave](https://github.com/khalil-work/heatwave-octave) | FTCS vs analytic decaying sine; implicit scheme stable at 32x the explicit limit (Octave) |
| [Droplet Journey](https://github.com/khalil-work/droplet-journey) | 0-D evaporation/heating vs Radau reference; population atlas with exact mass ledger |

## Geometry, data & tooling

| Project | What it verifies |
| --- | --- |
| [Triangle Mesh Audit](https://github.com/khalil-work/triangle-mesh-audit) | STL geometry/quality checks; exact tetrahedron volume 1/6, sphere 4pi/3 |
| [Energy Flow Atlas](https://github.com/khalil-work/energy-flow-atlas) | Sankey ribbons drawn only after node conservation is proven to close |
| [Parallel Numerics Bench](https://github.com/khalil-work/parallel-numerics-bench) | Serial/parallel equivalence: bit-identical results under any partitioning (C++17) |
| [Truss Equilibrium](https://github.com/khalil-work/truss-equilibrium) | Direct-stiffness truss vs hand statics and method-of-joints closure to 1e-12 |

## Contributing

Know a small verified code (exact-reference benchmarks, tests, honest limits)?
Open an issue or PR. Self-promotion is fine if the verification criteria are met.
See [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines on inclusion criteria, required format, and review steps.

## License

[CC0-1.0](https://creativecommons.org/publicdomain/zero/1.0/) — the list text
itself; each linked project keeps its own license.
