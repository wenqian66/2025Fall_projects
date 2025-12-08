from player import AllC, AllD, TFT, GTFT, GRIM, RAND, ReputationAwareTFT, CoalitionBuilder
from environment import EnvironmentUpdater, noise0
import random

class PlayerWrapper:
    """Player = strategy + dynamic environment state."""

    def __init__(self, strategy_class, noise=noise0, wealth=10):
        self.strategy = strategy_class()
        self.reputation = 0.0
        self.wealth = wealth
        self.noise = noise
        self.history = []
        self.bankrupt = False
        self.weights = {}

    def choose_strategy_action(self, opponent):
        """Call strategy logic (C/D) without noise."""
        return self.strategy.strategy(opponent.strategy)


#single round
def play_round(
    p1, p2,
    alpha_c=0.01, alpha_d=0.02,
    gamma=1.0, delta=1.0,
    welfare=0.05, bankrupt_threshold=0.0
):
    a1 = p1.choose_action(p2)
    a2 = p2.choose_action(p1)

    p1.history.append(a1)
    p2.history.append(a2)

    # payoff
    payoff1, payoff2 = PAYOFF[(a1, a2)]
    p1.wealth += payoff1
    p2.wealth += payoff2

    # reputation
    p1.reputation += alpha_c if a1 == "C" else -alpha_d
    p2.reputation += alpha_c if a2 == "C" else -alpha_d
    p1.reputation = max(-1, min(1, p1.reputation))
    p2.reputation = max(-1, min(1, p2.reputation))

    # network
    p1.weights[p2] = p1.weights.get(p2, 0)
    p2.weights[p1] = p2.weights.get(p1, 0)

    if a1 == "C" and a2 == "C":
        p1.weights[p2] += gamma
        p2.weights[p1] += gamma
    else:
        p1.weights[p2] = max(0, p1.weights[p2] - delta)
        p2.weights[p1] = max(0, p2.weights[p1] - delta)

    # bankruptcy + welfare
    for p in (p1, p2):
        if p.wealth < bankrupt_threshold:
            p.bankrupt = True
        if p.bankrupt:
            p.wealth += welfare


def random_pairing(players):
    random.shuffle(players)
    pairs = []
    for i in range(0, len(players)-1, 2):
        p1, p2 = players[i], players[i+1]
        if not p1.bankrupt and not p2.bankrupt:
            pairs.append((p1, p2))
    return pairs

def run_simulation(
    strategy_classes,
    rounds=10000,
    noise=noise0
):
    players = [PlayerWrapper(cls, noise=noise) for cls in strategy_classes]

    for _ in range(rounds):
        pairs = random_pairing(players)
        for p1, p2 in pairs:
            play_round(p1, p2)

    return players