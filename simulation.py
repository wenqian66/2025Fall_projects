#chatgpt used

import random
from environment import EnvironmentUpdater, noise0
from player import (
    OpponentView, ALL_STRATEGIES,
    AllC, AllD, TFT, GTFT, GRIM, RAND,
    ReputationAwareTFT, CoalitionBuilder
)

class PlayerWrapper:
    """
    >>> p = PlayerWrapper(0, AllC, initial_wealth=100)
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
    def __init__(self, player_id, strategy_class, initial_wealth=10, noise=noise0):
        self.id = player_id
        self.strategy = strategy_class()
        self.my_history = {}
        self.opp_history = {}
        self.reputation = 0.0
        self.weights = {}
        self.wealth = initial_wealth
        self.noise = noise
        self.bankrupt = False

    def choose_action(self, opponent, env):
        opp_id = opponent.id
        opp_actions = self.opp_history.get(opp_id, [])
        opponent_view = OpponentView(opp_actions)
        opponent_view._id = opp_id
        opponent_view._reputation = opponent.reputation
        opponent_view._weight = self.weights.get(opp_id, 0)
        action = self.strategy.strategy(opponent_view)
        return env.apply_noise(action, self.noise)

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
        if opponent_id not in self.my_history:
            self.my_history[opponent_id] = []
            self.opp_history[opponent_id] = []
        self.my_history[opponent_id].append(my_action)
        self.opp_history[opponent_id].append(opp_action)


def play_round(p1, p2, env,
               alpha_c=0.01, alpha_d=0.02,
               gamma=1.0, delta=1.0,
               welfare=0.05, bankrupt_threshold=0.0):
    """
    >>> env = EnvironmentUpdater()
    >>> p1 = PlayerWrapper(0, AllC, initial_wealth=10, noise=0)
    >>> p2 = PlayerWrapper(1, AllD, initial_wealth=10, noise=0)
    >>> play_round(p1, p2, env)
    >>> p1.wealth
    10.0
    >>> p2.wealth
    11.0
    >>> p1.reputation
    0.01
    >>> p2.reputation
    -0.02
    >>> p1.weights[1]
    0
    >>> p2.weights[0]
    0
    """
    a1 = p1.choose_action(p2, env)
    a2 = p2.choose_action(p1, env)
    p1.record_actions(p2.id, a1, a2)
    p2.record_actions(p1.id, a2, a1)
    env.update_payoff(p1, p2, a1, a2)
    env.update_reputation(p1, p2, a1, a2, alpha_c, alpha_d)
    env.update_network(p1, p2, a1, a2, gamma, delta)
    env.update_bankruptcy(p1, welfare, bankrupt_threshold)
    env.update_bankruptcy(p2, welfare, bankrupt_threshold)


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


def run_simulation(strategy_classes=None,
                   rounds=10000,
                   initial_wealth=10,
                   noise=noise0,
                   alpha_c=0.01, alpha_d=0.02,
                   gamma=1.0, delta=1.0,
                   welfare=0.05,
                   bankrupt_threshold=0.0):
    if strategy_classes is None:
        strategy_classes = ALL_STRATEGIES

    env = EnvironmentUpdater()
    players = []
    for sid, strategy_class in enumerate(strategy_classes):
        for i in range(5):
            player_id = sid * 5 + i
            players.append(PlayerWrapper(player_id, strategy_class, initial_wealth, noise))

    for round_num in range(rounds):
        for p1, p2 in random_pairing(players):
            play_round(p1, p2, env, alpha_c=alpha_c, alpha_d=alpha_d,
                       gamma=gamma, delta=delta, welfare=welfare,
                       bankrupt_threshold=bankrupt_threshold)
    return players


def run_monte_carlo(n_trials=1000, **kwargs):
    results = []
    for trial in range(n_trials):
        if trial % 100 == 0:
            print(f"Trial {trial}/{n_trials}")
        players = run_simulation(**kwargs)
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


if __name__ == "__main__":
    players = run_simulation(rounds=1000)
    result = analyze_trial(players)
    for strategy, stats in result.items():
        print(f"{strategy:20s}: Survival={stats['survival_rate']:.2%}, Avg Wealth={stats['avg_wealth']:.2f}")