#!/usr/bin/env python3
"""
Quick EQFE Test - Minimal validation script
"""

import sys
from pathlib import Path

# Add project to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def main():
    print("🔬 Quick EQFE Test")
    print("=" * 20)

    try:
        # Import core modules
        from simulations.core.field_simulator import (
            EnvironmentalFieldSimulator,
        )
        from simulations.core.quantum_correlations import (
            CHSHExperimentSimulator,
        )

        print("✅ Imports successful")

        # Create basic simulator
        env_sim = EnvironmentalFieldSimulator(
            field_mass=1e-6, coupling_strength=1e-3, temperature=300.0
        )
        print("✅ Environmental simulator created")

        # Test amplification
        A = env_sim.amplification_factor(1e-6)
        print(f"✅ Amplification factor: {A:.6f}")

        # Test CHSH simulation
        chsh_sim = CHSHExperimentSimulator(env_sim)
        results = chsh_sim.simulate_bell_experiment(n_trials=1000)

        S = results["S_mean"]
        S_std = results["S_std"]

        print(f"✅ CHSH parameter: {S:.4f} ± {S_std:.4f}")
        print(f"   Tsirelson bound: {2**(0.5)*2:.4f}")
        print(f"   Classical bound: 2.0000")

        # Physics validation
        if S <= 2 ** (0.5) * 2 + 1e-10:
            print("✅ Tsirelson bound respected")
        else:
            print("❌ Tsirelson bound violated!")

        if S > 2.0:
            print("✅ Bell inequality violated (quantum behavior)")
        else:
            print("⚠️  No Bell violation detected")

        print("\n🎉 Quick test completed successfully!")
        print("\nNext steps:")
        print("- Run: python examples/basic_demo.py")
        print("- Run: python validate_package.py")
        print("- Check: docs/getting_started.md")

        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
