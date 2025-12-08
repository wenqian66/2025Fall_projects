import random
from environment import EnvironmentUpdater, noise0
from player import (
    AllC, AllD, TFT, GTFT, GRIM, RAND,
    ReputationAwareTFT, CoalitionBuilder
)


class PlayerWrapper:
    """Player = strategy + dynamic state (wealth, rep, network, bankruptcy)."""
    def __init__(self, strategy_class, noise=noise0, wealth=10):
        self.strategy = strategy_class()
        self.history = {}
        self.reputation = 0.0
        self.weights = {}
        self.wealth = wealth
        self.noise = noise
        self.bankrupt = False

    def intended_action(self, opponent):
        """Action before noise."""
        return self.strategy.strategy(opponent)

    def choose_action(self, opponent, env: EnvironmentUpdater):
        """Action after applying noise."""
        a = self.intended_action(opponent)
        return env.apply_noise(a, self.noise)

# one PD round
def play_round(p1, p2, env: EnvironmentUpdater,
               alpha_c=0.01, alpha_d=0.02,
               gamma=1.0, delta=1.0,
               welfare=0.05, bankrupt_threshold=0.0):

    a1 = p1.choose_action(p2, env)
    a2 = p2.choose_action(p1, env)

    if p2 not in p1.history:
        p1.history[p2] = []
    if p1 not in p2.history:
        p2.history[p1] = []

    p1.history[p2].append(a1)
    p2.history[p1].append(a2)

    env.update_payoff(p1, p2, a1, a2)
    env.update_reputation(p1, p2, a1, a2, alpha_c, alpha_d)
    env.update_network(p1, p2, a1, a2, gamma, delta)
    env.update_bankruptcy(p1, welfare=welfare, threshold=bankrupt_threshold)
    env.update_bankruptcy(p2, welfare=welfare, threshold=bankrupt_threshold)


def random_pairing(players):
    """Randomly pair non-bankrupt players."""
    random.shuffle(players)
    pairs = []
    for i in range(0, len(players)-1, 2):
        p1, p2 = players[i], players[i+1]
        if not p1.bankrupt and not p2.bankrupt:
            pairs.append((p1, p2))
    return pairs

#Main simulation loop
def run_simulation(
    strategy_classes,
    rounds=10000,
    noise=noise0,
    initial_wealth=10,
    alpha_c=0.01, alpha_d=0.02,
    gamma=1.0, delta=1.0,
    welfare=0.05,
    bankrupt_threshold=0.0
):

    env = EnvironmentUpdater()

    # create one player per strategy
    players = [
        PlayerWrapper(cls, noise=noise, wealth=initial_wealth)
        for cls in strategy_classes
    ]

    for _ in range(rounds):
        for p1, p2 in random_pairing(players):
            play_round(
                p1, p2, env,
                alpha_c=alpha_c, alpha_d=alpha_d,
                gamma=gamma, delta=delta,
                welfare=welfare, bankrupt_threshold=bankrupt_threshold
            )

    return players
