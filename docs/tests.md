# Tests

This section documents the validation, integration, and physics tests for the Environmental Quantum Field Effects (EQFE) framework.

## Overview

EQFE includes a comprehensive suite of tests to ensure scientific rigor and reproducibility. These tests cover:

- Physics validation (e.g., Tsirelson bound, amplification law)
- Integration of simulation and hardware modules
- Edge-case and stress testing
- Experimental protocol validation

## Test Types

- **Unit Tests:** Validate individual modules and functions.
- **Integration Tests:** Ensure correct operation across modules (e.g., simulation + hardware).
- **Physics Validation:** Confirm that theoretical predictions match simulation and experimental results.
- **Experimental Protocols:** Automated checks for lab procedures and data analysis.

## Running Tests

To run all tests:

```sh
python -m pytest tests/ -v
```

See the `tests/` directory for detailed test scripts and documentation.

## Key Results

- All core modules pass unit and integration tests as of July 2025.
- Physics validation tests confirm theoretical predictions within statistical uncertainty.
- Experimental protocols are validated against recent lab data.

For more details, see the [project roadmap](./project-roadmap.md) and [experimental protocols](../experiments/protocols/).
