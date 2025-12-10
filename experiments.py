import numpy as np
import pandas as pd
from simulation import run_monte_carlo, run_simulation
from player import TFT, ReputationAwareTFT



def experiment_h1():
    print("=" * 60)
    print("H1: RA-TFT outperforms TFT in average payoff")
    print("=" * 60)

    results = run_monte_carlo(
        n_trials=1000,
        strategy_classes=[TFT, ReputationAwareTFT],
        copies_per_strategy=5,
        rounds=10000,
        noise=0.05
    )

    summary = aggregate_monte_carlo(results)
    print(summary)
    summary.to_csv('h1_results.csv', index=False)

    tft_wealth = summary[summary['strategy'] == 'TFT']['wealth_mean'].values[0]
    ratft_wealth = summary[summary['strategy'] == 'Reputation Aware TFT']['wealth_mean'].values[0]
    print(f"\nH1 supported: {ratft_wealth > tft_wealth}")

    return summary


def experiment_h2():
    print("=" * 60)
    print("H2: Coalition Builder achieves highest average payoff")
    print("=" * 60)

    results = run_monte_carlo(
        n_trials=1000,
        rounds=10000,
        noise=0.05
    )

    summary = aggregate_monte_carlo(results)
    summary = summary.sort_values('wealth_mean', ascending=False)
    print(summary)
    summary.to_csv('h2_results.csv', index=False)

    top_strategy = summary.iloc[0]['strategy']
    print(f"\nH2 supported: {top_strategy == 'Coalition Builder'}")

    return summary


def calculate_h3_metrics(players):
    conditional_strategies = ['TFT', 'GTFT', 'Grim']

    conditional_players = [p for p in players if p.strategy.name in conditional_strategies]
    cond_survived = sum(1 for p in conditional_players if not p.bankrupt)
    cond_survival_rate = cond_survived / len(conditional_players) if conditional_players else 0

    allc_players = [p for p in players if p.strategy.name == 'AllC']
    allc_survived = sum(1 for p in allc_players if not p.bankrupt)
    allc_survival_rate = allc_survived / len(allc_players) if allc_players else 0

    allc_exploitation_count = 0
    allc_total_interactions = 0
    for p in allc_players:
        for opp_id, actions in p.opp_history.items():
            opp = next((o for o in players if o.id == opp_id), None)
            if opp:
                if opp.strategy.name == 'AllD':
                    allc_exploitation_count += len(actions)
                allc_total_interactions += len(actions)

    exploitation_rate = allc_exploitation_count / allc_total_interactions if allc_total_interactions > 0 else 0

    survivors = [p for p in players if not p.bankrupt]
    avg_survivor_wealth = np.mean([p.wealth for p in survivors]) if survivors else 0

    return {
        'cond_survival_rate': cond_survival_rate,
        'allc_survival_rate': allc_survival_rate,
        'exploitation_rate': exploitation_rate,
        'avg_survivor_wealth': avg_survivor_wealth
    }


def experiment_h3():
    print("=" * 60)
    print("H3: Welfare paradox under high noise")
    print("=" * 60)

    welfare_levels = [0, 0.05, 0.10, 0.15, 0.20]
    all_results = []

    for welfare in welfare_levels:
        print(f"\nWelfare={welfare}")

        trial_metrics = []
        for trial in range(100):
            if trial % 20 == 0:
                print(f"  Trial {trial}/100")

            players = run_simulation(
                rounds=5000,
                noise=0.15,
                welfare=welfare
            )

            metrics = calculate_h3_metrics(players)
            trial_metrics.append(metrics)

        df_trials = pd.DataFrame(trial_metrics)
        welfare_summary = {
            'welfare': welfare,
            'cond_survival_mean': df_trials['cond_survival_rate'].mean(),
            'cond_survival_std': df_trials['cond_survival_rate'].std(),
            'allc_survival_mean': df_trials['allc_survival_rate'].mean(),
            'allc_survival_std': df_trials['allc_survival_rate'].std(),
            'exploitation_mean': df_trials['exploitation_rate'].mean(),
            'exploitation_std': df_trials['exploitation_rate'].std(),
            'avg_wealth_mean': df_trials['avg_survivor_wealth'].mean(),
            'avg_wealth_std': df_trials['avg_survivor_wealth'].std()
        }
        all_results.append(welfare_summary)

    df_results = pd.DataFrame(all_results)
    print("\n" + "=" * 60)
    print(df_results)
    df_results.to_csv('h3_results.csv', index=False)

    optimal_idx = df_results['cond_survival_mean'].idxmax()
    optimal_welfare = df_results.loc[optimal_idx, 'welfare']
    print(f"\nOptimal welfare for conditional cooperators: {optimal_welfare}")

    high_welfare = df_results[df_results['welfare'] >= 0.15]
    if not high_welfare.empty:
        high_welfare_exploitation = high_welfare['exploitation_mean'].mean()
        print(f"High welfare (≥0.15) exploitation rate: {high_welfare_exploitation:.2%}")
        print(f"H3 supported: {optimal_welfare == 0.05 and high_welfare_exploitation > 0.6}")

    return df_results


if __name__ == "__main__":
    h1_results = experiment_h1()
    h2_results = experiment_h2()
    h3_results = experiment_h3()
    print("\nAll experiments completed")