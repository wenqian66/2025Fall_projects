#ai tool used
import numpy as np
from simulation import run_simulation, PlayerWrapper, play_round
from player import AllC, AllD, ReputationAwareTFT, CoalitionBuilder
from environment import EnvironmentUpdater


def validate():
    """
    **Validation Checklist:**

    Payoffs work: AllC vs AllC gain equally; AllD exploits AllC successfully
    Bankruptcy triggers when wealth < 0

    RA-TFT reads opponent reputation
    Coalition Builder reads network weight

    Reputation: AllC reaches ~1.0, AllD reaches ~-1.0
    Network weight: Cooperating pairs reach >100 after 10k rounds
    """

    print("VALIDATION CHECKS")
    print("=" * 60)
    env = EnvironmentUpdater()

    print("\n1. Payoffs work")
    p1 = PlayerWrapper(0, AllC, initial_wealth=0, noise=0)
    p2 = PlayerWrapper(1, AllC, initial_wealth=0, noise=0)
    play_round(p1, p2, env)
    print(f"   AllC vs AllC: {p1.wealth} == {p2.wealth}? {p1.wealth == p2.wealth}")

    p3 = PlayerWrapper(2, AllD, initial_wealth=0, noise=0)
    p4 = PlayerWrapper(3, AllC, initial_wealth=0, noise=0)
    play_round(p3, p4, env)
    print(f"   AllD vs AllC: {p3.wealth} > {p4.wealth}? {p3.wealth > p4.wealth}")

    print("\n2. Bankruptcy triggers when wealth < 0")
    p5 = PlayerWrapper(4, AllC, initial_wealth=-1)
    env.update_bankruptcy(p5, welfare=0.05, threshold=0)
    print(f"   wealth={p5.wealth:.2f}, bankrupt={p5.bankrupt}")

    print("\n3. RA-TFT reads opponent reputation")
    p6 = PlayerWrapper(5, ReputationAwareTFT, noise=0)
    p7 = PlayerWrapper(6, AllD, noise=0)
    p7.reputation = -0.5
    action = p6.choose_action(p7, env)
    print(f"   RA-TFT vs low-rep opponent: action={action} (should be D)")

    print("\n4. Coalition Builder reads network weight")
    p8 = PlayerWrapper(7, CoalitionBuilder, noise=0)
    p9 = PlayerWrapper(8, AllC, noise=0)
    p8.weights[9] = 5
    action = p8.choose_action(p9, env)
    print(f"   CB with weight=5: action={action} (should be D, K=10)")

    p8.weights[9] = 15
    action = p8.choose_action(p9, env)
    print(f"   CB with weight=15: action={action} (should be C)")

    print("\n5. Long-term: Reputation & Network weights (10k rounds)")
    players = run_simulation(rounds=10000, initial_wealth=10, noise=0.05)

    allc = [p for p in players if p.strategy.name == "AllC"]
    alld = [p for p in players if p.strategy.name == "AllD"]

    print(f"   AllC reputation: {np.mean([p.reputation for p in allc]):+.3f}")
    print(f"   AllD reputation: {np.mean([p.reputation for p in alld]):+.3f}")

    all_weights = [w for p in players for w in p.weights.values()]
    print(f"   Max network weight: {max(all_weights):.1f}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    validate()