#!/usr/bin/env python3
"""
Simple validation test for Environmental Quantum Field Effects

This script performs basic validation of the core modules without requiring
external testing frameworks.
"""

import sys
import traceback
from pathlib import Path
import numpy as np

# Add package path
sys.path.append(str(Path(__file__).parent.parent))


def test_imports():
    """Test that all modules can be imported successfully."""
    print("Testing module imports...")

    try:
        from simulations.core.field_simulator import (
            EnvironmentalFieldSimulator,
            PhysicalConstants,
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

    try:
        from simulations.analysis.experimental_analysis import CHSHAnalyzer

        print("✓ Experimental analysis import successful")
    except Exception as e:
        print(f"✗ Experimental analysis import failed: {e}")
        return False

    return True


def test_field_simulator():
    """Test basic field simulator functionality."""
    print("\nTesting field simulator...")

    try:
        from simulations.core.field_simulator import (
            EnvironmentalFieldSimulator,
        )

        # Create simulator
        simulator = EnvironmentalFieldSimulator(
            field_mass=1e-6,
            coupling_strength=0.005,  # Smaller coupling for stability
            temperature=300.0,
        )
        print("✓ Simulator initialization successful")

        # Test field generation
        field_data = simulator.thermal_field_fluctuations(1000)
        assert field_data.shape == (
            1000,
        ), f"Expected shape (1000,), got {field_data.shape}"
        assert np.isfinite(
            field_data
        ).all(), "Field data contains non-finite values"
        print("✓ Field generation successful")

        # Test correlation modification
        ideal_chsh = 2.2  # Smaller starting value for stability
        modified_chsh = simulator.modify_quantum_correlations(
            ideal_chsh, field_data, 1.0
        )
        assert (
            modified_chsh.shape == field_data.shape
        ), "Shape mismatch in correlation modification"
        assert np.isfinite(
            modified_chsh
        ).all(), "Modified CHSH contains non-finite values"
        print("✓ Correlation modification successful")

        return True

    except Exception as e:
        print(f"✗ Field simulator test failed: {e}")
        traceback.print_exc()
        return False


def test_physics_validator():
    """Test physics validation functionality."""
    print("\nTesting physics validator...")

    try:
        from simulations.analysis.physics_validator import (
            QuantumBoundsValidator,
        )

        validator = QuantumBoundsValidator()
        print("✓ Validator initialization successful")

        # Test valid CHSH values
        valid_chsh = np.array([2.0, 2.5, 2.8])
        result = validator.validate_chsh_parameter(valid_chsh)
        assert result.is_valid, "Valid CHSH values failed validation"
        print("✓ Valid CHSH validation successful")

        # Test invalid CHSH values
        invalid_chsh = np.array([3.0, 3.5])
        result = validator.validate_chsh_parameter(invalid_chsh)
        assert not result.is_valid, "Invalid CHSH values passed validation"
        assert (
            len(result.violations) > 0
        ), "No violations detected for invalid values"
        print("✓ Invalid CHSH detection successful")

        return True

    except Exception as e:
        print(f"✗ Physics validator test failed: {e}")
        traceback.print_exc()
        return False


def test_chsh_experiment():
    """Test CHSH experiment simulation."""
    print("\nTesting CHSH experiment simulation...")

    try:
        from simulations.core.field_simulator import (
            EnvironmentalFieldSimulator,
        )
        from simulations.core.quantum_correlations import (
            CHSHExperimentSimulator,
        )

        # Create simulators with conservative parameters for testing
        env_simulator = EnvironmentalFieldSimulator(
            coupling_strength=1e-4  # Very small coupling for test stability
        )
        chsh_simulator = CHSHExperimentSimulator(env_simulator)
        print("✓ CHSH simulator initialization successful")

        # Test ideal quantum correlation
        ideal_chsh = chsh_simulator.ideal_quantum_correlation()
        expected = 2 * np.sqrt(2)
        assert (
            abs(ideal_chsh - expected) < 1e-10
        ), f"Expected {expected}, got {ideal_chsh}"
        print("✓ Ideal quantum correlation calculation successful")

        # Test Bell experiment simulation
        n_trials = 100  # Small number for quick test
        result = chsh_simulator.simulate_bell_experiment(n_trials=n_trials)

        assert "chsh_values" in result, "Missing chsh_values in result"
        assert result["chsh_values"].shape == (
            n_trials,
        ), "Incorrect shape for chsh_values"
        assert np.isfinite(
            result["chsh_values"]
        ).all(), "Non-finite values in CHSH results"
        print("✓ Bell experiment simulation successful")

        return True

    except Exception as e:
        print(f"✗ CHSH experiment test failed: {e}")
        traceback.print_exc()
        return False


def test_analysis_pipeline():
    """Test complete analysis pipeline."""
    print("\nTesting analysis pipeline...")

    try:
        from simulations.analysis.experimental_analysis import (
            CHSHAnalyzer,
            EnvironmentalCorrelationAnalyzer,
            ExperimentalData,
        )

        # Create test data
        n_points = 500
        timestamps = np.linspace(0, 100, n_points)
        chsh_values = 2.4 + 0.1 * np.random.normal(0, 1, n_points)
        field_data = np.random.normal(0, 1, n_points)

        test_data = ExperimentalData(
            timestamps=timestamps,
            chsh_values=chsh_values,
            correlations={},
            environmental_fields={"magnetic_field": field_data},
            detector_counts={},
            analyzer_settings={},
        )
        print("✓ Test data creation successful")

        # Test CHSH analyzer
        analyzer = CHSHAnalyzer()
        time_results = analyzer.analyze_time_evolution(test_data)
        assert "max_chsh" in time_results, "Missing max_chsh in time results"
        print("✓ CHSH time analysis successful")

        # Test environmental correlation analyzer
        env_analyzer = EnvironmentalCorrelationAnalyzer()
        field_variance = env_analyzer.calculate_field_variance(field_data)
        assert field_variance.shape == (
            n_points,
        ), "Incorrect field variance shape"
        assert np.all(field_variance >= 0), "Negative field variance detected"
        print("✓ Environmental correlation analysis successful")

        return True

    except Exception as e:
        print(f"✗ Analysis pipeline test failed: {e}")
        traceback.print_exc()
        return False


def test_physical_constants():
    """Test physical constants consistency."""
    print("\nTesting physical constants...")

    try:
        from simulations.core.field_simulator import PhysicalConstants

        # Test basic constants
        assert PhysicalConstants.c == 299792458.0, "Incorrect speed of light"
        assert PhysicalConstants.hbar > 0, "Invalid reduced Planck constant"
        print("✓ Basic constants correct")

        # Test electromagnetic consistency: c = 1/√(μ₀ε₀)
        c_derived = 1.0 / np.sqrt(
            PhysicalConstants.mu_0 * PhysicalConstants.epsilon_0
        )
        assert (
            abs(c_derived - PhysicalConstants.c) < 1e-6
        ), "Electromagnetic constants inconsistent"
        print("✓ Electromagnetic constants consistent")

        return True

    except Exception as e:
        print(f"✗ Physical constants test failed: {e}")
        traceback.print_exc()
        return False


def main():
    """Run all validation tests."""
    print("Environmental Quantum Field Effects - Validation Test Suite")
    print("=" * 70)

    tests = [
        test_imports,
        test_physical_constants,
        test_field_simulator,
        test_physics_validator,
        test_chsh_experiment,
        test_analysis_pipeline,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} crashed: {e}")
            failed += 1

    print("\n" + "=" * 70)
    print(f"Test Results: {passed} passed, {failed} failed")

    if failed == 0:
        print(
            "🎉 All tests passed! The Environmental Quantum Field Effects framework is ready."
        )
        return 0
    else:
        print("❌ Some tests failed. Please check the error messages above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
