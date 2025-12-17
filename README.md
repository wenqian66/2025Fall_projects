# **Steal or Refrain: A Monte Carlo Simulation of Repeated Cooperation and Defection**

**Team Member:**
Wenqian Chen

**Project Type:**
Type I: Formal Critique and Improvement of a Published Data Analysis

---

## **Project Description**

This project critiques and substantially extends prior open-source Prisoner's Dilemma simulations. 

**Limitations of existing simulations:**
* Round-robin pairing 
* Simplified noise models
* Classical strategies only (TFT, GRIM, AllC, AllD)
* No environmental information systems

**This project adds:**
* Reputation system tracking cooperation history (information only)
* Network weights capturing pairwise relationship strength
* Wealth dynamics with bankruptcy and welfare recovery
* New strategies (RA-TFT, Coalition Builder) that exploit 
  environmental information through **selective cooperation**

Players interact over 10,000(default) rounds. Monte Carlo trials evaluate how environmental mechanisms alter strategic equilibria beyond classical PD results.

---

## **Base Payoff Matrix**

|               | B Refrain (C) | B Steal (D) |
| ------------- |---------------|-------------|
| A Refrain (C) | (2, 2)        | (-5, 6)     |
| A Steal (D)   | (6, -5)       | (-4, -4)    |

The matrix follows the classcial Prisoner’s Dilemma problem requirements:   $T > R > P > S \quad \text{and} \quad 2R > T + S$

---

## **Rules**

### **Base Rules**
1. Two players paired for T rounds (default: 10,000)
2. Each round: choose Refrain (C) or Steal (D)
3. Payoffs follow base matrix
4. Players observe opponent history(local) and reputation(global)
5. Strategies fixed within simulation


### **New Environmental Rules**

**6. Reputation System**

$$r_i \leftarrow \min(r_{\max}, r_i + \alpha_c) \quad \text{after cooperation}$$
$$r_i \leftarrow \max(r_{\min}, r_i - \alpha_d) \quad \text{after defection}$$

- **Observable by all players**
- **Does not affect matching probability**
- **Only RA-TFT strategy use this information, others ignore it (TFT, AllC, AllD, etc)**

**7. Network-Based Information**

Each pair maintains edge weight $w(i,j)$:

$$w(i,j) \leftarrow w(i,j) + \gamma \quad \text{after cooperation}$$
$$w(i,j) \leftarrow \max(0, w(i,j) - \delta) \quad \text{after defection}$$

- **Observable by all players**
- **Does not affect matching probability**
- **Only Coalition Builder strategy use this information, others ignore it**

**8. Wealth & Bankruptcy**

$$W_i \leftarrow W_i + \pi_i$$

If $W_i < W_{\text{threshold}}$, player exits pool temporarily.

**9. Welfare Recovery**

$$W_i \leftarrow W_i + \beta \quad \text{if } W_i < W_{\text{threshold}}$$

where $\beta = 0.05$ (fixed welfare per round, 0.05 as defaul).

Mirrors real-world safety nets (unemployment insurance, welfare).

#### **Matching Algorithm**
**Pure random pairing via random.shuffle()**, each round:
1. Shuffle all active (non-bankrupt) players
2. Pair adjacent players: (players[0], players[1]), (players[2], players[3])...
3. Unpaired player (if odd number) sits out that round

**Critical Design Choice:**
1. Reputation and network are **information only**
2. Matching is **not** affected by reputation/network weights
3. Assortative matching emerges through **strategic behavior** 
  (Coalition Builder selectively cooperates), not system-imposed 
  preferential pairing

---

## **Strategies**

### **Baseline Strategies**
1. **AllC**: Always cooperate
2. **AllD**: Always defect
3. **TFT**: Tit-for-tat, start by cooperating, then mirror opponent's last move
4. **GRIM**: Cooperate until first defection, then always defect
5. **GTFT**: Forgiving TFT (forgiveness probability p)
6. **RAND**: Random 50/50

### **New Strategies**

**7. Reputation-Aware TFT (RA-TFT)**

$$
\text{Action} =
\begin{cases}
\text{GTFT}, & \text{if } r_j > r_{\text{threshold1}}, \\[6pt]
\text{TFT},  & \text{if } r_{\text{threshold2}} < r_j \le r_{\text{threshold1}}, \\[6pt]
D,           & \text{if } r_j \le r_{\text{threshold2}} 
\end{cases}
$$


Integrates reputation into TFT logic. 

**8. Coalition Builder**

Identifies allies using network edge weights:

$$
\text{Action}(i,j) = 
\begin{cases}
C, & \text{if } w(i,j) \geq K_{\text{threshold}} \text{ (high-trust partner)} \\
\text{TFT}, & \text{otherwise (new partner)}
\end{cases}
$$

**Mechanism:**
- Cooperates unconditionally with high-trust partners ($w \geq K$)
- Uses TFT with new partners

---

## **Randomized Variables**
* Player pairing (random.shuffle() each round)
* Action noise ε (move flip probability)
  - Default: ε = 0.05 (5% error rate)
  - High-noise treatment (H3): ε = 0.15
  - Models miscommunication/signal errors

## **Controlled Variables**
* Payoff matrix
* Initial wealth W₀ = 10.0 (equal start for all players)
* Monte Carlo trials (N = 1000)
* GTFT forgiveness p
* Reputation weights $\alpha_c, \alpha_d$
* Network weights $\gamma, \delta$
* Broke threshold $W_{\text{threshold}}$
* Welfare amount β
* Coalition threshold K

---

## **Three Phases**

### **Phase 1: Design**

Components:
* Base PD model (Steal/Refrain)
* Reputation system
* Network matching
* Wealth/bankruptcy mechanics
* Welfare recovery

### **Phase 2: Validation**

**Technical Checks:**
* AllC vs AllC → (0.5, 0.5)
* AllD vs AllD → (0, 0)
* TFT vs TFT (no noise) → full cooperation
* Reputation increases/decreases correctly
* Network clusters form
* Welfare recovery functions

**Classical PD Verification:**
Confirm B1-B5 using baseline strategies only (sanity check, not contribution).

**Baseline Hypotheses (Well-Established, Verification Only)**

**B1.** GRIM optimal in random pairing  
**B2.** TFT/GTFT > AllC when defectors present  
**B3.** GTFT > TFT when noise increases  
**B4.** AllD exploits naive cooperators early  
**B5.** Higher cooperation reward → more cooperation  

### **Phase 3: Experiments**

---

**Novel Hypotheses (Core Contributions)**

**H1**: When reputation information is available, RA-TFT will outperform 
standard TFT.

$$
(\alpha_c,\,\alpha_d)\in
\left\{
(0,0),\;
(0.005,\,0.01),\;
(0.02,\,0.04),\;
(0.05,\,0.10)
\right\}.
$$


**H2**: When reputation and network information are available, Coalition 
Builder will achieve best among all strategies(8).

$$
K \in {3,5,8,12}.$$
**H3**: Moderate welfare (β=0.05) helps conditional cooperators survive high-noise(ε=0.15) 
environments, but excessive welfare (β≥0.15) enables unconditional cooperators 
(AllC) to persist despite chronic exploitation, benefiting defectors (AllD) 
and reducing mutual cooperation rates.

*Test:* β = 0, 0.10, 0.20, 0.30, 0.40 under high noise (ε=0.15)

*Metrics (at round 5000):*
- Conditional cooperator survival (TFT, GTFT, GRIM)
- Average wealth per survivor
- Mutual cooperation vs exploitation rates
- AllC exploitation frequency and welfare dependency (if alive)

*Expected:* β=0.05 maximizes conditional cooperator survival and mutual 
cooperation; β≥0.15 sustains AllC despite chronic exploitation (>60%), 
benefiting AllD

---

## **References**

* [https://en.wikipedia.org/wiki/Game_theory](https://en.wikipedia.org/wiki/Game_theory)
* [https://en.wikipedia.org/wiki/Prisoner%27s_dilemma](https://en.wikipedia.org/wiki/Prisoner%27s_dilemma)
* [https://blogs.cornell.edu/info2040/2012/09/21/split-or-steal-an-analysis-using-game-theory/](https://blogs.cornell.edu/info2040/2012/09/21/split-or-steal-an-analysis-using-game-theory/)
* [https://github.com/Axelrod-Python/Axelrod](https://github.com/Axelrod-Python/Axelrod)
* [https://github.com/josephius/power](https://github.com/josephius/power)
* [https://github.com/jenna-jordan/Prisoners-Dilemma](https://github.com/jenna-jordan/Prisoners-Dilemma)
* Bergstrom, T. (2003). *The Algebra of Assortative Encounters and the Evolution of Cooperation*.
  UC Santa Barbara, Department of Economics.  
  Retrieved from https://escholarship.org/uc/item/03f6s9jt
* Nowak, M. A., & Sigmund, K. (1998). *Evolution of indirect reciprocity by image scoring*. Nature, 393(6685), 573–577.  
  Retrieved from https://www.nature.com/articles/31225
* Leibo, J. Z., Zambaldi, V., Lanctot, M., Marecki, J., & Graepel, T. (2017). 
  *Multi-agent Reinforcement Learning in Sequential Social Dilemmas*. 
  arXiv preprint arXiv:1702.03037. 
  Retrieved from https://doi.org/10.48550/arXiv.1702.03037
* Hilbe, C., Schmid, L., Tkadlec, J., Chatterjee, K., & Nowak, M. A. (2018). 
  *Indirect reciprocity with private, noisy, and incomplete information*. 
  Proceedings of the National Academy of Sciences, 115(48), 12241–12246. 
  https://doi.org/10.1073/pnas.1810565115
---



