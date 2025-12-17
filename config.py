class GameConfig:
    def __init__(self,
                 num_rounds=1000,
                 num_trials=50,
                 player_counts=None,
                 initial_wealth=20.0,
                 wealth_threshold=0.0,
                 noise=0.05,

                 alpha_c=0.01,
                 alpha_d=0.02,
                 reputation_max=1.0,
                 reputation_min=-1.0,
                 reputation_threshold=-0.3,

                 gamma=1.0,
                 delta=1.0,
                 network_threshold=4.0,

                 gtft_forgiveness=0.1,
                 ratft_high_rep_threshold=0.3):
        self.payoff = {
            ("C", "C"): (2, 2),
            ("C", "D"): (-5, 6),
            ("D", "C"): (6, -5),
            ("D", "D"): (-4, -4),
        }

        self.num_rounds = num_rounds
        self.num_trials = num_trials
        self.player_counts = player_counts or {
            'AllC': 10, 'AllD': 10, 'TFT': 10, 'GTFT': 10,
            'GRIM': 10, 'RAND': 10, 'ReputationAwareTFT': 10,
            'CoalitionBuilder': 10
        }
        self.initial_wealth = initial_wealth
        self.wealth_threshold = wealth_threshold
        self.noise = noise

        self.alpha_c = alpha_c
        self.alpha_d = alpha_d
        self.reputation_max = reputation_max
        self.reputation_min = reputation_min
        self.reputation_threshold = reputation_threshold

        self.gamma = gamma
        self.delta = delta
        self.network_threshold = network_threshold

        self.gtft_forgiveness = gtft_forgiveness
        self.ratft_high_rep_threshold = ratft_high_rep_threshold


def create_h1_configs():
    h1_player_counts = {
        'AllC': 10, 'AllD': 10, 'TFT': 15, 'GTFT': 10,
        'GRIM': 10, 'RAND': 10, 'ReputationAwareTFT': 15
    }

    rep_signals = [
        ('no_rep', 0.0, 0.0),
        ('weak_rep', 0.005, 0.01),
        ('weak_moderate_rep', 0.01, 0.02),
        ('moderate_rep', 0.02, 0.04),
        ('moderate_strong_rep', 0.03, 0.06),
        ('strong_rep', 0.05, 0.10),
    ]

    return {
        name: GameConfig(
            player_counts=h1_player_counts,
            initial_wealth=30.0,
            alpha_c=ac,
            alpha_d=ad
        )
        for name, ac, ad in rep_signals
    }


def create_h2_configs():
    h2_player_counts = {
        'AllC': 10, 'AllD': 10, 'TFT': 15, 'GTFT': 10,
        'GRIM': 10, 'RAND': 10, 'ReputationAwareTFT': 10,
        'CoalitionBuilder': 15
    }

    thresholds = {
        'very_easy': 1.0,
        'easy': 2.0,
        'moderate': 3.0,
        'moderate_hard': 5.0,
        'hard': 8.0,
        'very_hard': 12.0,
    }

    return {
        name: GameConfig(
            player_counts=h2_player_counts,
            network_threshold=threshold,
            alpha_c=0.0,
            alpha_d = 0.0
        )
        for name, threshold in thresholds.items()
    }


def create_h3_configs():
    noise_levels = [0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30]

    h3_player_counts = {
        'AllC': 15, 'AllD': 10, 'TFT': 10, 'GTFT': 10,
        'GRIM': 10, 'RAND': 10, 'ReputationAwareTFT': 15,
        'CoalitionBuilder': 15
    }

    return {
        f'noise_{int(n * 100):02d}': GameConfig(
            noise=n,
            num_rounds=3000,
            num_trials=50,
            player_counts=h3_player_counts,
            alpha_c=0.01,
            alpha_d=0.02,
            network_threshold=3.5
        )
        for n in noise_levels
    }