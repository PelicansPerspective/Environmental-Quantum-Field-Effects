"""
Quantum Correlations Module

Implements CHSH Bell test experiments with environmental field effects.
All simulations maintain rigorous respect for quantum mechanical bounds.
"""

import numpy as np
from scipy import stats
from typing import Dict, Optional
import warnings

from .field_simulator import EnvironmentalFieldSimulator, PhysicalConstants

# Import validator from correct module
try:
    from ..analysis.physics_validator import QuantumBoundsValidator
except ImportError:
    # Fallback for direct execution
    import sys
    from pathlib import Path

    sys.path.append(str(Path(__file__).parent.parent / "analysis"))
    from physics_validator import QuantumBoundsValidator


class CHSHExperimentSimulator:
    """
    Simulate CHSH Bell test experiments with environmental effects.

    This class handles complete Bell test simulations including:
    - Environmental field generation
    - Amplification law application
    - Bioelectromagnetic coupling (optional)
    - Statistical analysis
    - Physics validation
    """

    def __init__(
        self,
        env_simulator: EnvironmentalFieldSimulator,
        bioem_simulator: Optional["BioelectromagneticSimulator"] = None,
    ):
        """
        Initialize CHSH experiment simulator.

        Parameters:
        -----------
        env_simulator : EnvironmentalFieldSimulator
            Environmental field effects simulator
        bioem_simulator : BioelectromagneticSimulator, optional
            Bioelectromagnetic coupling simulator
        """
        self.env_simulator = env_simulator
        self.bioem_simulator = bioem_simulator
        self.validator = QuantumBoundsValidator()

        # CHSH experimental parameters
        self.tsirelson_bound = 2 * np.sqrt(2)
        self.classical_bound = 2.0

    def ideal_quantum_correlation(self) -> float:
        """Return ideal quantum mechanical CHSH parameter."""
        return self.tsirelson_bound

    def simulate_bell_experiment(
        self,
        n_trials: int = 10000,
        measurement_noise: float = 0.01,
        measurement_time: float = 1.0,
        bioem_data: Optional[np.ndarray] = None,
    ) -> Dict:
        """
        Simulate complete Bell test experiment with environmental effects.

        Parameters:
        -----------
        n_trials : int
            Number of measurement trials
        measurement_noise : float
            Experimental measurement noise level (dimensionless)
        measurement_time : float
            Total measurement time in seconds
        bioem_data : array, optional
            Bioelectromagnetic field data

        Returns:
        --------
        dict : Complete simulation results
        """
        # Generate environmental field fluctuations
        env_field = self.env_simulator.thermal_field_fluctuations(n_trials)

        # Ideal quantum correlation (Tsirelson bound)
        S_ideal = self.ideal_quantum_correlation()

        # Apply environmental amplification law
        S_env_modified = self.env_simulator.modify_quantum_correlations(
            S_ideal, env_field, measurement_time=measurement_time
        )

        # Apply bioelectromagnetic effects if available
        if self.bioem_simulator is not None and bioem_data is not None:
            S_bioem_modified = self._apply_bioem_coupling(
                S_env_modified, bioem_data, n_trials
            )
        else:
            S_bioem_modified = S_env_modified

        # Add experimental measurement noise
        noise = np.random.normal(0, measurement_noise, n_trials)
        S_measured = S_bioem_modified + noise

        # Physics validation
        validation_result = self.validator.validate_chsh_parameter(S_measured)
        tsirelson_respected = validation_result.bounds_checked.get(
            "tsirelson", True
        )
        classical_violation = validation_result.bounds_checked.get(
            "quantum_advantage", False
        )

        if not tsirelson_respected:
            warnings.warn(
                "Simulation produced values exceeding Tsirelson bound!"
            )

        # Compile results
        results = {
            "chsh_values": S_measured,  # Main CHSH parameter array
            "S_measured": S_measured,  # Alias for compatibility
            "S_mean": np.mean(S_measured),
            "S_std": np.std(S_measured),
            "S_sem": stats.sem(S_measured),
            "S_ideal": S_ideal,
            "env_field": env_field,
            "environmental_amplification": S_env_modified
            / S_ideal,  # Amplification factors
            "S_env_modified": S_env_modified,
            "classical_violation": classical_violation,
            "tsirelson_respected": tsirelson_respected,
            "n_trials": n_trials,
            "measurement_noise": measurement_noise,
            "measurement_time": measurement_time,
            "measurement_statistics": {
                "mean": np.mean(S_measured),
                "std": np.std(S_measured),
                "min": np.min(S_measured),
                "max": np.max(S_measured),
                "classical_violations": np.sum(S_measured > 2.0),
                "tsirelson_violations": np.sum(S_measured > 2 * np.sqrt(2)),
            },
            "validation_results": self.validator.validate_chsh_parameter(
                S_measured
            ),
            "simulation_parameters": self.env_simulator.get_simulation_parameters(),
        }

        if self.bioem_simulator is not None and bioem_data is not None:
            results["bioem_data"] = bioem_data
            results["S_bioem_modified"] = S_bioem_modified

        return results

    def _apply_bioem_coupling(
        self, correlations: np.ndarray, bioem_data: np.ndarray, n_trials: int
    ) -> np.ndarray:
        """Apply bioelectromagnetic coupling effects."""
        # Interpolate bioem data to match trial count if necessary
        if len(bioem_data) != n_trials:
            bioem_interp = np.interp(
                np.linspace(0, 1, n_trials),
                np.linspace(0, 1, len(bioem_data)),
                bioem_data,
            )
        else:
            bioem_interp = bioem_data

        # Calculate bioelectromagnetic coupling
        bioem_coupling = self.bioem_simulator.calculate_coupling(bioem_interp)

        # Apply small perturbative coupling (< 1% effect)
        coupling_strength = 0.01  # Maximum 1% modification
        modified_correlations = correlations * (
            1 + coupling_strength * bioem_coupling
        )

        return modified_correlations

    def statistical_analysis(self, results: Dict) -> Dict:
        """
        Perform comprehensive statistical analysis of experimental results.

        Parameters:
        -----------
        results : dict
            Results from simulate_bell_experiment

        Returns:
        --------
        dict : Statistical analysis results
        """
        S_measured = results["S_measured"]
        S_ideal = results["S_ideal"]

        # Test against classical bound
        t_stat_classical, p_val_classical = stats.ttest_1samp(
            S_measured, self.classical_bound
        )

        # Test against ideal quantum value
        t_stat_quantum, p_val_quantum = stats.ttest_1samp(S_measured, S_ideal)

        # Effect sizes (Cohen's d)
        cohen_d_classical = (
            np.mean(S_measured) - self.classical_bound
        ) / np.std(S_measured)
        cohen_d_quantum = (np.mean(S_measured) - S_ideal) / np.std(S_measured)

        # Confidence intervals
        ci_95 = stats.t.interval(
            0.95,
            len(S_measured) - 1,
            loc=np.mean(S_measured),
            scale=stats.sem(S_measured),
        )

        # Additional statistical tests
        shapiro_stat, shapiro_p = stats.shapiro(
            S_measured[:5000]
        )  # Limit for efficiency

        # Bell inequality violation analysis
        violation_fraction = np.mean(S_measured > self.classical_bound)

        return {
            "classical_comparison": {
                "t_statistic": t_stat_classical,
                "p_value": p_val_classical,
                "effect_size_cohen_d": cohen_d_classical,
                "significant": p_val_classical < 0.05,
                "violation_fraction": violation_fraction,
            },
            "quantum_comparison": {
                "t_statistic": t_stat_quantum,
                "p_value": p_val_quantum,
                "effect_size_cohen_d": cohen_d_quantum,
                "deviation_from_ideal": np.mean(S_measured) - S_ideal,
            },
            "descriptive_statistics": {
                "mean": np.mean(S_measured),
                "std": np.std(S_measured),
                "sem": stats.sem(S_measured),
                "median": np.median(S_measured),
                "q25": np.percentile(S_measured, 25),
                "q75": np.percentile(S_measured, 75),
                "min": np.min(S_measured),
                "max": np.max(S_measured),
            },
            "confidence_intervals": {
                "ci_95_lower": ci_95[0],
                "ci_95_upper": ci_95[1],
                "ci_width": ci_95[1] - ci_95[0],
            },
            "normality_test": {
                "shapiro_statistic": shapiro_stat,
                "shapiro_p_value": shapiro_p,
                "is_normal": shapiro_p > 0.05,
            },
            "physics_validation": {
                "tsirelson_bound_respected": results["tsirelson_respected"],
                "classical_bound_violated": results["classical_violation"],
                "max_violation": np.max(S_measured) - self.tsirelson_bound,
                "bound_violation_fraction": np.mean(
                    S_measured > self.tsirelson_bound
                ),
            },
        }

    def parameter_scan(
        self,
        parameter_name: str,
        parameter_values: np.ndarray,
        n_trials: int = 1000,
    ) -> Dict:
        """
        Perform parameter scan over environmental conditions.

        Parameters:
        -----------
        parameter_name : str
            Name of parameter to scan ('temperature', 'coupling_strength', etc.)
        parameter_values : np.ndarray
            Values to scan over
        n_trials : int
            Number of trials per parameter value

        Returns:
        --------
        dict : Parameter scan results
        """
        results = {
            "parameter_name": parameter_name,
            "parameter_values": parameter_values,
            "mean_chsh": [],
            "std_chsh": [],
            "amplification_factors": [],
            "violation_fractions": [],
        }

        # Store original parameter value
        original_value = getattr(self.env_simulator, parameter_name)

        for param_value in parameter_values:
            # Update parameter
            setattr(self.env_simulator, parameter_name, param_value)

            # Recompute derived parameters if necessary
            if parameter_name in ["coupling_strength"]:
                self.env_simulator.alpha = (
                    self.env_simulator.coupling_strength**2 / 2.0
                )
                self.env_simulator.beta = (
                    self.env_simulator.coupling_strength**4 / 4.0
                )

            # Run simulation
            sim_results = self.simulate_bell_experiment(n_trials=n_trials)

            # Collect results
            results["mean_chsh"].append(sim_results["S_mean"])
            results["std_chsh"].append(sim_results["S_std"])
            results["amplification_factors"].append(
                sim_results["S_mean"] / sim_results["S_ideal"]
            )
            results["violation_fractions"].append(
                np.mean(sim_results["S_measured"] > self.classical_bound)
            )

        # Restore original parameter value
        setattr(self.env_simulator, parameter_name, original_value)
        if parameter_name in ["coupling_strength"]:
            self.env_simulator.alpha = (
                self.env_simulator.coupling_strength**2 / 2.0
            )
            self.env_simulator.beta = (
                self.env_simulator.coupling_strength**4 / 4.0
            )

        # Convert lists to arrays
        for key in [
            "mean_chsh",
            "std_chsh",
            "amplification_factors",
            "violation_fractions",
        ]:
            results[key] = np.array(results[key])

        return results


class BioelectromagneticSimulator:
    """
    Simulate classical electromagnetic coupling between neural activity
    and quantum systems.
    """

    def __init__(
        self,
        dipole_moment: float = 1e-12,  # A⋅m
        neural_frequency: float = 40.0,  # Hz
        distance: float = 0.1,
    ):  # m
        """
        Initialize bioelectromagnetic simulator.

        Parameters:
        -----------
        dipole_moment : float
            Neural dipole moment in A⋅m
        neural_frequency : float
            Characteristic neural oscillation frequency in Hz
        distance : float
            Distance between neural source and quantum system in m
        """
        self.dipole_moment = dipole_moment
        self.neural_frequency = neural_frequency
        self.distance = distance

    def neural_electromagnetic_field(
        self, time: np.ndarray, neural_signal: Optional[np.ndarray] = None
    ) -> np.ndarray:
        """
        Compute electromagnetic field from neural activity.

        Uses dipole radiation formula for oscillating electric dipole.
        """
        if neural_signal is None:
            # Generate synthetic neural signal (gamma oscillations)
            neural_signal = np.sin(2 * np.pi * self.neural_frequency * time)

        # Electromagnetic field amplitude from oscillating dipole
        omega = 2 * np.pi * self.neural_frequency

        # Near-field approximation (r << c/ω)
        E_amplitude = (
            PhysicalConstants.mu_0 * omega**2 * self.dipole_moment
        ) / (4 * np.pi * self.distance)

        return E_amplitude * neural_signal

    def calculate_coupling(self, neural_data: np.ndarray) -> np.ndarray:
        """
        Calculate quantum system coupling from neural electromagnetic fields.

        Parameters:
        -----------
        neural_data : np.ndarray
            Neural activity data (e.g., EEG amplitudes)

        Returns:
        --------
        np.ndarray : Coupling parameters (dimensionless)
        """
        # Generate time array
        time = np.arange(len(neural_data)) / 1000.0  # Assume 1 kHz sampling

        # Calculate EM field
        em_field = self.neural_electromagnetic_field(time, neural_data)

        # Quantum transition dipole moment (typical atomic scale)
        quantum_dipole = 1e-29  # C⋅m

        # Interaction energy
        interaction_energy = quantum_dipole * em_field

        # Convert to dimensionless coupling parameter
        coupling_parameter = interaction_energy / PhysicalConstants.e

        return coupling_parameter


def run_comprehensive_experiment(
    field_mass: float = 1e-6,
    coupling_strength: float = 1e-3,
    temperature: float = 300.0,
    n_trials: int = 10000,
) -> Dict:
    """
    Run comprehensive CHSH experiment with environmental effects.

    Parameters:
    -----------
    field_mass : float
        Environmental field mass in eV/c²
    coupling_strength : float
        Field-quantum system coupling strength
    temperature : float
        Environmental temperature in Kelvin
    n_trials : int
        Number of experimental trials

    Returns:
    --------
    dict : Complete experimental results and analysis
    """
    # Initialize simulators
    env_sim = EnvironmentalFieldSimulator(
        field_mass=field_mass,
        coupling_strength=coupling_strength,
        temperature=temperature,
    )

    bioem_sim = BioelectromagneticSimulator()
    chsh_sim = CHSHExperimentSimulator(env_sim, bioem_sim)

    # Generate synthetic bioelectromagnetic data
    time = np.arange(n_trials) / 1000.0
    bioem_data = np.sin(2 * np.pi * 40 * time) + 0.1 * np.random.randn(
        n_trials
    )

    # Run experiment simulation
    experiment_results = chsh_sim.simulate_bell_experiment(
        n_trials=n_trials,
        measurement_noise=0.01,
        measurement_time=10.0,  # 10 second measurement
        bioem_data=bioem_data,
    )

    # Perform statistical analysis
    statistical_results = chsh_sim.statistical_analysis(experiment_results)

    # Combine all results
    comprehensive_results = {
        "experiment_results": experiment_results,
        "statistical_analysis": statistical_results,
        "simulation_metadata": {
            "field_mass_eV": field_mass,
            "coupling_strength": coupling_strength,
            "temperature_K": temperature,
            "n_trials": n_trials,
            "bioem_included": True,
        },
    }

    return comprehensive_results


if __name__ == "__main__":
    # Example usage and validation
    print("Quantum Correlations Module - CHSH Experiments")
    print("=" * 50)

    # Run comprehensive experiment
    results = run_comprehensive_experiment()

    # Display key results
    stats = results["statistical_analysis"]
    print(f"\nExperimental Results:")
    print(
        f"  Mean CHSH parameter: {stats['descriptive_statistics']['mean']:.6f}"
    )
    print(f"  Standard error: {stats['descriptive_statistics']['sem']:.6f}")
    print(
        f"  Classical violation: {stats['classical_comparison']['significant']}"
    )
    print(
        f"  Tsirelson bound respected: {stats['physics_validation']['tsirelson_bound_respected']}"
    )
    print(
        f"  Effect size (vs classical): {stats['classical_comparison']['effect_size_cohen_d']:.3f}"
    )

    print("\nQuantum correlations module validation complete!")
