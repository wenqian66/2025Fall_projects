#chatgpt used
import random
from config import PAYOFF

class EnvironmentUpdater:
    def apply_noise(self, action, noise):
        """Flip C/D with probability noise.

        # no noise
        >>> env = EnvironmentUpdater()
        >>> env.apply_noise("C", 0)
        'C'
        >>> env.apply_noise("D", 0)
        'D'

        >>> # full noise always flips
        >>> flipped = [env.apply_noise("C", 1) for _ in range(5)]
        >>> all(a == 'D' for a in flipped)
        True
        """
        if random.random() < noise:
            return "D" if action == "C" else "C"
        return action

    def update_payoff(self, p1, p2, a1, a2):
        """
        p1,p2 are the players
        a1,a2 are the chosen action
        >>> class P: pass
        >>> p1, p2 = P(), P()
        >>> p1.wealth, p2.wealth = 0, 0
        >>> env = EnvironmentUpdater()

        >>> env.update_payoff(p1, p2, "C", "C")
        >>> (p1.wealth, p2.wealth)
        (3, 3)

        >>> p1.wealth, p2.wealth = 0, 0
        >>> env.update_payoff(p1, p2, "D", "D")
        >>> (p1.wealth, p2.wealth)
        (-2, -2)

        >>> p1.wealth, p2.wealth = 0, 0
        >>> env.update_payoff(p1, p2, "C", "D")
        >>> (p1.wealth, p2.wealth)
        (-3, 4)

        >>> p1.wealth, p2.wealth = 0, 0
        >>> env.update_payoff(p1, p2, "D", "C")
        >>> (p1.wealth, p2.wealth)
        (4, -3)
        """
        payoff1, payoff2 = PAYOFF[(a1, a2)]
        p1.wealth += payoff1
        p2.wealth += payoff2

    def update_reputation(self, p1, p2, a1, a2,
                          alpha_c, alpha_d, reputation_max,reputation_min):
        """
        >>> class P: pass
        >>> p1, p2 = P(), P()
        >>> p1.reputation, p2.reputation = 0, 0
        >>> env = EnvironmentUpdater()

        >>> env.update_reputation(p1, p2, "C", "C", 0.02, 0.04, 1.0, -1.0)
        >>> (p1.reputation, p2.reputation)
        (0.02, 0.02)

        # Defections decreases reputation (alpha_d=0.04)
        >>> p1.reputation, p2.reputation = 0, 0
        >>> env.update_reputation(p1, p2, "D", "D", 0.02, 0.04, 1.0, -1.0)
        >>> (p1.reputation, p2.reputation)
        (-0.04, -0.04)

        >>> p1.reputation, p2.reputation = 0, 0
        >>> env.update_reputation(p1, p2, "C", "D", 0.02, 0.04, 1.0, -1.0)
        >>> (p1.reputation, p2.reputation)
        (0.02, -0.04)

        # boundary
        >>> p1.reputation, p2.reputation = 0.99, -0.99
        >>> env.update_reputation(p1, p2, "C", "D", 0.02, 0.04, 1.0, -1.0)
        >>> (round(p1.reputation, 2), round(p2.reputation, 2))
        (1.0, -1.0)
        """
        p1.reputation += alpha_c if a1 == "C" else -alpha_d
        p2.reputation += alpha_c if a2 == "C" else -alpha_d

        p1.reputation = max(reputation_min, min(reputation_max, p1.reputation))
        p2.reputation = max(reputation_min, min(reputation_max, p2.reputation))

    def update_network(self, p1, p2, a1, a2, gamma, delta):
        """
        gamma is the enhancement
        delta is the punishment

        >>> class P:
        ...     def __init__(self, player_id):
        ...         self.id = player_id
        ...         self.weights = {}
        >>> p1, p2 = P(1), P(2)
        >>> env = EnvironmentUpdater()

        >>> env.update_network(p1, p2, "C", "C", 1.0, 1.0)
        >>> p1.weights[2], p2.weights[1]
        (1.0, 1.0)

        >>> env.update_network(p1, p2, "C", "C", 1.0, 1.0)
        >>> p1.weights[2], p2.weights[1]
        (2.0, 2.0)

        >>> env.update_network(p1, p2, "D", "D", 1.0, 1.0)
        >>> p1.weights[2], p2.weights[1]
        (1.0, 1.0)

        >>> env.update_network(p1, p2, "C", "D", 1.0, 1.0)
        >>> p1.weights[2], p2.weights[1]
        (0, 0)
        """
        p1.weights[p2.id] = p1.weights.get(p2.id, 0)
        p2.weights[p1.id] = p2.weights.get(p1.id, 0)

        if a1 == "C" and a2 == "C":
            p1.weights[p2.id] += gamma
            p2.weights[p1.id] += gamma
        else:
            p1.weights[p2.id] = max(0, p1.weights[p2.id] - delta)
            p2.weights[p1.id] = max(0, p2.weights[p1.id] - delta)

    def update_bankruptcy(self, p, welfare, threshold):
        """
        >>> class P:
        ...     def __init__(self, wealth):
        ...         self.wealth = wealth
        ...         self.bankrupt = False

        >>> env = EnvironmentUpdater()

        # wealth < threshold -> bankrupt
        >>> p = P(-1)
        >>> env.update_bankruptcy(p, welfare=0.1, threshold=0)
        >>> p.bankrupt
        True
        >>> round(p.wealth, 2)
        -0.9

        # bankrupt -> welfare keeps adding
        >>> env.update_bankruptcy(p, welfare=0.1, threshold=0)
        >>> round(p.wealth, 2)
        -0.8

        # Bankruptcy is checked before welfare, so q.bankrupt updates one round late.
        >>> q = P(-.09)
        >>> env.update_bankruptcy(q, welfare=0.1, threshold=0)
        >>> (q.bankrupt, round(q.wealth, 2))
        (True, 0.01)

        >>> env.update_bankruptcy(q, welfare=0.1, threshold=0)
        >>> (q.bankrupt, round(q.wealth, 2))
        (False, 0.01)
        """
        p.bankrupt = (p.wealth < threshold)
        if p.bankrupt:
            p.wealth += welfare

    def update_all(self, p1, p2, a1, a2, params):
        self.update_payoff(p1, p2, a1, a2)
        self.update_reputation(
            p1, p2, a1, a2,
            params['alpha_c'], params['alpha_d'],
            params['reputation_max'], params['reputation_min']
        )
        self.update_network(
            p1, p2, a1, a2,
            params['gamma'], params['delta']
        )
        self.update_bankruptcy(p1, params['welfare'], params['wealth_threshold'])
        self.update_bankruptcy(p2, params['welfare'], params['wealth_threshold'])
