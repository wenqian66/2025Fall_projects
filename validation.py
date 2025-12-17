#ai tool used
from config import GameConfig
from simulation import run_simulation, aggregate_monte_carlo_results, analyze_trial
import numpy as np
import matplotlib.pyplot as plt

def check_single_strategy(strategy_name, num_players, num_rounds):
    config = GameConfig(
        player_counts={strategy_name: num_players},
        num_rounds=num_rounds,
        num_trials=1
    )
    players = run_simulation(config)
    wealth = [p.wealth for p in players]
    bankruptcies = sum(p.bankrupt for p in players)
    return np.mean(wealth), np.std(wealth), bankruptcies

def check_extreme_parameter(param_name, param_value, num_rounds, num_trials=30):
    results = []
    for _ in range(num_trials):
        config = GameConfig(num_rounds=num_rounds, num_trials=1, **{param_name: param_value})
        players = run_simulation(config)
        if param_name == 'noise':
            tft = [p for p in players if p.strategy.name == "TFT"]
            results.append(np.mean([p.wealth for p in tft]) if tft else 0)

    return np.mean(results)


def run_convergence(n_runs, strategies, num_rounds):
    data = {s: {'wealth': [], 'survival': []} for s in strategies}

    for n in range(1, n_runs + 1):
        if n % 20 == 0:
            print(f"  Run {n}/{n_runs}")

        config = GameConfig(num_rounds=num_rounds, num_trials=1)
        players = run_simulation(config)
        trial_result = analyze_trial(players)
        agg = aggregate_monte_carlo_results([trial_result])

        for s in strategies:
            if s in agg:
                data[s]['wealth'].append(agg[s]['wealth_mean'])
                data[s]['survival'].append(agg[s]['survival_mean'])

    for s in strategies:
        n = len(data[s]['wealth'])
        data[s]['wealth'] = np.cumsum(data[s]['wealth']) / np.arange(1, n + 1)
        data[s]['survival'] = np.cumsum(data[s]['survival']) / np.arange(1, n + 1)

    return data


def plot_convergence(data, strategies):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

    for s in strategies:
        n = len(data[s]['wealth'])
        ax1.plot(range(1, n + 1), data[s]['wealth'], linewidth=2, label=s)
        ax2.plot(range(1, n + 1), data[s]['survival'], linewidth=2, label=s)

    ax1.set_title("Wealth Convergence", fontsize=14)
    ax1.set_xlabel("Number of Runs")
    ax1.set_ylabel("Cumulative Average Wealth")
    ax1.legend()
    ax1.grid(alpha=0.3)

    ax2.set_title("Survival Rate Convergence", fontsize=14)
    ax2.set_xlabel("Number of Runs")
    ax2.set_ylabel("Cumulative Average Survival Rate")
    ax2.legend()
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig('convergence.png', dpi=300)


def validate():
    print("=" * 70)
    print("SANITY CHECKS")
    print("=" * 70)

    print("\n1. All Same Strategy")
    print("All AllC (everyone cooperates):")
    mean_w, std_w, bankruptcies = check_single_strategy('AllC', 80, 1000)
    print(f"  Avg wealth: {mean_w:.2f}, Std dev: {std_w:.2f}, Bankruptcies: {bankruptcies}")

    print("\nAll AllD (everyone defects):")
    mean_w, std_w, bankruptcies = check_single_strategy('AllD', 80, 1000)
    print(f"  Avg wealth: {mean_w:.2f}, Bankruptcies: {bankruptcies}")

    print("\n2. Zero Rounds")
    config = GameConfig(num_rounds=0, initial_wealth=100, num_trials=1)
    players = run_simulation(config)
    all_100 = all(p.wealth == 100 for p in players)
    no_bankrupt = all(not p.bankrupt for p in players)
    print(f"  All wealth = 100: {all_100}, No bankruptcies: {no_bankrupt}")

    print("\n3. Extreme Noise")
    print(f"No noise: TFT wealth = {check_extreme_parameter('noise', 0.0, 1000):.2f}")
    print(f"Full noise: TFT wealth = {check_extreme_parameter('noise', 1.0, 1000):.2f}")

    print("CONVERGENCE ANALYSIS")
    strategies = ['TFT', 'AllD', 'AllC']
    print(f"Running 100 iterations...")
    data = run_convergence(100, strategies, 500)

    plot_convergence(data, strategies)
    print("\nConvergence analysis complete. Saved to convergence.png")

    for s in strategies:
        if len(data[s]['wealth']) > 0:
            print(f"  {s}: wealth={data[s]['wealth'][-1]:.2f}, survival={data[s]['survival'][-1]:.2%}")

if __name__ == "__main__":
    validate()