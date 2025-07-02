# Environmental Quantum Field Effects - Configuration

# Default simulation parameters
DEFAULT_FIELD_MASS = 1e-6  # eV
DEFAULT_COUPLING = 1e-3  # dimensionless
DEFAULT_TEMPERATURE = 300.0  # Kelvin
DEFAULT_MEASUREMENT_TIME = 1e-6  # seconds

# Physical constants (SI units)
SPEED_OF_LIGHT = 2.99792458e8  # m/s
HBAR = 1.054571817e-34  # J⋅s
ELEMENTARY_CHARGE = 1.602176634e-19  # C
BOLTZMANN = 1.380649e-23  # J/K

# Quantum bounds
TSIRELSON_BOUND = 2.8284271247461903  # 2√2
CLASSICAL_BOUND = 2.0

# Numerical tolerances
PHYSICS_TOLERANCE = 1e-10
NUMERICAL_TOLERANCE = 1e-12
STATISTICAL_TOLERANCE = 0.1

# Simulation defaults
DEFAULT_N_TRIALS = 10000
DEFAULT_N_SAMPLES = 1000
MAX_INTEGRATION_TIME = 1e-2  # 10 ms

# Experimental parameters
DETECTION_EFFICIENCY = 0.8
DARK_COUNT_RATE = 100  # Hz
TIMING_RESOLUTION = 1e-9  # 1 ns

# Validation thresholds
MIN_ENHANCEMENT = 1.001  # Minimum detectable enhancement
MAX_ENHANCEMENT = 1.1  # Maximum realistic enhancement
ENHANCEMENT_SIGNIFICANCE = 3.0  # Sigma threshold
