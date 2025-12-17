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

