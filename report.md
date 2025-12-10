```
┌───────────────────────────────────────────────────────────┐
│                         experiments.py                    │
│  • run_h1_experiment()                                    │
│  • run_h2_experiment()                                    │
│  • run_h3_experiment()                                    │
│  • run_all_experiments()                                  │
│-----------------------------------------------------------│
│  Calls run_monte_carlo() to run batches of experiments    │
│  and prints summary tables                                 │
└───────────────▲───────────────────────────────┬──────────┘
│                               │
│ monte-carlo trial results      │
│                               ▼
┌───────────────────────────────────────────────────────────┐
│                         simulation.py                     │
│  • run_monte_carlo()                                      │
│  • run_simulation()                                       │
│  • play_round()                                           │
│  • analyze_trial() / aggregate_results()                  │
│  • random_pairing()                                       │
│                                                           │
│   Controls the simulation pipeline:                       │
│   1. Create all players                                   │
│   2. Randomly pair active players each round              │
│   3. Call play_round                                      │
│   4. Repeat for n_rounds                                  │
│   5. Aggregate Monte-Carlo results                         │
└───────────────▲───────────────────────────────┬──────────┘
│  calls                        │ calls
│                               │
▼                               ▼
┌───────────────────────────────────────────────────────────┐
│                          player.py                        │
│  • OpponentView                                            │
│  • AllC / AllD / TFT / GTFT / Grim / RAND                  │
│  • ReputationAwareTFT                                      │
│  • CoalitionBuilder                                        │
│  • STRATEGY_MAP                                            │
│                                                           │
│  Defines all “agents”:                                    │
│  strategies read only from OpponentView                    │
│  PlayerWrapper turns strategy classes into actual players  │
└───────────────▲───────────────────────────────┘
│ OpponentView + actions
│
▼
┌───────────────────────────────────────────────────────────┐
│                       environment.py                      │
│  • apply_noise()                                          │
│  • update_payoff()                                        │
│  • update_reputation()                                    │
│  • update_network()                                       │
│  • update_bankruptcy()                                    │
│  • update_all()                                           │
│                                                           │
│   World rules: updates player states after each round      │
│   1. Noise                                                 │
│   2. Payoff                                                │
│   3. Reputation                                            │
│   4. Network weight                                        │
│   5. Bankruptcy + welfare                                  │
└───────────────────────────────────────────────────────────┘

``` 
```

======================================================================
H1 SUMMARY
H1: When reputation information is available, ReputationAwareTFT (RA-TFT) will outperform standard TFT.

results show a strong non-linear effect
Reputation information benefits adaptive strategies only under **weak-to-moderate signals**.
Strong reputation signals destroy cooperation, that too much sensitivity makes cooperation collapse.
======================================================================
Signal           alpha_c  alpha_d          TFT       RA-TFT    Advantage
----------------------------------------------------------------------
no_rep             0.000    0.000      3931.22      3914.48        -0.4%
weak_rep           0.005    0.010      2217.30      3218.76        45.2%
moderate_rep       0.020    0.040      4284.41       175.85       -95.9%
strong_rep         0.050    0.100      5758.89        92.73       -98.4%

======================================================================
H2 SUMMARY: Network Threshold vs Coalition Builder Performance
H2: When network and reputation information are available, Coalition Builder will achieve the highest payoff among all strategies
When the threshold is low, Most network weights quickly exceed 3, Coalition Builder ends up cooperating with almost everyone.
With moderate to high thresholds, selectively forms stable coalitions with reliable partners. against unreliable players (AllD, Random), protecting itself.
Supported, network memory is a powerful tool for building stable cooperative clusters while avoiding exploiters.
======================================================================
Threshold                   K    CB Wealth     CB Survival     Highest Strategy
----------------------------------------------------------------------
easy_coalition            3.0     12015.98         83.90%                 AllC
moderate_coalition        5.0     12441.33         86.40%    Coalition Builder
hard_coalition            8.0     12313.26         85.80%    Coalition Builder
very_hard_coalition      12.0     12315.40         86.20%    Coalition Builder

======================================================================
H3 SUMMARY: Welfare Effects on Conditional Cooperators vs AllC
H3: Moderate welfare (β=0.05) helps conditional cooperators survive high noise (ε=0.15), but large welfare (β≥0.15) enables unconditional cooperators (AllC) to survive exploitation.
However, results do not support this hypothesis.
Survival outcomes remain nearly unchanged across β ∈ [0.00, 0.40]:

Possible
R1:Welfare is too small to matter?
R2:I want to test the hypothesis in a hash envrionment, not hash enough? AllC already survives well without welfare, too forgiving 41–46% survival?
R3:reject H3, welfare not efficient under high noise, like elfare is simply too weak to counteract the systemic and persistent disruptions caused by high noise.

TODO: why failed, which strategies rely most heavily on welfare, how many additional rounds of survival welfare actually provides for bankrupt players
======================================================================
   Welfare     CC_Survival    CC_Wealth   AllC_Survival  AllC_Wealth
----------------------------------------------------------------------
      0.00         31.07%       935.64         45.20%      1742.76
      0.10         30.87%       979.37         45.60%      1805.35
      0.20         29.87%       958.53         46.00%      1905.59
      0.30         30.33%       978.16         41.00%      1735.43
      0.40         29.73%       922.03         41.80%      1656.02
```



