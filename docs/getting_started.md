---
layout: default
title: Getting Started with EQFE
---

# Getting Started with EQFE

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/[username]/Environmental-Quantum-Field-Effects.git
   cd Environmental-Quantum-Field-Effects
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**:
   ```bash
   python -m pytest tests/ -v
   ```

## Quick Start

### Basic Simulation

```python
from simulations.core import EnvironmentalFieldSimulator, CHSHExperimentSimulator

# Create environmental field simulator
env_sim = EnvironmentalFieldSimulator(
    field_mass=1e-6,        # 1 μeV
    coupling_strength=1e-3,  # Weak coupling
    temperature=300.0        # Room temperature
)

# Set up Bell test experiment
chsh_sim = CHSHExperimentSimulator(env_sim)

# Run simulation
results = chsh_sim.simulate_bell_experiment(n_trials=10000)
print(f"CHSH parameter: {results['S_mean']:.4f} ± {results['S_std']:.4f}")
```

### Parameter Optimization

```python
# Find optimal conditions for enhancement
temperatures = np.linspace(50, 400, 20)
enhancements = []

for T in temperatures:
    env_sim = EnvironmentalFieldSimulator(
        field_mass=1e-6,
        coupling_strength=1e-3,
        temperature=T
    )
    A = env_sim.amplification_factor(measurement_time=1e-6)
    enhancements.append(A)

optimal_temp = temperatures[np.argmax(enhancements)]
print(f"Optimal temperature: {optimal_temp:.1f} K")
```

## Examples

Run the included example scripts:

```bash
# Basic demonstration
python examples/basic_demo.py

# Advanced analysis
python examples/advanced_analysis.py
```

## Next Steps

- Review the [theory documentation](../theory/) for mathematical details
- Check [experimental protocols](../experiments/protocols/) for lab procedures  
- Explore the [API reference](api_reference.md) for detailed usage
