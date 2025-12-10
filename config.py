#1. payoff matrix
PAYOFF = {
    ("C", "C"): (3, 3),
    ("C", "D"): (-3, 4),
    ("D", "C"): (4, -3),
    ("D", "D"): (-2, -2),
}

#2. default simulation and envir... parameters
DEFAULT_PARAMS = {
    'num_rounds': 10000, # num of game rounds per simulation
    'num_trials': 1000, # num of simulation trails
    'players_per_strategy': 10,

    'initial_wealth': 10.0,
    'broke_threshold': 0.0,
    'welfare': 0.05,

    'noise0': 0.05,

    #reputation sys
    'alpha_c': 0.01,
    'alpha_d': 0.02,
    'reputation_max': 1.0,
    'reputation_min': -1.0,
    'reputation_threshold': 0.0,

    #network sys
    'gamma': 1.0,
    'delta': 1.0,
    'network_threshold': 5.0,
}

BASELINE_STRATEGIES = ['AllC', 'AllD', 'TFT', 'GRIM', 'GTFT', 'RAND']
ALL_STRATEGIES = BASELINE_STRATEGIES + ['ReputationAwareTFT', 'CoalitionBuilder']


# 3.experiment Config

# Baseline verification (classical PD)
BASELINE_CONFIG = DEFAULT_PARAMS.copy()
BASELINE_CONFIG.update({
    'strategies': BASELINE_STRATEGIES,
    'num_trials': 500,
})

# H1: RA-TFT vs TFT (with reputation)
H1_CONFIG = DEFAULT_PARAMS.copy()
H1_CONFIG.update({
    'strategies': ALL_STRATEGIES,
})

# H2: Coalition Builder (with reputation + network)
H2_CONFIG = DEFAULT_PARAMS.copy()
H2_CONFIG.update({
    'strategies': ALL_STRATEGIES,
})

# H3: Welfare levels under high noise
H3_WELFARE_LEVELS = [0, 0.05, 0.10, 0.15, 0.20]
H3_BASE_CONFIG = DEFAULT_PARAMS.copy()
H3_BASE_CONFIG.update({
    'strategies': ALL_STRATEGIES,
    'noise': 0.15,
    'num_rounds': 5000,
})

# Generate H3 configs for each welfare level
H3_CONFIGS = {
    f'welfare_{int(w * 100):02d}': {
        **H3_BASE_CONFIG,
        'welfare': w
    }
    for w in H3_WELFARE_LEVELS
}

# ============== GTFT Parameters ==============
GTFT_FORGIVENESS_PROB = 0.1