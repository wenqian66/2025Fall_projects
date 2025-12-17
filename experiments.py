from config import create_h1_configs, create_h2_configs, create_h3_configs
from simulation import run_monte_carlo, aggregate_monte_carlo_results
import os
import matplotlib.pyplot as plt


def plot_comparison(x_data, y_data_dict, xlabel, ylabel, title, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    wealth_keys = list(y_data_dict['wealth'].keys())
    for label, data in y_data_dict['wealth'].items():
        marker = 'o' if label == wealth_keys[0] else 's'
        ax1.plot(x_data, data, marker=marker, linewidth=2, label=label)

    ax1.set_xlabel(xlabel)
    ax1.set_ylabel('Wealth')
    ax1.set_title(f'{title}: Wealth')
    ax1.legend()
    ax1.grid(alpha=0.3)

    survival_keys = list(y_data_dict['survival'].keys())
    for label, data in y_data_dict['survival'].items():
        marker = 'o' if label == survival_keys[0] else 's'
        ax2.plot(x_data, data, marker=marker, linewidth=2, label=label)

    ax2.set_xlabel(xlabel)
    ax2.set_ylabel('Survival Rate')
    ax2.set_title(f'{title}: Survival')
    ax2.legend()
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()



def run_h1_experiment():
    print("H1: REPUTATION SIGNAL STRENGTH")
    h1_configs = create_h1_configs()
    results = {}

    for signal_name, config in h1_configs.items():
        print(f"\n{signal_name}: alpha_c={config.alpha_c}, alpha_d={config.alpha_d}")
        res = run_monte_carlo(config)
        results[signal_name] = aggregate_monte_carlo_results(res)

    print("\n" + "*" * 70)
    print("H1 SUMMARY")
    print("*" * 70)
    print(f"{'Signal':20s} {'alpha_c':>8s} {'alpha_d':>8s} {'TFT':>12s} {'RA-TFT':>12s} {'Advantage':>12s}")

    for signal in results:
        config = h1_configs[signal]
        tft_w = results[signal]['TFT']['wealth_mean']
        ratft_w = results[signal]['Reputation Aware TFT']['wealth_mean']
        adv = (ratft_w - tft_w) / tft_w * 100
        print(f"{signal:20s} {config.alpha_c:>8.3f} {config.alpha_d:>8.3f} {tft_w:>12.2f} {ratft_w:>12.2f} {adv:>11.1f}%")

    signals = ['no_rep', 'weak_rep', 'weak_moderate_rep', 'moderate_rep', 'moderate_strong_rep', 'strong_rep']
    alpha_cs = [h1_configs[s].alpha_c for s in signals]

    y_data = {
        'wealth': {
            'RA-TFT': [results[s]['Reputation Aware TFT']['wealth_mean'] for s in signals],
            'TFT': [results[s]['TFT']['wealth_mean'] for s in signals]
        },
        'survival': {
            'RA-TFT': [results[s]['Reputation Aware TFT']['survival_mean'] for s in signals],
            'TFT': [results[s]['TFT']['survival_mean'] for s in signals]
        }
    }

    plot_comparison(alpha_cs, y_data, 'alpha_c', 'Wealth/Survival', 'H1', 'figures/h1_results.png')
    print("\nSaved: h1_results.png")
    return results


def run_h2_experiment():
    print("H2: NETWORK THRESHOLD")
    h2_configs = create_h2_configs()
    results = {}

    for threshold_name, config in h2_configs.items():
        print(f"\n{threshold_name}: K={config.network_threshold}")
        res = run_monte_carlo(config)
        results[threshold_name] = aggregate_monte_carlo_results(res)

    print("\n" + "*" * 70)
    print("H2 SUMMARY")
    print("*" * 70)
    print(f"{'Threshold':20s} {'K':>8s} {'CB Wealth':>12s} {'TFT Wealth':>12s} {'Advantage':>12s}")

    for threshold_name in results:
        config = h2_configs[threshold_name]
        cb_w = results[threshold_name]['Coalition Builder']['wealth_mean']
        tft_w = results[threshold_name]['TFT']['wealth_mean']
        adv = (cb_w - tft_w) / tft_w * 100
        print(f"{threshold_name:20s} {config.network_threshold:>8.1f} {cb_w:>12.2f} {tft_w:>12.2f} {adv:>11.1f}%")

    thresholds = ['very_easy', 'easy', 'moderate', 'moderate_hard', 'hard', 'very_hard']
    Ks = [h2_configs[t].network_threshold for t in thresholds]

    y_data = {
        'wealth': {
            'Coalition Builder': [results[t]['Coalition Builder']['wealth_mean'] for t in thresholds],
            'TFT': [results[t]['TFT']['wealth_mean'] for t in thresholds]
        },
        'survival': {
            'Coalition Builder': [results[t]['Coalition Builder']['survival_mean'] for t in thresholds],
            'TFT': [results[t]['TFT']['survival_mean'] for t in thresholds]
        }
    }

    plot_comparison(Ks, y_data, 'K', 'Wealth/Survival', 'H2', 'figures/h2_results.png')
    print("\nSaved: h2_results.png")
    return results


def run_h3_experiment():
    print("H3: NOISE EFFECT ON COOPERATION")
    h3_configs = create_h3_configs()
    results = {}

    for config_name, config in h3_configs.items():
        print(f"\n{config_name}: noise={config.noise}")
        res = run_monte_carlo(config)
        results[config_name] = aggregate_monte_carlo_results(res)

    print("\n" + "*" * 70)
    print("H3 SUMMARY")
    print("*" * 70)
    print(f"{'Noise':>10s} {'RATFT_Wealth':>15s} {'CB_Wealth':>12s} {'AllC_Wealth':>12s} {'RATFT_Survival':>15s} {'CB_Survival':>15s}")

    for config_name in sorted(results.keys()):
        noise_val = h3_configs[config_name].noise
        data = results[config_name]
        ratft_w = data['Reputation Aware TFT']['wealth_mean'] if 'Reputation Aware TFT' in data else 0
        cb_w = data['Coalition Builder']['wealth_mean'] if 'Coalition Builder' in data else 0
        allc_w = data['AllC']['wealth_mean'] if 'AllC' in data else 0
        ratft_s = data['Reputation Aware TFT']['survival_mean'] if 'Reputation Aware TFT' in data else 0
        cb_s = data['Coalition Builder']['survival_mean'] if 'Coalition Builder' in data else 0
        print(f"{noise_val:>10.2f} {ratft_w:>14.2f} {cb_w:>12.2f} {allc_w:>12.2f} {ratft_s:>14.2%} {cb_s:>14.2%}")

    noises = sorted([h3_configs[k].noise for k in h3_configs.keys()])
    configs_sorted = [f'noise_{int(n*100):02d}' for n in noises]

    y_data = {
        'wealth': {
            'RA-TFT': [results[c]['Reputation Aware TFT']['wealth_mean'] for c in configs_sorted],
            'Coalition Builder': [results[c]['Coalition Builder']['wealth_mean'] for c in configs_sorted],
            'AllC': [results[c]['AllC']['wealth_mean'] for c in configs_sorted]
        },
        'survival': {
            'RA-TFT': [results[c]['Reputation Aware TFT']['survival_mean'] for c in configs_sorted],
            'Coalition Builder': [results[c]['Coalition Builder']['survival_mean'] for c in configs_sorted],
            'AllC': [results[c]['AllC']['survival_mean'] for c in configs_sorted]
        }
    }

    plot_comparison(noises, y_data, 'Noise Level', 'Wealth/Survival', 'H3', 'figures/h3_results.png')
    print("\nSaved: h3_results.png")
    return results


def run_all_experiments():
    h1 = run_h1_experiment()
    h2 = run_h2_experiment()
    h3 = run_h3_experiment()
    return {'H1': h1, 'H2': h2, 'H3': h3}


if __name__ == "__main__":
    run_all_experiments()
