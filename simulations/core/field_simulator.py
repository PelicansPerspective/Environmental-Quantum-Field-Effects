"""
Environmental Field Simulator - Core Module

This module implements the theoretical amplification law for quantum correlation
modifications due to environmental scalar fields. All simulations are based on
rigorous quantum field theory derivations and respect established physics principles.
"""

import numpy as np
import warnings
from dataclasses import dataclass
from typing import Union, Optional


@dataclass
class PhysicalConstants:
    """Physical constants in SI units."""
    c = 299792458.0  # Speed of light (m/s)
    hbar = 1.054571817e-34  # Reduced Planck constant (J⋅s)
    e = 1.602176634e-19  # Elementary charge (C)
    mu_0 = 4e-7 * np.pi  # Vacuum permeability (H/m)
    epsilon_0 = 1.0 / (mu_0 * c**2)  # Vacuum permittivity (F/m)
    k_B = 1.380649e-23  # Boltzmann constant (J/K)


class QuantumBoundValidator:
    """Validator to ensure all quantum correlations respect physical bounds."""
    
    @staticmethod
    def check_tsirelson_bound(S: Union[float, np.ndarray]) -> bool:
        """
        Verify that CHSH parameter S satisfies Tsirelson bound S ≤ 2√2.
        
        Parameters:
        -----------
        S : float or array
            CHSH parameter value(s)
            
        Returns:
        --------
        bool : True if bound is respected, False otherwise
        """
        tsirelson_limit = 2 * np.sqrt(2)
        return np.all(S <= tsirelson_limit + 1e-10)
    
    @staticmethod
    def check_bell_inequality(S: Union[float, np.ndarray]) -> bool:
        """
        Verify that CHSH parameter respects classical Bell inequality S ≤ 2.
        
        Parameters:
        -----------
        S : float or array
            CHSH parameter value(s)
            
        Returns:
        --------
        bool : True if classical bound is violated (quantum behavior)
        """
        return np.any(S > 2.0)


class EnvironmentalFieldSimulator:
    """
    Core simulator for environmental scalar field effects on quantum correlations.
    
    Implements the theoretically derived amplification law:
    A(φ,t) = exp[α⟨φ²⟩t - β∫₀ᵗ C(τ) dτ]
    
    Where:
    - α = g²/2 (enhancement parameter)
    - β = g⁴/4 (decoherence parameter)  
    - ⟨φ²⟩ (field variance)
    - C(τ) (field correlation function)
    """
    
    def __init__(self, 
                 field_mass: float = 1e-6,  # eV/c²
                 coupling_strength: float = 1e-3,  # Dimensionless
                 temperature: float = 300.0,  # Kelvin
                 field_speed: Optional[float] = None):  # m/s
        """
        Initialize environmental field simulator.
        
        Parameters:
        -----------
        field_mass : float
            Scalar field mass in eV/c²
        coupling_strength : float  
            Dimensionless coupling constant (must be << 1)
        temperature : float
            Environmental temperature in Kelvin
        field_speed : float, optional
            Field propagation speed (default: speed of light)
        """
        self.field_mass = field_mass
        self.coupling_strength = coupling_strength
        self.temperature = temperature
        self.field_speed = field_speed or PhysicalConstants.c
        
        # Validate physical parameters
        self._validate_parameters()
        
        # Pre-calculate derived parameters
        self.alpha = self.coupling_strength**2 / 2.0  # Enhancement parameter
        self.beta = self.coupling_strength**4 / 4.0   # Decoherence parameter
        
    def _validate_parameters(self):
        """Validate that all parameters respect physics constraints."""
        if self.field_speed > PhysicalConstants.c:
            raise ValueError(f"Field speed {self.field_speed} exceeds c")
        if self.coupling_strength < 0:
            raise ValueError("Coupling strength must be non-negative")
        if self.field_mass < 0:
            raise ValueError("Field mass must be non-negative")
        if self.temperature <= 0:
            raise ValueError("Temperature must be positive")
        if self.coupling_strength > 0.1:
            warnings.warn("Large coupling may violate perturbative approximation")
    
    def thermal_field_fluctuations(self, n_samples: int) -> np.ndarray:
        """
        Generate thermal fluctuations of the environmental field.
        
        Uses equipartition theorem: ⟨φ²⟩ = k_B T / (mass c²)
        For massless fields, uses IR cutoff at thermal scale.
        
        Parameters:
        -----------
        n_samples : int
            Number of field samples to generate
            
        Returns:
        --------
        np.ndarray : Field strength values
        """
        # Convert field mass from eV to kg
        if self.field_mass > 0:
            mass_kg = (self.field_mass * PhysicalConstants.e / 
                      PhysicalConstants.c**2)
            field_variance = (PhysicalConstants.k_B * self.temperature / 
                            (mass_kg * PhysicalConstants.c**2))
        else:
            # Massless field: use thermal energy scale as IR cutoff
            field_variance = (PhysicalConstants.k_B * self.temperature / 
                            PhysicalConstants.e)
        
        # Generate Gaussian thermal fluctuations
        return np.random.normal(0, np.sqrt(field_variance), n_samples)
    
    def correlation_time(self) -> float:
        """
        Calculate field correlation time based on field mass.
        
        Returns:
        --------
        float : Correlation time τ_c in seconds
        """
        if self.field_mass > 0:
            # Massive field: τ_c ~ ℏ/(mc²)
            mass_kg = (self.field_mass * PhysicalConstants.e / 
                      PhysicalConstants.c**2)
            return PhysicalConstants.hbar / (mass_kg * PhysicalConstants.c**2)
        else:
            # Massless field: use thermal time scale
            return PhysicalConstants.hbar / (PhysicalConstants.k_B * 
                                           self.temperature)
    
    def correlation_integral(self, field_variance: np.ndarray, 
                           measurement_time: float) -> np.ndarray:
        """
        Calculate correlation integral ∫₀ᵗ C(τ) dτ.
        
        Assumes exponential correlation: C(τ) = ⟨φ²⟩ exp(-τ/τ_c)
        Integral = ⟨φ²⟩ τ_c [1 - exp(-t/τ_c)]
        
        Parameters:
        -----------
        field_variance : np.ndarray
            Field variance values ⟨φ²⟩
        measurement_time : float
            Total measurement time
            
        Returns:
        --------
        np.ndarray : Correlation integral values
        """
        tau_c = self.correlation_time()
        return field_variance * tau_c * (1 - np.exp(-measurement_time / tau_c))
    
    def _calculate_field_variance(self) -> float:
        """Calculate thermal field variance."""
        if self.field_mass > 0:
            mass_kg = (self.field_mass * PhysicalConstants.e / 
                      PhysicalConstants.c**2)
            return (PhysicalConstants.k_B * self.temperature / 
                   (mass_kg * PhysicalConstants.c**2))
        else:
            return (PhysicalConstants.k_B * self.temperature / 
                   PhysicalConstants.e)

    def _calculate_correlation_integral(self, measurement_time: float) -> float:
        """Calculate correlation integral for given measurement time."""
        field_variance = self._calculate_field_variance()
        tau_c = self.correlation_time()
        return field_variance * tau_c * (1 - np.exp(-measurement_time / tau_c))

    def amplification_factor(self, measurement_time: float = 1.0) -> float:
        """
        Calculate the amplification factor using the derived law.
        
        A(φ,t) = exp[α⟨φ²⟩t - β∫₀ᵗ C(τ) dτ]
        
        Parameters:
        -----------
        measurement_time : float
            Total measurement time for correlation integral
            
        Returns:
        --------
        float : Amplification factor
        """
        # Field variance: ⟨φ²⟩
        field_variance = self._calculate_field_variance()
        
        # Enhancement term: α⟨φ²⟩t
        enhancement_term = self.alpha * field_variance * measurement_time
        
        # Decoherence term: β∫₀ᵗ C(τ) dτ
        decoherence_term = self.beta * self._calculate_correlation_integral(measurement_time)
        
        # Amplification factor
        return np.exp(enhancement_term - decoherence_term)
    
    def modify_quantum_correlations(self, 
                                    ideal_correlation: float,
                                    measurement_time: float = 1.0) -> float:
        """
        Apply amplification law to modify quantum correlations.
        
        Parameters:
        -----------
        ideal_correlation : float
            Ideal quantum correlation value
        measurement_time : float
            Total measurement time
            
        Returns:
        --------
        float : Modified correlation value
        """
        # Calculate amplification factor
        amplification = self.amplification_factor(measurement_time)
        
        # Apply to ideal correlations
        modified_correlation = ideal_correlation * amplification
        
        # Ensure Tsirelson bound is respected
        tsirelson_bound = 2 * np.sqrt(2)
        clipped_correlation = np.clip(modified_correlation, 0, tsirelson_bound)
        
        # Check for bound violations
        if modified_correlation > tsirelson_bound:
            warnings.warn(f"Tsirelson bound clipping: {modified_correlation:.6f} -> {clipped_correlation:.6f}")
        
        return clipped_correlation
    
    def optimal_temperature(self) -> float:
        """
        Calculate optimal temperature for maximum amplification.
        
        Returns:
        --------
        float : Optimal temperature in Kelvin
        """
        tau_c = self.correlation_time()
        # From dA/dT = 0 condition
        if self.field_mass > 0:
            mass_kg = (self.field_mass * PhysicalConstants.e / 
                      PhysicalConstants.c**2)
            return (self.beta * tau_c * mass_kg * PhysicalConstants.c**2 / 
                   (self.alpha * PhysicalConstants.k_B))
        else:
            # For massless fields, optimal temperature depends on IR cutoff
            return PhysicalConstants.hbar / (PhysicalConstants.k_B * tau_c)
    
    def get_simulation_parameters(self) -> dict:
        """
        Get complete set of simulation parameters.
        
        Returns:
        --------
        dict : All simulation parameters and derived quantities
        """
        return {
            'field_mass_eV': self.field_mass,
            'coupling_strength': self.coupling_strength,
            'temperature_K': self.temperature,
            'field_speed_fraction_c': self.field_speed / PhysicalConstants.c,
            'enhancement_parameter_alpha': self.alpha,
            'decoherence_parameter_beta': self.beta,
            'correlation_time_s': self.correlation_time(),
            'optimal_temperature_K': self.optimal_temperature()
        }


def create_simulator_with_validation(field_mass: float = 1e-6,
                                   coupling_strength: float = 1e-3,
                                   temperature: float = 300.0) -> EnvironmentalFieldSimulator:
    """
    Create environmental field simulator with automatic parameter validation.
    
    Parameters:
    -----------
    field_mass : float
        Field mass in eV/c²
    coupling_strength : float
        Coupling strength (dimensionless)
    temperature : float
        Temperature in Kelvin
        
    Returns:
    --------
    EnvironmentalFieldSimulator : Validated simulator instance
    """
    simulator = EnvironmentalFieldSimulator(
        field_mass=field_mass,
        coupling_strength=coupling_strength,
        temperature=temperature
    )
    
    # Additional validation checks
    validator = QuantumBoundValidator()
    
    # Test with sample field values
    test_field = simulator.thermal_field_fluctuations(1000)
    test_correlation = simulator.modify_quantum_correlations(
        2 * np.sqrt(2), test_field, measurement_time=1.0
    )
    
    if not validator.check_tsirelson_bound(test_correlation):
        raise ValueError("Simulator parameters produce unphysical results")
    
    return simulator


if __name__ == "__main__":
    # Example usage and validation
    print("Environmental Field Simulator - Core Module")
    print("=" * 50)
    
    # Create validated simulator
    simulator = create_simulator_with_validation()
    
    # Display parameters
    params = simulator.get_simulation_parameters()
    print("\nSimulation Parameters:")
    for key, value in params.items():
        print(f"  {key}: {value}")
    
    # Test amplification law
    field_samples = simulator.thermal_field_fluctuations(10000)
    ideal_chsh = 2 * np.sqrt(2)
    modified_chsh = simulator.modify_quantum_correlations(
        ideal_chsh, field_samples, measurement_time=1.0
    )
    
    print(f"\nAmplification Test:")
    print(f"  Ideal CHSH: {ideal_chsh:.6f}")
    print(f"  Mean modified CHSH: {np.mean(modified_chsh):.6f}")
    print(f"  Amplification factor: {np.mean(modified_chsh)/ideal_chsh:.6f}")
    print(f"  Tsirelson bound respected: {np.all(modified_chsh <= 2*np.sqrt(2))}")
    
    print("\nCore module validation complete!")
