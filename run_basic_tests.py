#!/usr/bin/env python3
"""
Simple Test Runner for Environmental Quantum Field Effects

This script runs basic functionality tests without requiring pytest.
For comprehensive testing, use the validate_framework.py script.
"""

import sys
import os
import numpy as np

# Add simulations directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "simulations"))


def test_basic_imports():
    """Test that all core modules can be imported."""
    print("Testing basic imports...")

    try:
        from simulations.core.field_simulator import (
            EnvironmentalFieldSimulator,
        )

        print("✓ Field simulator import successful")
    except Exception as e:
        print(f"✗ Field simulator import failed: {e}")
        return False

    try:
        from simulations.core.quantum_correlations import (
            CHSHExperimentSimulator,
        )

        print("✓ Quantum correlations import successful")
    except Exception as e:
        print(f"✗ Quantum correlations import failed: {e}")
        return False

    try:
        from simulations.analysis.physics_validator import (
            QuantumBoundsValidator,
        )

        print("✓ Physics validator import successful")
    except Exception as e:
        print(f"✗ Physics validator import failed: {e}")
        return False

    return True


def test_basic_functionality():
    """Test basic functionality of core components."""
    print("\nTesting basic functionality...")

    try:
        from simulations.core.field_simulator import (
            EnvironmentalFieldSimulator,
        )
        from simulations.core.quantum_correlations import (
            CHSHExperimentSimulator,
        )
        from simulations.analysis.physics_validator import (
            QuantumBoundsValidator,
        )

        # Test field simulator
        simulator = EnvironmentalFieldSimulator()
        field_data = simulator.thermal_field_fluctuations(100)
        assert field_data.shape == (100,)
        print("✓ Field simulation working")

        # Test CHSH simulator
        chsh_sim = CHSHExperimentSimulator(simulator)
        ideal_chsh = chsh_sim.ideal_quantum_correlation()
        assert 2.8 < ideal_chsh < 2.9  # Should be ~2√2
        print("✓ CHSH simulation working")

        # Test validator
        validator = QuantumBoundsValidator()
        result = validator.validate_chsh_parameter(2.5)
        assert result.is_valid
        print("✓ Physics validation working")

        return True

    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        return False


def main():
    """Run all basic tests."""
    print("Environmental Quantum Field Effects - Basic Test Suite")
    print("=" * 60)

    all_passed = True

    # Run tests
    all_passed &= test_basic_imports()
    all_passed &= test_basic_functionality()

    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All basic tests passed!")
        print(
            "\nFor comprehensive validation, run: python validate_framework.py"
        )
    else:
        print("❌ Some tests failed!")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
