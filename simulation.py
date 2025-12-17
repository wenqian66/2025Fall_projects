#chatgpt used
import random
from environment import EnvironmentUpdater
from player import (
    OpponentView,
    AllC, AllD, TFT, GRIM,
)
from player import STRATEGY_MAP
import numpy as np
from utils import print_results_with_ci


class PlayerWrapper:
    """
    >>> p = PlayerWrapper(0, AllC, initial_wealth=100, noise=0.05)
    >>> p.id
    0
    >>> p.wealth
    100
    >>> p.bankrupt
    False
    >>> p.reputation
    0.0
    >>> p.noise
    0.05
    """
    def __init__(self, player_id, strategy_class, initial_wealth=10, noise=0.05):
        self.id = player_id
        self.strategy = None
        self.my_history = {}
        self.opp_history = {}
        self.reputation = 0.0
        self.weights = {}
        self.wealth = initial_wealth
        self.noise = noise
        self.bankrupt = False

    def _build_opponent_view(self, opponent):
        opp_id = opponent.id
        v = OpponentView(self.opp_history.get(opp_id, []))
        v._id = opp_id
        v._reputation = opponent.reputation
        v._weight = self.weights.get(opp_id, 0)
        return v

    def choose_action(self, opponent, env):
        opponent_view = self._build_opponent_view(opponent)
        action = self.strategy.strategy(opponent_view)
        return env.apply_noise(action, self.noise)

    def _ensure_history(self, opponent_id):
        if opponent_id not in self.my_history:
            self.my_history[opponent_id] = []
            self.opp_history[opponent_id] = []

    def record_actions(self, opponent_id, my_action, opp_action):
        """
        >>> p = PlayerWrapper(0, AllC)
        >>> p.record_actions(1, 'C', 'D')
        >>> p.my_history[1]
        ['C']
        >>> p.opp_history[1]
        ['D']
        >>> p.record_actions(1, 'C', 'C')
        >>> p.my_history[1]
        ['C', 'C']
        >>> p.opp_history[1]
        ['D', 'C']
        """
        self._ensure_history(opponent_id)
        self.my_history[opponent_id].append(my_action)
        self.opp_history[opponent_id].append(opp_action)


def play_round(p1, p2, env, config):
    """
    >>> from config import GameConfig
    >>> env = EnvironmentUpdater()
    >>> config = GameConfig()
    >>> p1 = PlayerWrapper(0, AllC, initial_wealth=10, noise=0)
    >>> p2 = PlayerWrapper(1, AllD, initial_wealth=10, noise=0)
    >>> play_round(p1, p2, env, config)
    >>> p1.wealth
    5
    >>> p2.wealth
    16
    >>> p1.reputation
    0.02
    >>> p2.reputation
    -0.04
    >>> p1.weights[1]
    0
    >>> p2.weights[0]
    0
    """
    a1 = p1.choose_action(p2, env)
    a2 = p2.choose_action(p1, env)
    p1.record_actions(p2.id, a1, a2)
    p2.record_actions(p1.id, a2, a1)
    env.update_all(p1, p2, a1, a2, config)


def random_pairing(players):
    """
    >>> p1 = PlayerWrapper(0, AllC)
    >>> p2 = PlayerWrapper(1, AllD)
    >>> p3 = PlayerWrapper(2, TFT)
    >>> p3.bankrupt = True
    >>> pairs = random_pairing([p1, p2, p3])
    >>> len(pairs)
    1
    >>> p1 in pairs[0] or p2 in pairs[0]
    True

    >>> p4 = PlayerWrapper(3, GRIM)
    >>> pairs = random_pairing([p1, p2, p3, p4])
    >>> len(pairs)
    1
    """
    active = [p for p in players if not p.bankrupt]
    random.shuffle(active)
    pairs = []
    for i in range(0, len(active) - 1, 2):
        pairs.append((active[i], active[i + 1]))
    return pairs


def run_simulation(config):
    player_counts = config.player_counts
    rounds = config.num_rounds
    initial_wealth = config.initial_wealth
    noise = config.noise

    env = EnvironmentUpdater()
    players = []
    player_id = 0

    for strategy_name, count in player_counts.items():
        strategy_class = STRATEGY_MAP[strategy_name]
        for _ in range(count):
            player = PlayerWrapper(player_id, strategy_class, initial_wealth, noise)

            if strategy_name == 'GTFT':
                player.strategy = strategy_class(config.gtft_forgiveness)
            elif strategy_name == 'ReputationAwareTFT':
                player.strategy = strategy_class(config.reputation_threshold, config.ratft_high_rep_threshold)
            elif strategy_name == 'CoalitionBuilder':
                player.strategy = strategy_class(config.network_threshold)
            else:
                player.strategy = strategy_class()

            players.append(player)
            player_id += 1

    for round_num in range(rounds):
        for p1, p2 in random_pairing(players):
            play_round(p1, p2, env, config)
    return players


def run_monte_carlo(config):
    num_trials = config.num_trials
    results = []
    for trial in range(num_trials):
        if trial % 100 == 0:
            print(f"Trial {trial}/{num_trials}")
        players = run_simulation(config)
        results.append(analyze_trial(players))
    return results


def analyze_trial(players):
    """
    >>> p1 = PlayerWrapper(0, AllC, initial_wealth=50)
    >>> p2 = PlayerWrapper(1, AllC, initial_wealth=60)
    >>> p3 = PlayerWrapper(2, AllD, initial_wealth=30)
    >>> p3.bankrupt = True
    >>> result = analyze_trial([p1, p2, p3])
    >>> result['AllC']['total']
    2
    >>> result['AllC']['survived']
    2
    >>> result['AllC']['survival_rate']
    1.0
    >>> result['AllD']['survived']
    0
    >>> result['AllD']['survival_rate']
    0.0
    """
    by_strategy = {}
    for p in players:
        strategy_name = p.strategy.name
        if strategy_name not in by_strategy:
            by_strategy[strategy_name] = {
                'total': 0,
                'survived': 0,
                'total_wealth': 0.0,
                'final_wealth': []
            }
        by_strategy[strategy_name]['total'] += 1
        if not p.bankrupt:
            by_strategy[strategy_name]['survived'] += 1
        by_strategy[strategy_name]['total_wealth'] += p.wealth
        by_strategy[strategy_name]['final_wealth'].append(p.wealth)

    for strategy_name in by_strategy:
        data = by_strategy[strategy_name]
        data['survival_rate'] = data['survived'] / data['total']
        data['avg_wealth'] = data['total_wealth'] / data['total']
    return by_strategy


def aggregate_monte_carlo_results(results):
    aggregated = {}
    for trial_result in results:
        for strategy, stats in trial_result.items():
            if strategy not in aggregated:
                aggregated[strategy] = {'survival_rates': [], 'avg_wealths': []}
            aggregated[strategy]['survival_rates'].append(stats['survival_rate'])
            aggregated[strategy]['avg_wealths'].append(stats['avg_wealth'])

    return {
        strategy: {
            'survival_mean': np.mean(data['survival_rates']),
            'survival_std': np.std(data['survival_rates']),
            'wealth_mean': np.mean(data['avg_wealths']),
            'wealth_std': np.std(data['avg_wealths']),
            'n_trials': len(data['survival_rates'])
        }
        for strategy, data in aggregated.items()
    }



