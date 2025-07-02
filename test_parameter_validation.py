#!/usr/bin/env python3
"""
EQFE Parameter Validation Test Script

This script demonstrates the parameter validation functionality
added to the EQFE simulation framework.
"""

import sys
import numpy as np
import warnings
from pathlib import Path

# Add EQFE modules to path
sys.path.append(str(Path(__file__).parent))

try:
    from simulations.core.field_simulator import ParameterValidator, EnvironmentalFieldSimulator
    print("✓ Successfully imported EQFE validation modules")
except ImportError as e:
    print(f"✗ Failed to import EQFE modules: {e}")
    print("Note: This is expected if running without the full EQFE installation")
    sys.exit(1)

def test_parameter_validation():
    """Test comprehensive parameter validation."""
    
    print("\n" + "="*50)
    print("EQFE Parameter Validation Test Suite")
    print("="*50)
    
    validator = ParameterValidator()
    
    # Test 1: Coupling strength validation
    print("\n1. Testing coupling strength validation:")
    print("-" * 40)
    
    valid_couplings = [0.01, 0.05, 0.1]
    for g in valid_couplings:
        try:
            g_validated = validator.validate_coupling_strength(g)
            print(f"  ✓ g = {g:.3f} → validated: {g_validated:.3f}")
        except Exception as e:
            print(f"  ✗ g = {g:.3f} → error: {e}")
    
    # Test invalid couplings
    invalid_couplings = [-0.1, 0.0, 0.5, 1.5]
    for g in invalid_couplings:
        try:
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                g_validated = validator.validate_coupling_strength(g)
                if w:
                    print(f"  ⚠ g = {g:.3f} → warning: {w[-1].message}")
                else:
                    print(f"  ✓ g = {g:.3f} → validated: {g_validated:.3f}")
        except Exception as e:
            print(f"  ✗ g = {g:.3f} → error: {e}")
    
    # Test 2: Temperature validation
    print("\n2. Testing temperature validation:")
    print("-" * 40)
    
    temperatures = [0.1, 1.0, 10.0, 300.0, -1.0, 0.0, 1e-10]
    for T in temperatures:
        try:
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                T_validated = validator.validate_temperature(T)
                if w:
                    print(f"  ⚠ T = {T:.2e} → warning: {w[-1].message}")
                else:
                    print(f"  ✓ T = {T:.2e} → validated: {T_validated:.2e}")
        except Exception as e:
            print(f"  ✗ T = {T:.2e} → error: {e}")
    
    # Test 3: Correlation time validation  
    print("\n3. Testing correlation time validation:")
    print("-" * 40)
    
    tau_c_values = [0.01, 1.0, 10.0, 1000.0, -1.0, 0.0, 1e-20]
    for tau_c in tau_c_values:
        try:
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                tau_c_validated = validator.validate_correlation_time(tau_c)
                if w:
                    print(f"  ⚠ τc = {tau_c:.2e} → warning: {w[-1].message}")
                else:
                    print(f"  ✓ τc = {tau_c:.2e} → validated: {tau_c_validated:.2e}")
        except Exception as e:
            print(f"  ✗ τc = {tau_c:.2e} → error: {e}")
    
    # Test 4: Phase parameter validation
    print("\n4. Testing phase parameter validation:")
    print("-" * 40)
    
    phases = [0.0, np.pi/4, np.pi, 2*np.pi, 4*np.pi, -np.pi, np.inf, np.nan]
    for phi in phases:
        try:
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                phi_validated = validator.validate_phase_parameter(phi)
                if w:
                    print(f"  ⚠ φ = {phi:.3f} → warning: {w[-1].message}")
                else:
                    print(f"  ✓ φ = {phi:.3f} → normalized: {phi_validated:.3f}")
        except Exception as e:
            print(f"  ✗ φ = {phi} → error: {e}")
    
    # Test 5: Time parameter validation
    print("\n5. Testing time parameter validation:")
    print("-" * 40)
    
    time_configs = [
        (0.0, 10.0, 0.1),    # Valid
        (0.0, 10.0, 0.01),   # Valid (small dt)
        (0.0, 10.0, 1.0),    # Valid (large dt, warning expected)
        (-1.0, 10.0, 0.1),   # Invalid start time
        (5.0, 2.0, 0.1),     # Invalid end < start
        (0.0, 10.0, -0.1),   # Invalid negative dt
        (0.0, 10.0, 15.0),   # Invalid dt > evolution time
    ]
    
    for t_start, t_end, dt in time_configs:
        try:
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                t_validated = validator.validate_time_parameters(t_start, t_end, dt)
                if w:
                    print(f"  ⚠ ({t_start}, {t_end}, {dt}) → warning: {w[-1].message}")
                else:
                    print(f"  ✓ ({t_start}, {t_end}, {dt}) → validated")
        except Exception as e:
            print(f"  ✗ ({t_start}, {t_end}, {dt}) → error: {e}")
    
    # Test 6: Parameter clamping
    print("\n6. Testing parameter clamping:")
    print("-" * 40)
    
    test_values = [-5.0, 0.5, 15.0]
    min_val, max_val = 0.0, 10.0
    
    for value in test_values:
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            clamped = validator.clamp_to_physical_range(
                value, min_val, max_val, "test_param"
            )
            if w:
                print(f"  ⚠ {value} → {clamped} (warning: {w[-1].message})")
            else:
                print(f"  ✓ {value} → {clamped} (no clamping needed)")

def test_field_simulator_validation():
    """Test validation in EnvironmentalFieldSimulator."""
    
    print("\n" + "="*50)
    print("Field Simulator Validation Test")
    print("="*50)
    
    # Test valid parameters
    print("\n1. Testing valid field simulator initialization:")
    try:
        simulator = EnvironmentalFieldSimulator(
            field_mass=1.0,
            coupling_strength=0.05,
            temperature=1.0,
            field_speed=2.998e8
        )
        print("  ✓ Valid parameters accepted")
    except Exception as e:
        print(f"  ✗ Valid parameters rejected: {e}")
    
    # Test invalid parameters
    print("\n2. Testing invalid field simulator parameters:")
    
    invalid_configs = [
        {"field_mass": -1.0, "coupling_strength": 0.05, "temperature": 1.0},
        {"field_mass": 1.0, "coupling_strength": -0.05, "temperature": 1.0},
        {"field_mass": 1.0, "coupling_strength": 0.05, "temperature": -1.0},
        {"field_mass": 1.0, "coupling_strength": 0.05, "temperature": 1.0, 
         "field_speed": 4e8},  # Faster than light
    ]
    
    for i, config in enumerate(invalid_configs):
        try:
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                simulator = EnvironmentalFieldSimulator(**config)
                if w:
                    print(f"  ⚠ Config {i+1}: Warning - {w[-1].message}")
                else:
                    print(f"  ? Config {i+1}: Unexpectedly accepted")
        except Exception as e:
            print(f"  ✓ Config {i+1}: Correctly rejected - {e}")

if __name__ == "__main__":
    # Run validation tests
    test_parameter_validation()
    test_field_simulator_validation()
    
    print("\n" + "="*50)
    print("Parameter Validation Test Complete")
    print("="*50)
    print("\nKey Features Demonstrated:")
    print("• Comprehensive input parameter validation")
    print("• Automatic parameter clamping to physical ranges")
    print("• Informative error messages for unphysical inputs")
    print("• Warning system for edge cases")
    print("• Integration with EQFE simulation framework")
    print("\nThe EQFE framework now includes robust parameter validation")
    print("to prevent unphysical simulations and guide users toward")
    print("physically meaningful parameter ranges.")
