# baseline(6) strategies code cite from axelrod and chatgpt
#6+2 strategies in total
import random
from config import DEFAULT_PARAMS


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
    """Generous TFT: cooperate first, then p to coopertate and (1-p) do TFT
    >>> GTFT().strategy(OpponentView([])) == "C"
    True
    >>> GTFT().strategy(OpponentView(['C'])) == "C"
    True
    >>> result = GTFT().strategy(OpponentView(['D']))
    >>> result in ['C', 'D']
    True
    """
    name = "GTFT"
    def __init__(self, p=None):
        if p is None:
            p = DEFAULT_PARAMS['gtft_forgiveness']
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
    Reputation-based strategy: uses GTFT for high rep, Defect for low rep, TFT for medium
    >>> ratft = ReputationAwareTFT(reputation_threshold=-0.5, high_rep_threshold=0.3)
    >>> opp1 = OpponentView([])
    >>> opp1._reputation = 0.0
    >>> ratft.strategy(opp1)
    'C'

    >>> opp2 = OpponentView(['C'])
    >>> opp2._reputation = 0.5
    >>> ratft.strategy(opp2)
    'C'

    >>> opp4 = OpponentView(['C', 'D'])
    >>> opp4._reputation = -0.6
    >>> opp4._id = 1
    >>> ratft.strategy(opp4)
    'D'
    """
    name = "Reputation Aware TFT"

    def __init__(self, reputation_threshold=None, high_rep_threshold=None):
        if reputation_threshold is None:
            reputation_threshold = DEFAULT_PARAMS['reputation_threshold']
        if high_rep_threshold is None:
            high_rep_threshold = DEFAULT_PARAMS['ratft_high_rep_threshold']
        self.reputation_threshold = reputation_threshold
        self.high_rep_threshold = high_rep_threshold
        self.tft = TFT()
        self.gtft = GTFT()

    def strategy(self, opponent):
        opp_reputation = getattr(opponent, '_reputation', 0.0)

        if opp_reputation > self.high_rep_threshold:
            return self.gtft.strategy(opponent)
        elif opp_reputation < self.reputation_threshold:
            return "D"
        else:
            return self.tft.strategy(opponent)


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

    def __init__(self, K=None):
        if K is None:
            K = DEFAULT_PARAMS['network_threshold']
        self.K = K
        self.tft = TFT()

    def strategy(self, opponent):
        weight = getattr(opponent, '_weight', 0)
        if weight >= self.K:
            return "C"
        return self.tft.strategy(opponent)


STRATEGY_MAP = {
    'AllC': AllC,
    'AllD': AllD,
    'TFT': TFT,
    'GTFT': GTFT,
    'GRIM': GRIM,
    'RAND': RAND,
    'ReputationAwareTFT': ReputationAwareTFT,
    'CoalitionBuilder': CoalitionBuilder,
}