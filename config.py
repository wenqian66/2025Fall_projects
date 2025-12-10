#1. payoff matrix

PAYOFF = {
    ("C", "C"): (2, 2),
    ("C", "D"): (-5, 6),
    ("D", "C"): (6, -5),
    ("D", "D"): (-4, -4),
}

#2. default simulation and envir... parameters
DEFAULT_PARAMS = {
    'num_rounds': 10000, # num of game rounds per simulation
    'num_trials': 50, # num of simulation trails
    'player_counts': {
        'AllC': 10,
        'AllD': 10,
        'TFT': 10,
        'GTFT': 10,
        'GRIM': 10,
        'RAND': 10,
        'ReputationAwareTFT': 10,
        'CoalitionBuilder': 10,
    },
    'initial_wealth': 20.0,
    'wealth_threshold': 0.0,
    'welfare': 0.05,

    'noise': 0.05,

    #reputation sys
    'alpha_c': 0.02,
    'alpha_d': 0.04,
    'reputation_max': 1.0,
    'reputation_min': -1.0,
    'reputation_threshold': -0.3,

    #network sys
    'gamma': 1.0,
    'delta': 1.0,
    'network_threshold': 5.0,

    'gtft_forgiveness': 0.1,
    'ratft_high_rep_threshold': 0.3,
}

# 3.experiment Config

H1_MIXED_COUNTS = {
    'AllC': 10,
    'AllD': 10,
    'TFT': 15,
    'GTFT': 10,
    'GRIM': 10,
    'RAND': 10,
    'ReputationAwareTFT': 15,
}

H1_CONFIGS = {
    'no_rep': {
        **DEFAULT_PARAMS,
        'player_counts': H1_MIXED_COUNTS,
        'initial_wealth': 30.0,
        'alpha_c': 0.0,
        'alpha_d': 0.0,
    },
    'weak_rep': {
        **DEFAULT_PARAMS,
        'player_counts': H1_MIXED_COUNTS,
        'initial_wealth': 30.0,
        'alpha_c': 0.005,
        'alpha_d': 0.01,
    },
    'moderate_rep': {
        **DEFAULT_PARAMS,
        'player_counts': H1_MIXED_COUNTS,
        'initial_wealth': 30.0,
        'alpha_c': 0.02,
        'alpha_d': 0.04,
    },
    'strong_rep': {
        **DEFAULT_PARAMS,
        'player_counts': H1_MIXED_COUNTS,
        'initial_wealth': 30.0,
        'alpha_c': 0.05,
        'alpha_d': 0.10,
    },
}

H2_BASE_COUNTS = {
    'AllC': 8,
    'AllD': 15,
    'TFT': 10,
    'GTFT': 12,
    'GRIM': 5,
    'RAND': 8,
    'ReputationAwareTFT': 10,
    'CoalitionBuilder': 20,
}

H2_NETWORK_THRESHOLDS = {
    'easy_coalition': {
        **DEFAULT_PARAMS,
        'player_counts': H2_BASE_COUNTS,
        'network_threshold': 3.0,
    },
    'moderate_coalition': {
        **DEFAULT_PARAMS,
        'player_counts': H2_BASE_COUNTS,
        'network_threshold': 5.0,
    },
    'hard_coalition': {
        **DEFAULT_PARAMS,
        'player_counts': H2_BASE_COUNTS,
        'network_threshold': 8.0,
    },
    'very_hard_coalition': {
        **DEFAULT_PARAMS,
        'player_counts': H2_BASE_COUNTS,
        'network_threshold': 12.0,
    },
}

H3_WELFARE_LEVELS = [0, 0.10, 0.20, 0.30, 0.40]

H3_BASE_CONFIG = DEFAULT_PARAMS.copy()
H3_BASE_CONFIG.update({
    'noise': 0.15,
    'num_rounds': 5000,
    'num_trials': 50,
})

H3_CONFIGS = {
    f'welfare_{int(w * 100):02d}': {
        **H3_BASE_CONFIG,
        'welfare': w
    }
    for w in H3_WELFARE_LEVELS
}