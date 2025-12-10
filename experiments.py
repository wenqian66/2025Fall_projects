from config import H1_CONFIGS, H2_NETWORK_THRESHOLDS, H3_CONFIGS, H3_WELFARE_LEVELS
from simulation import run_monte_carlo, aggregate_monte_carlo_results
from utils import print_results_with_ci



def run_h1_experiment():
    print("=" * 70)
    print("H1: TFT vs RA-TFT across reputation signal strengths")
    print("=" * 70)

    results = {}
    for signal_name, config in H1_CONFIGS.items():
        print(f"\n{signal_name}: alpha_c={config['alpha_c']}, alpha_d={config['alpha_d']}")
        res = run_monte_carlo(config)
        agg = aggregate_monte_carlo_results(res)
        results[signal_name] = agg
        print_results_with_ci(agg)

    print("\n" + "=" * 70)
    print("H1 SUMMARY")
    print("=" * 70)
    print(f"{'Signal':15s} {'alpha_c':>8s} {'alpha_d':>8s} {'TFT':>12s} {'RA-TFT':>12s} {'Advantage':>12s}")
    print("-" * 70)
    for signal in results:
        config = H1_CONFIGS[signal]
        tft_w = results[signal]['TFT']['wealth_mean']
        ratft_w = results[signal]['Reputation Aware TFT']['wealth_mean']
        adv = (ratft_w - tft_w) / tft_w * 100
        print(
            f"{signal:15s} {config['alpha_c']:>8.3f} {config['alpha_d']:>8.3f} {tft_w:>12.2f} {ratft_w:>12.2f} {adv:>11.1f}%")

    return results


def run_h2_experiment():
    print("\n" + "=" * 70)
    print("H2: NETWORK THRESHOLD EFFECT")
    print("=" * 70)

    h2_results = {}

    for threshold_name, config in H2_NETWORK_THRESHOLDS.items():
        K = config['network_threshold']
        print(f"\n{'=' * 70}")
        print(f"Testing: {threshold_name} (K={K})")
        print(f"{'=' * 70}")

        results = run_monte_carlo(config)
        aggregated = aggregate_monte_carlo_results(results)
        h2_results[threshold_name] = aggregated

        print_results_with_ci(aggregated)

        max_wealth = max(s['wealth_mean'] for s in aggregated.values())
        winner = [name for name, s in aggregated.items() if s['wealth_mean'] == max_wealth][0]
        print(f"\n>>> Highest wealth: {winner} ({max_wealth:.2f})")

    print("\n" + "=" * 70)
    print("H2 SUMMARY: Network Threshold vs Coalition Builder Performance")
    print("=" * 70)
    print(f"{'Threshold':20s} {'K':>8s} {'CB Wealth':>12s} {'CB Survival':>15s} {'Highest Strategy':>20s}")
    print("-" * 70)

    for threshold_name, config in H2_NETWORK_THRESHOLDS.items():
        if threshold_name in h2_results:
            data = h2_results[threshold_name]
            K = config['network_threshold']

            if 'Coalition Builder' in data:
                cb_wealth = data['Coalition Builder']['wealth_mean']
                cb_survival = data['Coalition Builder']['survival_mean']
            else:
                cb_wealth = 0
                cb_survival = 0

            max_wealth = max(s['wealth_mean'] for s in data.values())
            winner = [name for name, s in data.items() if s['wealth_mean'] == max_wealth][0]

            print(f"{threshold_name:20s} {K:>8.1f} {cb_wealth:>12.2f} {cb_survival:>14.2%} {winner:>20s}")

    return h2_results


def run_h3_experiment():
    print("\n" + "=" * 70)
    print("H3: WELFARE LEVELS UNDER HIGH NOISE")
    print("=" * 70)

    h3_results = {}

    for config_name, config in H3_CONFIGS.items():
        welfare = config['welfare']
        print(f"\n{'=' * 70}")
        print(f"Testing: {config_name} (welfare={welfare:.2f}, noise={config['noise']})")
        print(f"{'=' * 70}")

        results = run_monte_carlo(config)
        aggregated = aggregate_monte_carlo_results(results)
        h3_results[config_name] = aggregated

        print_results_with_ci(aggregated)

        cond_coop = ['TFT', 'GTFT', 'Grim']
        cond_coop_data = [aggregated[s] for s in cond_coop if s in aggregated]
        if cond_coop_data:
            avg_survival = sum(s['survival_mean'] for s in cond_coop_data) / len(cond_coop_data)
            avg_wealth = sum(s['wealth_mean'] for s in cond_coop_data) / len(cond_coop_data)
            print(f"\n>>> Conditional Cooperators: Survival={avg_survival:.2%}, Wealth={avg_wealth:.2f}")

        if 'AllC' in aggregated:
            allc = aggregated['AllC']
            print(f">>> AllC: Survival={allc['survival_mean']:.2%}, Wealth={allc['wealth_mean']:.2f}")

    print("\n" + "=" * 70)
    print("H3 SUMMARY: Welfare Effects on Conditional Cooperators vs AllC")
    print("=" * 70)
    print(f"{'Welfare':>10s} {'CC_Survival':>15s} {'CC_Wealth':>12s} {'AllC_Survival':>15s} {'AllC_Wealth':>12s}")
    print("-" * 70)

    for config_name in sorted(h3_results.keys()):
        welfare = H3_CONFIGS[config_name]['welfare']
        data = h3_results[config_name]

        cond_coop = ['TFT', 'GTFT', 'Grim']
        cond_coop_data = [data[s] for s in cond_coop if s in data]
        if cond_coop_data:
            cc_survival = sum(s['survival_mean'] for s in cond_coop_data) / len(cond_coop_data)
            cc_wealth = sum(s['wealth_mean'] for s in cond_coop_data) / len(cond_coop_data)
        else:
            cc_survival = 0
            cc_wealth = 0

        allc_survival = data['AllC']['survival_mean'] if 'AllC' in data else 0
        allc_wealth = data['AllC']['wealth_mean'] if 'AllC' in data else 0

        print(f"{welfare:>10.2f} {cc_survival:>14.2%} {cc_wealth:>12.2f} {allc_survival:>14.2%} {allc_wealth:>12.2f}")

    return h3_results


def run_all_experiments():
    print("\n" + "=" * 70)
    print("RUNNING ALL EXPERIMENTS")
    print("=" * 70)

    h1_results = run_h1_experiment()
    h2_results = run_h2_experiment()
    h3_results = run_h3_experiment()

    print("\n" + "=" * 70)
    print("ALL EXPERIMENTS COMPLETED")
    print("=" * 70)

    return {
        'H1': h1_results,
        'H2': h2_results,
        'H3': h3_results,
    }


if __name__ == "__main__":
    all_results = run_all_experiments()