---
title: "The Evolution of Cooperation"
---

# The Evolution of Cooperation

Cooperation is a puzzle for Darwinism: if defectors always out-earn cooperators in a direct encounter, why is the living world full of altruism, from cells to societies?
The answer is that some structure — relatedness, repetition, reputation, or a network of neighbours — can tip the balance so that helping pays.

## The Prisoner's Dilemma

The tension is captured by the **Prisoner's Dilemma**.
Two players each choose to cooperate (C) or defect (D).
Mutual cooperation pays the reward $R$, mutual defection the punishment $P$; a defector meeting a cooperator earns the temptation $T$ while the cooperator gets the sucker's payoff $S$, with

\[
T > R > P > S.
\]

\[
\begin{array}{c|cc}
 & C & D \\ \hline
C & R & S \\
D & T & P
\end{array}
\]

In a single round defection **dominates**: whatever the opponent does, $T > R$ and $P > S$ mean you earn more by defecting.
Yet two defectors land at $P$, worse for both than the $R$ they could have shared, so rational individual choices produce a collectively poor outcome.
This is a frequency-dependent game, and it sits squarely inside [evolutionary game theory](evolutionary-game-theory.md).

## Repetition and reciprocal strategies

Everything changes when the same players meet again.
In the **iterated Prisoner's Dilemma**, a strategy is a rule for choosing C or D based on past play, and cooperation can be protected by the threat of future retaliation.

Two robust reciprocal strategies stand out.
**Tit-for-tat** cooperates on the first move and then copies the opponent's previous move: nice, retaliatory, and forgiving.
**Win-stay-lose-shift** (Pavlov) repeats its last move after a good outcome ($R$ or $T$) and switches after a bad one ($P$ or $S$), which lets it exploit unconditional cooperators and recover from errors.

## Nowak's five rules

Martin Nowak organised the mechanisms that let cooperation evolve into five rules, each a threshold comparing the benefit $b$ a cooperator confers to the cost $c$ it pays.

**1.
Kin selection.** Helping relatives spreads copies of the cooperator's genes.
Hamilton's rule says altruism is favoured when

\[
r\,b > c,
\]

where $r$ is the coefficient of relatedness between actor and recipient.

**2.
Direct reciprocity.** If the same two individuals interact repeatedly, cooperation pays when

\[
w > \frac{c}{b},
\]

where $w$ is the probability of another round.
A high enough chance of meeting again makes retaliatory strategies like tit-for-tat stable.

**3.
Indirect reciprocity.** Reputation lets helpers be repaid by third parties who observed them.
Cooperation is favoured when

\[
q > \frac{c}{b},
\]

where $q$ is the probability of knowing another individual's reputation.

**4.
Network (spatial) reciprocity.** When individuals interact only with neighbours on a graph rather than in a well-mixed population, cooperators can form clusters that support one another.
For a graph with mean degree $\langle k\rangle$, cooperation is favoured roughly when

\[
\frac{b}{c} > \langle k\rangle .
\]

Sparse, tightly clustered contact structures — few neighbours per node — are the most hospitable to cooperation.
This ties the fate of cooperation directly to the structure of [networks](networks.md): the same graph properties studied through [centrality](centrality.md) and in [ecological networks](ecological-networks.md) determine whether helpers can cluster and persist rather than being picked off by defectors.

**5.
Group selection.** When populations are divided into groups and groups with more cooperators grow or survive faster, selection between groups can favour cooperation.
For groups of size $n$ competing among $m$ groups, the threshold is $b/c > 1 + n/m$.

Rules 2 through 5 all reduce to a benefit-to-cost condition: cooperation needs $b/c$ to exceed a critical value set by the mechanism.

## Worked example: crossing the threshold

Suppose helping costs a cooperator $c = 1$ offspring-equivalent and delivers a benefit $b = 3$ to the recipient.

*Kin selection.* Directed at a full sibling, $r = 1/2$, Hamilton's rule gives $r b = 0.5 \times 3 = 1.5 > 1 = c$, so the altruism is favoured.
Directed at a cousin, $r = 1/8$, we get $r b = 0.375 < 1$, and it is not.

*Network reciprocity.* Here $b/c = 3$.
On a sparse graph with mean degree $\langle k\rangle = 2$ we have $b/c = 3 > 2$, so cooperator clusters spread.
On a denser graph with $\langle k\rangle = 4$, the condition $3 > 4$ fails, and defection takes over — more neighbours dilute the local advantage of clustered cooperators.
The same benefit and cost thus lead to opposite outcomes depending purely on how interactions are wired.

## Simulation: an iterated Prisoner's Dilemma tournament

We run a round-robin among tit-for-tat, always-cooperate, and always-defect over 200-round games and total each strategy's score.

### R

```r
R <- 3; S <- 0; T <- 5; P <- 1

move <- function(strat, opp_hist) {
  if (strat == "ALLC") return("C")
  if (strat == "ALLD") return("D")
  if (length(opp_hist) == 0) "C" else tail(opp_hist, 1)  # TFT
}

play <- function(a, b, rounds = 200) {
  ha <- hb <- character(0); sa <- sb <- 0
  for (i in seq_len(rounds)) {
    ma <- move(a, hb); mb <- move(b, ha)
    pay <- if (ma == "C" && mb == "C") c(R, R)
           else if (ma == "C") c(S, T)
           else if (mb == "C") c(T, S) else c(P, P)
    sa <- sa + pay[1]; sb <- sb + pay[2]
    ha <- c(ha, ma); hb <- c(hb, mb)
  }
  c(sa, sb)
}

strats <- c("TFT", "ALLC", "ALLD"); tot <- setNames(numeric(3), strats)
for (i in seq_along(strats)) for (j in i:length(strats)) {
  s <- play(strats[i], strats[j])
  if (i == j) tot[i] <- tot[i] + s[1]
  else { tot[i] <- tot[i] + s[1]; tot[j] <- tot[j] + s[2] }
}
tot            # TFT 1399, ALLC 1200, ALLD 1404
```

### Python

```python
from itertools import combinations_with_replacement
R, S, T, P = 3, 0, 5, 1

def move(strat, opp_hist):
    if strat == "ALLC": return "C"
    if strat == "ALLD": return "D"
    return "C" if not opp_hist else opp_hist[-1]      # TFT

def play(a, b, rounds=200):
    ha, hb, sa, sb = [], [], 0, 0
    for _ in range(rounds):
        ma, mb = move(a, hb), move(b, ha)
        if   ma == "C" and mb == "C": pa, pb = R, R
        elif ma == "C":               pa, pb = S, T
        elif mb == "C":               pa, pb = T, S
        else:                         pa, pb = P, P
        sa += pa; sb += pb; ha.append(ma); hb.append(mb)
    return sa, sb

strats = ["TFT", "ALLC", "ALLD"]
tot = {s: 0 for s in strats}
for a, b in combinations_with_replacement(strats, 2):
    sa, sb = play(a, b)
    if a == b: tot[a] += sa
    else:      tot[a] += sa; tot[b] += sb
print(tot)     # {'TFT': 1399, 'ALLC': 1200, 'ALLD': 1404}
```

<!-- python-output:auto -->
```text
{'TFT': 1399, 'ALLC': 1200, 'ALLD': 1404}
```
<!-- /python-output:auto -->

### Julia

```julia
R, S, T, P = 3, 0, 5, 1

move(strat, opp) = strat == "ALLC" ? "C" :
                   strat == "ALLD" ? "D" :
                   isempty(opp)    ? "C" : opp[end]      # TFT

function play(a, b; rounds = 200)
    ha = String[]; hb = String[]; sa = sb = 0
    for _ in 1:rounds
        ma, mb = move(a, hb), move(b, ha)
        pa, pb = ma == "C" && mb == "C" ? (R, R) :
                 ma == "C"              ? (S, T) :
                 mb == "C"              ? (T, S) : (P, P)
        sa += pa; sb += pb; push!(ha, ma); push!(hb, mb)
    end
    sa, sb
end

strats = ["TFT", "ALLC", "ALLD"]; tot = Dict(s => 0 for s in strats)
for i in eachindex(strats), j in i:length(strats)
    sa, sb = play(strats[i], strats[j])
    i == j ? (tot[strats[i]] += sa) :
             (tot[strats[i]] += sa; tot[strats[j]] += sb)
end
println(tot)   # TFT 1399, ALLC 1200, ALLD 1404
```

Tit-for-tat never loses badly and matches other cooperators, but always-defect edges ahead here because the naive always-cooperate strategy hands it a steady stream of temptation payoffs.
Remove the unconditional cooperators, or let the population evolve by imitation, and the direct-reciprocity threshold $w > c/b$ makes a population of tit-for-tat players uninvadable — a bistability the tournament totals only hint at, and which is amplified once interactions are structured on a network rather than well-mixed.

## Why it matters

The evolution of cooperation explains how natural selection built the major transitions of life — genes into chromosomes, cells into organisms, individuals into societies — despite the short-term advantage of cheating.
The same five thresholds guide practical problems from managing microbial public goods and cancer (a breakdown of cellular cooperation) to designing incentives, and they show why population structure, drift, and who-interacts-with-whom matter as much as raw payoffs; in small or structured populations, [genetic drift](genetic-drift.md) can carry rare cooperators across a threshold that deterministic selection alone would block.

## Related

- [Evolutionary Game Theory](evolutionary-game-theory.md)
- [Networks](networks.md)
- [Ecological Networks](ecological-networks.md)
- [Centrality](centrality.md)
- [Genetic Drift](genetic-drift.md)
- [Kin Selection and Inclusive Fitness](kin-selection.md) — Hamilton's rule and relatedness developed in full as the first of Nowak's mechanisms
- [Quantitative Methods](../math.md)
