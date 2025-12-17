from config import create_h1_configs, create_h2_configs, create_h3_configs
from simulation import run_monte_carlo, aggregate_monte_carlo_results
import matplotlib.pyplot as plt
import numpy as np


def run_h1_experiment():
    print("=" * 70)
    print("H1: REPUTATION SIGNAL STRENGTH")
    print("=" * 70)

    h1_configs = create_h1_configs()
    results = {}

    for signal_name, config in h1_configs.items():
        print(f"\n{signal_name}: alpha_c={config.alpha_c}, alpha_d={config.alpha_d}")
        res = run_monte_carlo(config)
        results[signal_name] = aggregate_monte_carlo_results(res)

    print("\n" + "=" * 70)
    print("H1 SUMMARY")
    print("=" * 70)
    print(f"{'Signal':20s} {'alpha_c':>8s} {'alpha_d':>8s} {'TFT':>12s} {'RA-TFT':>12s} {'Advantage':>12s}")

    for signal in results:
        config = h1_configs[signal]
        tft_w = results[signal]['TFT']['wealth_mean']
        ratft_w = results[signal]['Reputation Aware TFT']['wealth_mean']
        adv = (ratft_w - tft_w) / tft_w * 100
        print(
            f"{signal:20s} {config.alpha_c:>8.3f} {config.alpha_d:>8.3f} {tft_w:>12.2f} {ratft_w:>12.2f} {adv:>11.1f}%")

    signals = ['no_rep', 'weak_rep', 'weak_moderate_rep', 'moderate_rep', 'moderate_strong_rep', 'strong_rep']
    alpha_cs = [h1_configs[s].alpha_c for s in signals]
    tft_wealth = [results[s]['TFT']['wealth_mean'] for s in signals]
    ratft_wealth = [results[s]['Reputation Aware TFT']['wealth_mean'] for s in signals]
    tft_survival = [results[s]['TFT']['survival_mean'] for s in signals]
    ratft_survival = [results[s]['Reputation Aware TFT']['survival_mean'] for s in signals]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    ax1.plot(alpha_cs, ratft_wealth, marker='o', linewidth=2, label='RA-TFT', color='#355C7D')
    ax1.plot(alpha_cs, tft_wealth, marker='s', linewidth=2, label='TFT', color='#99B898')
    ax1.set_xlabel('alpha_c')
    ax1.set_ylabel('Wealth')
    ax1.set_title('H1: Wealth by Reputation Signal')
    ax1.legend()
    ax1.grid(alpha=0.3)

    ax2.plot(alpha_cs, ratft_survival, marker='o', linewidth=2, label='RA-TFT', color='#355C7D')
    ax2.plot(alpha_cs, tft_survival, marker='s', linewidth=2, label='TFT', color='#99B898')
    ax2.set_xlabel('alpha_c')
    ax2.set_ylabel('Survival Rate')
    ax2.set_title('H1: Survival by Reputation Signal')
    ax2.legend()
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig('h1_results.png', dpi=300)
    plt.close()
    print("\nSaved: h1_results.png")

    return results


def run_h2_experiment():
    print("\n" + "=" * 70)
    print("H2: NETWORK THRESHOLD")
    print("=" * 70)

    h2_configs = create_h2_configs()
    results = {}

    for threshold_name, config in h2_configs.items():
        print(f"\n{threshold_name}: K={config.network_threshold}")
        res = run_monte_carlo(config)
        results[threshold_name] = aggregate_monte_carlo_results(res)

    print("\n" + "=" * 70)
    print("H2 SUMMARY")
    print("=" * 70)
    print(f"{'Threshold':20s} {'K':>8s} {'CB Wealth':>12s} {'TFT Wealth':>12s} {'Advantage':>12s}")

    for threshold_name in results:
        config = h2_configs[threshold_name]
        cb_w = results[threshold_name]['Coalition Builder']['wealth_mean']
        tft_w = results[threshold_name]['TFT']['wealth_mean']
        adv = (cb_w - tft_w) / tft_w * 100
        print(f"{threshold_name:20s} {config.network_threshold:>8.1f} {cb_w:>12.2f} {tft_w:>12.2f} {adv:>11.1f}%")

    thresholds = ['very_easy', 'easy', 'moderate', 'moderate_hard', 'hard', 'very_hard']
    Ks = [h2_configs[t].network_threshold for t in thresholds]
    cb_wealth = [results[t]['Coalition Builder']['wealth_mean'] for t in thresholds]
    tft_wealth = [results[t]['TFT']['wealth_mean'] for t in thresholds]
    cb_survival = [results[t]['Coalition Builder']['survival_mean'] for t in thresholds]
    tft_survival = [results[t]['TFT']['survival_mean'] for t in thresholds]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    ax1.plot(Ks, cb_wealth, marker='o', linewidth=2, label='Coalition Builder', color='#355C7D')
    ax1.plot(Ks, tft_wealth, marker='s', linewidth=2, label='TFT', color='#99B898')
    ax1.set_xlabel('K')
    ax1.set_ylabel('Wealth')
    ax1.set_title('H2: Wealth by Network Threshold')
    ax1.legend()
    ax1.grid(alpha=0.3)

    ax2.plot(Ks, cb_survival, marker='o', linewidth=2, label='Coalition Builder', color='#355C7D')
    ax2.plot(Ks, tft_survival, marker='s', linewidth=2, label='TFT', color='#99B898')
    ax2.set_xlabel('K')
    ax2.set_ylabel('Survival Rate')
    ax2.set_title('H2: Survival by Network Threshold')
    ax2.legend()
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig('h2_results.png', dpi=300)
    plt.close()
    print("\nSaved: h2_results.png")

    return results


def run_h3_experiment():
    print("\n" + "=" * 70)
    print("H3: NOISE EFFECT ON COOPERATION")
    print("=" * 70)

    h3_configs = create_h3_configs()
    results = {}

    for config_name, config in h3_configs.items():
        print(f"\n{config_name}: noise={config.noise}")
        res = run_monte_carlo(config)
        results[config_name] = aggregate_monte_carlo_results(res)

    print("\n" + "=" * 70)
    print("H3 SUMMARY")
    print("=" * 70)
    print(f"{'Noise':>10s} {'CC_Survival':>15s} {'CC_Wealth':>12s} {'AllC_Survival':>15s} {'AllC_Wealth':>12s}")

    for config_name in sorted(results.keys()):
        noise_val = h3_configs[config_name].noise
        data = results[config_name]

        cond_coop = ['TFT', 'GTFT', 'GRIM']
        cond_coop_data = [data[s] for s in cond_coop if s in data]

        cc_survival = np.mean([s['survival_mean'] for s in cond_coop_data]) if cond_coop_data else 0
        cc_wealth = np.mean([s['wealth_mean'] for s in cond_coop_data]) if cond_coop_data else 0

        allc_survival = data['AllC']['survival_mean'] if 'AllC' in data else 0
        allc_wealth = data['AllC']['wealth_mean'] if 'AllC' in data else 0

        print(f"{noise_val:>10.2f} {cc_survival:>14.2%} {cc_wealth:>12.2f} {allc_survival:>14.2%} {allc_wealth:>12.2f}")

    noises = sorted([h3_configs[k].noise for k in h3_configs.keys()])
    configs_sorted = [f'noise_{int(n * 100):02d}' for n in noises]

    cc_wealth_list = []
    cc_survival_list = []
    allc_wealth_list = []
    allc_survival_list = []

    for config_name in configs_sorted:
        data = results[config_name]
        cond_coop = ['TFT', 'GTFT', 'GRIM']
        cond_coop_data = [data[s] for s in cond_coop if s in data]

        cc_wealth_list.append(np.mean([s['wealth_mean'] for s in cond_coop_data]) if cond_coop_data else 0)
        cc_survival_list.append(np.mean([s['survival_mean'] for s in cond_coop_data]) if cond_coop_data else 0)
        allc_wealth_list.append(data['AllC']['wealth_mean'] if 'AllC' in data else 0)
        allc_survival_list.append(data['AllC']['survival_mean'] if 'AllC' in data else 0)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    ax1.plot(noises, cc_wealth_list, marker='o', linewidth=2, label='Cond Cooperators', color='#355C7D')
    ax1.plot(noises, allc_wealth_list, marker='s', linewidth=2, label='AllC', color='#99B898')
    ax1.set_xlabel('Noise Level')
    ax1.set_ylabel('Wealth')
    ax1.set_title('H3: Wealth by Noise Level')
    ax1.legend()
    ax1.grid(alpha=0.3)

    ax2.plot(noises, cc_survival_list, marker='o', linewidth=2, label='Cond Cooperators', color='#355C7D')
    ax2.plot(noises, allc_survival_list, marker='s', linewidth=2, label='AllC', color='#99B898')
    ax2.set_xlabel('Noise Level')
    ax2.set_ylabel('Survival Rate')
    ax2.set_title('H3: Survival by Noise Level')
    ax2.legend()
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig('h3_results.png', dpi=300)
    plt.close()

    print("\nSaved: h3_results.png")
    return results


def run_all_experiments():
    h1 = run_h1_experiment()
    h2 = run_h2_experiment()
    h3 = run_h3_experiment()
    return {'H1': h1, 'H2': h2, 'H3': h3}


if __name__ == "__main__":
    run_all_experiments()
