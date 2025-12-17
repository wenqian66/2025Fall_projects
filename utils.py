import numpy as np

def print_results_with_ci(aggregated):
    for strategy, stats in aggregated.items():
        survival_ci = 1.96 * stats['survival_std'] / np.sqrt(stats['n_trials'])
        wealth_ci = 1.96 * stats['wealth_std'] / np.sqrt(stats['n_trials'])
        print(f"{strategy:20s}: "
              f"Survival={stats['survival_mean']:.2%} ±{survival_ci:.2%}, "
              f"Wealth={stats['wealth_mean']:.2f} ±{wealth_ci:.2f}")




