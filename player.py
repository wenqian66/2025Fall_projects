# baseline(6) strategies code cite from axelrod and chatgpt
#6+2 strategies in total
import random
#doctest test the baseline strategies' first move
class AllC:
    """Always Cooperate
    >>> AllC().strategy(AllD()) == "C"
    True
    """
    name = "AllC"
    def __init__(self):
        self.history = {}
    def strategy(self, opponent):
        return "C"

class AllD:
    """Always Defect
    >>> AllD().strategy(AllC()) == "D"
    True
    """
    name = "AllD"
    def __init__(self):
        self.history = {}
    def strategy(self, opponent):
        return "D"

class TFT:
    """Tit For Tat: Cooperate first, then copy opponent
    >>> TFT().strategy(AllC()) == "C"
    True
    """
    name = "TFT"
    def __init__(self):
        self.history = {}
    def strategy(self, opponent):
        opp_hist = opponent.history.get(self, [])
        if not opponent.history:
            return "C"
        return opp_hist[-1]

class GTFT:
    """Generous TFT: cooperate unless opponent defected AND random chance
    >>> isinstance(GTFT().strategy(AllC()), str)
    True
    """
    name = "GTFT"
    def __init__(self, p=0.1):
        self.history = {}
        self.p = p
    def strategy(self, opponent):
        opp_hist = opponent.history.get(self, [])
        if not opp_hist:
            return "C"
        last = opp_hist[-1]
        if last == "D" and random.random() < self.p:
            return "C"
        return last

class GRIM:
    """Grim Trigger: Cooperate until opponent defects once, then always defect
    >>> GRIM().strategy(AllC()) == "C"
    True
    """
    name = "Grim"
    def __init__(self):
        self.history = {}
        self.grim = False
    def strategy(self, opponent):
        opp_hist = opponent.history.get(self, [])
        if "D" in opp_hist:
            self.grim = True
        return "D" if self.grim else "C"

class RAND:
    """Random strategy"""
    name = "Random"
    def __init__(self):
        self.history = {}
    def strategy(self, opponent):
        import random
        return "C" if random.random() < 0.5 else "D"

class ReputationAwareTFT:
    """
    Always defect against low-reputation opponents
    Play TFT against high-reputation opponents
    >>> p1 = ReputationAwareTFT(reputation_threshold=0.5)
    >>> p2 = AllC()
    >>> p1._opponent_reputation = 0.3
    >>> p1.strategy(p2)
    'D'

    >>> p1._opponent_reputation = 0.7
    >>> p2.history[p1] = ['C','D','C']
    >>> p1.strategy(p2)
    'C'
    """
    name = "Reputation Aware TFT"
    def __init__(self, reputation_threshold=0.3):
        super().__init__()
        self.history = {}
        self.reputation_threshold = reputation_threshold

    def strategy(self, opponent):
        opp_reputation = getattr(self, '_opponent_reputation', 0.5)

        if opp_reputation <= self.reputation_threshold:
            return "D"

        opp_hist = opponent.history.get(self, [])
        if not opp_hist:
            return "C"
        return opp_hist[-1]


class CoalitionBuilder:
    """
    Cooperates with trusted partners (network weight >= K)
    Defects against others
    >>> p1 = CoalitionBuilder(K=10)
    >>> p2 = AllC()
    >>> p1._opponent_weight = 5
    >>> p1.strategy(p2)
    'D'
    >>> p1._opponent_weight = 15
    >>> p1.strategy(p2)
    'C'
    """
    name = "Coalition Builder"

    def __init__(self, K=10):
        super().__init__()
        self.K = K

    def strategy(self, opponent):
        weight = getattr(self, '_opponent_weight', 0)

        if weight >= self.K:
            return "C"
        return "D"


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
