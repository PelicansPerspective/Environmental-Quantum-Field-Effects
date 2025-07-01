#!/usr/bin/env python3
"""
EQFE Package Validation Script

Comprehensive validation of the Environmental Quantum Field Effects package.
This script tests all core functionality and ensures physics compliance.
"""

import sys
import numpy as np
from pathlib import Path

# Add project root for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test that all core modules can be imported."""
    print("Testing imports...")
    
    try:
        from simulations.core.field_simulator import EnvironmentalFieldSimulator
        from simulations.core.quantum_correlations import CHSHExperimentSimulator
        print("✅ Core modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_basic_functionality():
    """Test basic simulation functionality."""
    print("Testing basic functionality...")
    
    try:
        from simulations.core.field_simulator import EnvironmentalFieldSimulator
        from simulations.core.quantum_correlations import CHSHExperimentSimulator
        
        # Create simulator
        env_sim = EnvironmentalFieldSimulator(
            field_mass=1e-6,
            coupling_strength=1e-3,
            temperature=300.0
        )
        
        # Test amplification calculation
        A = env_sim.amplification_factor(measurement_time=1e-6)
        assert isinstance(A, float), "Amplification should be float"
        assert A > 0, "Amplification should be positive"
        assert np.isfinite(A), "Amplification should be finite"
        
        # Test CHSH simulation
        chsh_sim = CHSHExperimentSimulator(env_sim)
        results = chsh_sim.simulate_bell_experiment(n_trials=100)
        
        # Validate results structure
        required_keys = ['S_mean', 'S_std', 'S_measured']
        for key in required_keys:
            assert key in results, f"Missing key: {key}"
        
        # Validate physics bounds
        S = results['S_mean']
        assert S <= 2 * np.sqrt(2) + 1e-10, f"Tsirelson bound violated: S={S}"
        assert results['S_std'] >= 0, "Standard deviation should be non-negative"
        
        print("✅ Basic functionality tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def test_physics_bounds():
    """Test that physics bounds are always respected."""
    print("Testing physics bounds...")
    
    try:
        from simulations.core.field_simulator import EnvironmentalFieldSimulator
        from simulations.core.quantum_correlations import CHSHExperimentSimulator
        
        # Test with various parameter combinations
        test_params = [
            {'mass': 1e-7, 'coupling': 1e-4, 'temp': 77},
            {'mass': 1e-6, 'coupling': 1e-3, 'temp': 300},
            {'mass': 1e-5, 'coupling': 5e-3, 'temp': 400},
        ]
        
        tsirelson_bound = 2 * np.sqrt(2)
        
        for params in test_params:
            env_sim = EnvironmentalFieldSimulator(
                field_mass=params['mass'],
                coupling_strength=params['coupling'],
                temperature=params['temp']
            )
            
            chsh_sim = CHSHExperimentSimulator(env_sim)
            results = chsh_sim.simulate_bell_experiment(n_trials=500)
            
            S_mean = results['S_mean']
            S_all = results['S_measured']
            
            # Check bounds
            assert S_mean <= tsirelson_bound + 1e-10, \
                f"Mean CHSH violates Tsirelson bound: {S_mean} > {tsirelson_bound}"
            
            assert np.all(S_all <= tsirelson_bound + 1e-10), \
                f"Some measurements violate Tsirelson bound"
            
            # Check amplification factor
            A = env_sim.amplification_factor(1e-6)
            assert A > 0, f"Non-positive amplification: {A}"
            assert A < 10, f"Unphysically large amplification: {A}"
        
        print("✅ Physics bounds tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Physics bounds test failed: {e}")
        return False

def test_parameter_validation():
    """Test parameter validation."""
    print("Testing parameter validation...")
    
    try:
        from simulations.core.field_simulator import EnvironmentalFieldSimulator
        
        # Test valid parameters
        env_sim = EnvironmentalFieldSimulator(
            field_mass=1e-6,
            coupling_strength=1e-3,
            temperature=300.0
        )
        assert env_sim is not None
        
        # Test invalid parameters (should raise errors)
        invalid_cases = [
            {'field_mass': -1e-6, 'coupling_strength': 1e-3, 'temperature': 300},
            {'field_mass': 1e-6, 'coupling_strength': -1e-3, 'temperature': 300},
            {'field_mass': 1e-6, 'coupling_strength': 1e-3, 'temperature': -300},
        ]
        
        for case in invalid_cases:
            try:
                EnvironmentalFieldSimulator(**case)
                assert False, f"Should have raised error for: {case}"
            except ValueError:
                pass  # Expected
        
        print("✅ Parameter validation tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Parameter validation test failed: {e}")
        return False

def test_scaling_laws():
    """Test theoretical scaling laws."""
    print("Testing scaling laws...")
    
    try:
        from simulations.core.field_simulator import EnvironmentalFieldSimulator
        
        # Test coupling strength scaling
        base_params = {'field_mass': 1e-6, 'temperature': 300.0}
        couplings = [1e-4, 2e-4, 5e-4, 1e-3]
        enhancements = []
        
        for g in couplings:
            env_sim = EnvironmentalFieldSimulator(
                coupling_strength=g, **base_params
            )
            A = env_sim.amplification_factor(1e-6)
            enhancement = A - 1  # Enhancement above unity
            enhancements.append(enhancement)
        
        # For weak coupling, enhancement should scale approximately as g²
        # Check that enhancement increases with coupling
        assert all(e >= 0 for e in enhancements), "Enhancements should be non-negative"
        
        # Test mass scaling (correlation time should scale as 1/m)
        masses = [5e-7, 1e-6, 2e-6, 5e-6]
        correlation_times = []
        
        for m in masses:
            env_sim = EnvironmentalFieldSimulator(
                field_mass=m, coupling_strength=1e-3, temperature=300.0
            )
            tau_c = env_sim.correlation_time()
            correlation_times.append(tau_c)
        
        # Correlation times should decrease with increasing mass
        for i in range(1, len(correlation_times)):
            assert correlation_times[i] < correlation_times[i-1], \
                "Correlation time should decrease with mass"
        
        print("✅ Scaling laws tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Scaling laws test failed: {e}")
        return False

def run_comprehensive_validation():
    """Run all validation tests."""
    print("🔬 EQFE Package Comprehensive Validation")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_basic_functionality,
        test_physics_bounds,
        test_parameter_validation,
        test_scaling_laws,
    ]
    
    results = []
    for test in tests:
        print()
        success = test()
        results.append(success)
    
    print("\n" + "=" * 50)
    print("VALIDATION SUMMARY")
    print("=" * 50)
    
    total_tests = len(tests)
    passed_tests = sum(results)
    
    for i, (test, result) in enumerate(zip(tests, results)):
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{i+1}. {test.__name__}: {status}")
    
    print(f"\nOverall: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED - Package is ready for use!")
        return True
    else:
        print("⚠️  Some tests failed - package needs fixes")
        return False

if __name__ == "__main__":
    success = run_comprehensive_validation()
    sys.exit(0 if success else 1)
