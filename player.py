import axelrod as axl

AllC = axl.Cooperator
AllD = axl.Defector
TFT = axl.TitForTat
GTFT = axl.GTFT
GRIM = axl.Grudger
RAND = axl.Random

class ReputationAwareTFT(axl.Player):
    """
    Always defect against low-reputation opponents
    Play TFT against high-reputation opponents

    >>> p1 = ReputationAwareTFT(reputation_threshold=0.5)
    >>> p2 = axl.Cooperator()
    >>> p1._opponent_reputation = 0.3
    >>> p1.strategy(p2)
    <Action.D: 'D'>
    >>> p1._opponent_reputation = 0.7
    >>> p1.strategy(p2)
    <Action.C: 'C'>
    """
    name = "Reputation Aware TFT"
    def __init__(self, reputation_threshold=0.3):
        super().__init__()
        self.reputation_threshold = reputation_threshold

    def strategy(self, opponent):
        opp_reputation = getattr(self, '_opponent_reputation', 0.5)

        if opp_reputation <= self.reputation_threshold:
            return axl.Action.D

        if not self.history:
            return axl.Action.C

        return opponent.history[-1]


class CoalitionBuilder(axl.Player):
    """
    Cooperates with trusted partners (network weight >= K)
    Defects against others
    >>> p1 = CoalitionBuilder(K=10)
    >>> p2 = axl.Cooperator()
    >>> p1._opponent_weight = 5
    >>> p1.strategy(p2)
    <Action.D: 'D'>
    >>> p1._opponent_weight = 15
    >>> p1.strategy(p2)
    <Action.C: 'C'>
    """
    name = "Coalition Builder"

    def __init__(self, K=10):
        super().__init__()
        self.K = K

    def strategy(self, opponent):
        """
        If network_weight[opponent] >= K: Cooperate
        Otherwise: Defect
        """
        weight = getattr(self, '_opponent_weight', 0)

        if weight >= self.K:
            return axl.Action.C
        return axl.Action.D


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
