from config import DEFAULT_PARAMS
import numpy as np

def _prepare_params(params, kwargs):
    if params is None:
        params = DEFAULT_PARAMS.copy()
    params = params.copy()
    params.update(kwargs)
    return params

def print_results_with_ci(aggregated):
    """Print results with 95% confidence intervals"""
    for strategy, stats in aggregated.items():
        survival_ci = 1.96 * stats['survival_std'] / np.sqrt(stats['n_trials'])
        wealth_ci = 1.96 * stats['wealth_std'] / np.sqrt(stats['n_trials'])
        print(f"{strategy:20s}: "
              f"Survival={stats['survival_mean']:.2%} ±{survival_ci:.2%}, "
              f"Wealth={stats['wealth_mean']:.2f} ±{wealth_ci:.2f}")




