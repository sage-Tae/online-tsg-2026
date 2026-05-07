"""
Configuration constants for the Online TSG experiments.

Defines the dimensionless framework per phase1_design.md (Phase 1 Design Doc):
- N2 normalization: L = sqrt(n), speed = 1, density = 1 per unit area
- Load parameter: rho = (L/v) / tau
- Pattern taxonomy: rho-based (B_heavy/B_medium/B_light replacing B1/B2/B5)
"""

import math


# ============================================================
# Physical / Dimensional Constants
# ============================================================

# Beardwood-Halton-Hammersley constant for 2D Euclidean TSP
# Under N2 convention (density = 1), this yields avg inter-customer
# travel time ~= BETA_BHH (independent of n).
BETA_BHH = 0.7124  # empirical value from literature

# Unit vehicle speed (distance per time)
DEFAULT_SPEED = 1.0

# Depot location (fixed in all experiments)
DEPOT = (0.0, 0.0)


# ============================================================
# N2 Normalization
# ============================================================

def L_N2(n):
    """Square side length under N2 convention: L = sqrt(n).

    This fixes customer density at 1 per unit area, following
    Steele (1997, Probability Theory and Combinatorial Optimization).
    """
    return math.sqrt(n)


def tau_from_rho(rho, base_travel=BETA_BHH):
    """Compute mean inter-arrival interval from load parameter rho.

    rho = (characteristic travel time) / (mean arrival interval)
    => tau = base_travel / rho

    base_travel defaults to BETA_BHH because under N2, avg travel time
    between two uniform customers is ~= BETA_BHH (n-independent).
    """
    if rho == float('inf'):
        return 0.0  # simultaneous arrivals
    return base_travel / rho


# ============================================================
# Pattern Taxonomy (rho-based)
# ============================================================

# Seven arrival patterns spanning the rho spectrum.
# Each entry: (new_name, structure_type, rho)
PATTERN_RHO = {
    'A':        float('inf'),  # simultaneous, k = n
    'B_heavy':  4.0,           # sequential, queue piles up
    'B_medium': 2.0,           # sequential, balanced
    'B_light':  0.5,           # sequential, queue drains
    'C':        2.0,           # clustered (2 batches), interleaved
    'D':        1.0,           # reverse zig-zag (worst-case NN)
    'E':        1.0,           # Poisson random
}

PATTERN_STRUCTURE = {
    'A':        'simultaneous',
    'B_heavy':  'sequential_uniform',
    'B_medium': 'sequential_uniform',
    'B_light':  'sequential_uniform',
    'C':        'clustered_interleave',
    'D':        'reverse_zigzag',
    'E':        'poisson_random',
}

# Mapping from old pattern names (previous paper) to new (for legacy data)
OLD_TO_NEW_PATTERN = {
    'A':  'A',
    'B1': 'B_heavy',
    'B2': 'B_medium',
    'B5': 'B_light',
    'C':  'C',
    'D':  'D',
    'E':  'E',
}

# Canonical ordering for tables/figures
PATTERN_ORDER = ['A', 'B_heavy', 'B_medium', 'B_light', 'C', 'D', 'E']


# ============================================================
# Experimental Grid
# ============================================================

# Main study
DEFAULT_N_VALUES = [5, 7, 10, 12, 15]
DEFAULT_SEEDS = [7, 42, 99, 123, 256]
DEFAULT_POLICIES = ['nearest_neighbor', 'cheapest_insertion', 'batch_reoptimize']

# Scale-up study
SCALEUP_N_VALUES = [20, 30, 50]
SCALEUP_PATTERNS = ['A', 'B_medium', 'C']

# Sensitivity (scale invariance verification, Appendix B)
SENSITIVITY_ALPHAS = [0.5, 1.0, 2.0, 5.0]
SENSITIVITY_N_VALUES = [10, 20]
SENSITIVITY_PATTERNS = ['B_heavy', 'B_medium', 'C']
SENSITIVITY_SEED = 42  # single seed for sensitivity study


# ============================================================
# Utility
# ============================================================

def get_pattern_params(pattern_name):
    """Return (rho, tau, structure) for a given pattern name."""
    rho = PATTERN_RHO[pattern_name]
    tau = tau_from_rho(rho)
    structure = PATTERN_STRUCTURE[pattern_name]
    return rho, tau, structure


def describe_pattern(pattern_name):
    """Human-readable description for logging/debugging."""
    rho, tau, structure = get_pattern_params(pattern_name)
    return f"{pattern_name}: rho={rho}, tau={tau:.3f}, structure={structure}"
