# baseline(6) strategies code cite from axelrod and chatgpt
#6+2 strategies in total
import random

class OpponentView:
    def __init__(self, history):
        self.history = history

#doctest test the baseline strategies' first move
class AllC:
    """Always Cooperate
    >>> AllC().strategy(OpponentView([])) == "C"
    True
    """
    name = "AllC"
    def strategy(self, opponent):
        return "C"

class AllD:
    """Always Defect
    >>> AllD().strategy(OpponentView([])) == "D"
    True
    """
    name = "AllD"
    def strategy(self, opponent):
        return "D"

class TFT:
    """Tit For Tat: Cooperate first, then copy opponent
    >>> TFT().strategy(OpponentView([])) == "C"
    True
    >>> TFT().strategy(OpponentView(['D'])) == "D"
    True
    >>> TFT().strategy(OpponentView(['C', 'D', 'C'])) == "C"
    True
    """
    name = "TFT"
    def strategy(self, opponent):
        if not opponent.history:
            return "C"
        return opponent.history[-1]

class GTFT:
    """Generous TFT: cooperate unless opponent defected AND random chance
    >>> GTFT().strategy(OpponentView([])) == "C"
    True
    >>> GTFT().strategy(OpponentView(['C'])) == "C"
    True
    >>> result = GTFT().strategy(OpponentView(['D']))
    >>> result in ['C', 'D']
    True
    """
    name = "GTFT"
    def __init__(self, p=0.1):
        self.p = p
    def strategy(self, opponent):
        if not opponent.history:
            return "C"
        if opponent.history[-1] == "D" and random.random() < self.p:
            return "C"
        return opponent.history[-1]

class GRIM:
    """Grim Trigger: Cooperate until opponent defects once, then always defect
    >>> grim = GRIM()
    >>> opp1 = OpponentView(['C', 'C'])
    >>> opp1._id = 1
    >>> grim.strategy(opp1) == "C"
    True
    >>> opp2 = OpponentView(['C', 'D', 'C'])
    >>> opp2._id = 2
    >>> grim.strategy(opp2) == "D"
    True
    >>> grim.strategy(opp2) == "D"
    True
    """
    name = "Grim"
    def __init__(self):
        self.triggered = {}
    def strategy(self, opponent):
        opp_id = getattr(opponent, '_id', None)
        if opp_id not in self.triggered:
            self.triggered[opp_id] = False

        if "D" in opponent.history:
            self.triggered[opp_id] = True

        return "D" if self.triggered[opp_id] else "C"

class RAND:
    """Random strategy"""
    name = "Random"
    def strategy(self, opponent):
        import random
        return "C" if random.random() < 0.5 else "D"

class ReputationAwareTFT:
    """
    Always defect against low-reputation opponents
    Play TFT against high-reputation opponents
    >>> ratft = ReputationAwareTFT(reputation_threshold=0.5)
    >>> opp1 = OpponentView([])
    >>> opp1._reputation = 0.3
    >>> ratft.strategy(opp1)
    'D'

    >>> opp2 = OpponentView(['C', 'D', 'C'])
    >>> opp2._reputation = 0.7
    >>> ratft.strategy(opp2)
    'C'

    >>> opp3 = OpponentView(['D'])
    >>> opp3._reputation = 0.8
    >>> ratft.strategy(opp3)
    'D'
    """
    name = "Reputation Aware TFT"
    def __init__(self, reputation_threshold=0.3):
        self.reputation_threshold = reputation_threshold

    def strategy(self, opponent):
        opp_reputation = getattr(opponent, '_reputation', 0.0)

        if opp_reputation <= self.reputation_threshold:
            return "D"

        if not opponent.history:
            return "C"
        return opponent.history[-1]


class CoalitionBuilder:
    """
    Cooperates with trusted partners (network weight >= K)
    Defects against others
    >>> cb = CoalitionBuilder(K=10)
    >>> opp = OpponentView([])
    >>> opp._weight = 5
    >>> cb.strategy(opp)
    'C'

    >>> opp.history = ['C','C','C','D']
    >>> opp._weight = 5
    >>> cb.strategy(opp)
    'D'

    >>> opp._weight = 15
    >>> cb.strategy(opp)
    'C'

    >>> opp._weight = 10
    >>> cb.strategy(opp)
    'C'
    """
    name = "Coalition Builder"

    def __init__(self, K=10):
        self.K = K

    def strategy(self, opponent):
        weight = getattr(opponent, '_weight', 0)

        if weight >= self.K:
            return "C"
        if not opponent.history:
            return "C"
        return opponent.history[-1]


ALL_STRATEGIES = [
    AllC,
    AllD,
    TFT,
    GTFT,
    GRIM,
    RAND,
    ReputationAwareTFT,
    CoalitionBuilder
]
