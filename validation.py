#ai tool used
import numpy as np
from simulation import run_simulation, PlayerWrapper, play_round
from player import AllC, AllD, ReputationAwareTFT, CoalitionBuilder, TFT
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
    p8.weights[p9.id] = 5
    action = p8.choose_action(p9, env)
    print(f"   CB with weight=5: action={action} (should be C, first TFT, even default K=10)")

    p8.weights[p9.id] = 15
    action = p8.choose_action(p9, env)
    print(f"   CB with weight=15: action={action} (should be C)")

    #Reputation: AllC reaches ~1.0, AllD reaches ~-1.0
    #Network weight: Cooperating pairs reach >100 after 10k rounds
    print("\n5. Long-term: Reputation & Network weights (10k rounds)")
    players = run_simulation(rounds=10000, initial_wealth=10, noise=0.05)

    allc = [p for p in players if p.strategy.name == "AllC"]
    alld = [p for p in players if p.strategy.name == "AllD"]

    for p in players:
        print(f"Player {p.id}: {p.strategy.name}, wealth={p.wealth:.1f}, bankrupt={p.bankrupt}")
        print(f"  Weights: {p.weights}")
        print()

    print(f"   AllC reputation: {np.mean([p.reputation for p in allc]):+.3f}")
    print(f"   AllD reputation: {np.mean([p.reputation for p in alld]):+.3f}")

    all_weights = [w for p in players for w in p.weights.values()]
    print(f"   Max network weight: {max(all_weights):.1f}") #the number around 240 .. make K=10 reasonable

    print("\n6. Known Outcomes: TFT vs TFT (no noise)")
    print("   Expected: Full cooperation, equal wealth growth")
    p10 = PlayerWrapper(10, TFT, initial_wealth=0, noise=0)
    p11 = PlayerWrapper(11, TFT, initial_wealth=0, noise=0)
    for _ in range(100):
        play_round(p10, p11, env)
    print(f"   After 100 rounds: p10={p10.wealth:.1f}, p11={p11.wealth:.1f}")
    print(f"   Equal? {abs(p10.wealth - p11.wealth) < 0.01}")

    print("\n7. Known Outcomes: AllD vs AllD")
    print("   Expected: Both bankrupt quickly")
    p12 = PlayerWrapper(12, AllD, initial_wealth=10, noise=0)
    p13 = PlayerWrapper(13, AllD, initial_wealth=10, noise=0)
    for _ in range(100):
        play_round(p12, p13, env, welfare=0.05)
    print(f"   After 100 rounds: both bankrupt? {p12.bankrupt and p13.bankrupt}")

    print("\n8. Convergence: Multiple identical players have similar results")
    print("   Expected: 5 AllC players should have similar wealth")
    players = run_simulation(rounds=10000)
    allc_wealth = [p.wealth for p in players if p.strategy.name == "AllC"]
    wealth_std = np.std(allc_wealth)
    print(f"   AllC wealth std dev: {wealth_std:.2f} (should be < 50)")

    print("\n9. Random Pairing Fairness")
    print("   Expected: Mean interactions ≈ 128 per pair (10k rounds, 40 players)")
    all_interactions = [len(h) for p in players for h in p.opp_history.values()]
    print(f"   Mean interactions: {np.mean(all_interactions):.1f}")
    print(f"   Std dev: {np.std(all_interactions):.1f}")



if __name__ == "__main__":
    validate()