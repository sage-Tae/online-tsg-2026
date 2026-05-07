"""
Customer position and arrival time generators for Online TSG experiments.

Implements the N2 dimensionless framework per phase1_design.md:
- generate_customers: uniform sampling in [0, L]^2 with L = sqrt(n) (default)
- generate_arrivals:  rho-based arrival pattern construction

Supports sensitivity / scale-invariance studies via explicit L, tau overrides.
"""

import math
import numpy as np

from config import (
    L_N2,
    tau_from_rho,
    PATTERN_RHO,
    PATTERN_STRUCTURE,
    DEPOT,
)


# ============================================================
# Customer position generation
# ============================================================

def generate_customers(n, seed, L=None):
    """Sample n customer positions uniformly in [0, L]^2.

    Parameters
    ----------
    n : int
        Number of customers.
    seed : int
        Random seed (numpy.random.RandomState).
    L : float, optional
        Square side length. Defaults to N2 convention L = sqrt(n).

    Returns
    -------
    dict[int, tuple[float, float]]
        Mapping customer_id (1..n) to (x, y) coordinates.
    """
    if L is None:
        L = L_N2(n)

    rng = np.random.RandomState(seed)
    positions = {}
    for i in range(1, n + 1):
        positions[i] = (rng.uniform(0, L), rng.uniform(0, L))
    return positions


# ============================================================
# Arrival time generation (rho-based)
# ============================================================

def _arrivals_simultaneous(n, ids, rng):
    """Pattern A: all customers arrive at t=0."""
    return {i: 0.0 for i in ids}


def _arrivals_sequential_uniform(n, ids, rng, tau):
    """Sequential arrivals with fixed interval tau.

    Customer i arrives at time (i - 1) * tau.
    Under N2, tau is chosen so that rho = travel_time / tau.
    """
    return {i: (i - 1) * tau for i in ids}


def _arrivals_clustered_interleave(n, ids, positions, rng, tau):
    """Pattern C: two angular clusters interleaved in time.

    Customers are sorted by their angle from depot, then split alternately
    into two clusters (0, 2, 4, ...) and (1, 3, 5, ...) by rank.
    Clusters are assigned times so that cluster gap = 2*tau.
    Small random jitter added to avoid exact coincidences.
    """
    angles = [(i, math.atan2(positions[i][1] - DEPOT[1],
                             positions[i][0] - DEPOT[0])) for i in ids]
    angles.sort(key=lambda x: x[1])

    times = {}
    # gap between the two clusters = 2*tau (clustered regime)
    cluster_gap = 2.0 * tau
    jitter_scale = 0.3 * tau  # small jitter proportional to tau

    for rank, (cid, _) in enumerate(angles):
        cluster = rank % 2  # alternating
        times[cid] = cluster * cluster_gap + rng.uniform(0, jitter_scale)
    return times


def _arrivals_reverse_zigzag(n, ids, positions, rng, tau):
    """Pattern D: zigzag arrival order based on angle extremes.

    Customers sorted by angle, then arrive in zigzag: first angle, last angle,
    second angle, second-to-last, etc.  Inter-arrival interval = tau.
    """
    angles = [(i, math.atan2(positions[i][1] - DEPOT[1],
                             positions[i][0] - DEPOT[0])) for i in ids]
    angles.sort(key=lambda x: x[1])

    zigzag_order = []
    lo, hi = 0, len(angles) - 1
    while lo <= hi:
        zigzag_order.append(angles[lo])
        if lo != hi:
            zigzag_order.append(angles[hi])
        lo += 1
        hi -= 1

    times = {}
    for rank, (cid, _) in enumerate(zigzag_order):
        times[cid] = rank * tau
    return times


def _arrivals_poisson_random(n, ids, rng, tau):
    """Pattern E: random uniform arrivals over [0, n*tau].

    Matches Poisson-like spread with mean interval ~ tau.
    """
    span = n * tau
    return {i: rng.uniform(0, span) for i in ids}


def generate_arrivals(n, pattern, positions, seed, rho=None, tau=None):
    """Generate arrival times for a given pattern.

    Parameters
    ----------
    n : int
    pattern : str
        One of {'A', 'B_heavy', 'B_medium', 'B_light', 'C', 'D', 'E'}.
    positions : dict[int, tuple[float, float]]
    seed : int
    rho : float, optional
        Load parameter. Defaults to PATTERN_RHO[pattern].
    tau : float, optional
        Mean interval. Defaults to tau_from_rho(rho).
        If given explicitly, overrides rho (used for sensitivity studies).

    Returns
    -------
    dict[int, float]
        Mapping customer_id to arrival time.
    """
    if pattern not in PATTERN_RHO:
        raise ValueError(f"Unknown pattern: {pattern}")

    if rho is None:
        rho = PATTERN_RHO[pattern]
    if tau is None:
        tau = tau_from_rho(rho)

    structure = PATTERN_STRUCTURE[pattern]
    ids = list(range(1, n + 1))
    rng = np.random.RandomState(seed + 1000)  # independent from positions RNG

    if structure == 'simultaneous':
        return _arrivals_simultaneous(n, ids, rng)
    elif structure == 'sequential_uniform':
        return _arrivals_sequential_uniform(n, ids, rng, tau)
    elif structure == 'clustered_interleave':
        return _arrivals_clustered_interleave(n, ids, positions, rng, tau)
    elif structure == 'reverse_zigzag':
        return _arrivals_reverse_zigzag(n, ids, positions, rng, tau)
    elif structure == 'poisson_random':
        return _arrivals_poisson_random(n, ids, rng, tau)
    else:
        raise ValueError(f"Unknown structure: {structure}")


# ============================================================
# Scale invariance helper (for sensitivity study)
# ============================================================

def generate_scaled_instance(n, pattern, seed, alpha=1.0):
    """Generate an instance under scaled coordinates (L -> alpha * L)
    and correspondingly scaled intervals (tau -> alpha * tau).

    Under joint rescaling (L, tau) -> (alpha*L, alpha*tau) with speed fixed,
    all dimensionless observables should be invariant to alpha.
    This is the key empirical test for scale invariance.

    Returns
    -------
    positions : dict
    arrivals : dict
    meta : dict
        Contains L, tau, rho, alpha for logging.
    """
    L_base = L_N2(n)
    L = alpha * L_base

    rho = PATTERN_RHO[pattern]
    tau_base = tau_from_rho(rho)
    tau = alpha * tau_base

    positions = generate_customers(n, seed, L=L)
    arrivals = generate_arrivals(n, pattern, positions, seed, rho=rho, tau=tau)

    meta = {
        'L': L,
        'tau': tau,
        'rho': rho,
        'alpha': alpha,
    }
    return positions, arrivals, meta
