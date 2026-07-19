---
title: "Burst Size, Latent Period, and Mutation at the Cellular Scale"
description: "The cell-level viral life history: how burst size, latent (eclipse) period, and mutation rate set the reproduction number, the extinction probability, the optimal lysis time, and the supply of variation."
toc: true
---

# Burst Size, Latent Period, and Mutation at the Cellular Scale

The same population dynamics that govern how microbes and their hosts interact also play out one scale down, inside a single infected cell.
Zoom in from the host to that cell and a virus faces a small number of decisions, each with a mathematical consequence.
How long should it commandeer the cell before releasing progeny — its **latent period**?
How many virions should it build in that time — its **burst size**?
And how faithfully should it copy its genome — its **mutation rate**?
Perfect copying would be a trap: some level of variation is itself an advantage, the raw material that lets the virus evolve and adapt to immunity and drugs.
These three are the virus's cellular **life-history traits**, and they are coupled rather than independent: a longer latent period buys a larger burst, a larger burst is a larger draw from sequence space, and the fidelity of copying sets how much of that draw is mutant.
This page works through the math that links them, at the level of the cell, following the viral-ecology tradition that Joshua Weitz synthesized in *Quantitative Viral Ecology* and that goes back to the phage physiologists.

![Left: virions accumulate inside a cell only after an eclipse period, rising then saturating as host resources deplete. Right: the phage population growth rate is maximised at an intermediate latent period, and the optimum shifts to shorter lysis when hosts are abundant.](../assets/figures/burst-latent-optimum.svg "fig:tradeoff")

## The cellular parameters

The [within-host models](within-host-dynamics.md) track target cells, infected cells, and free virus with rate constants; here we name the *per-cell* quantities those rates encode.

| Symbol | Name | Meaning |
|--------|------|---------|
| $\tau_E$ | eclipse period | time from infection until the first progeny virion is assembled |
| $L$ | latent period | time from infection until progeny release (lysis, or onset of budding); $L \ge \tau_E$ |
| $p$ | production rate | virions assembled per unit time during the productive phase |
| $B$ | burst size | total progeny virions released by one infected cell |
| $a$ | infected-cell death rate | $1/a$ is the mean productive lifespan of a cell |
| $u$ | virion clearance rate | rate at which a free virion is lost (decay, clearance) |
| $\beta x_0$ | adsorption hazard | rate a free virion successfully attaches to a target cell |
| $\mu$ | per-site mutation rate | probability a given base is miscopied per replication |
| $U = L_g \mu$ | genomic mutation rate | expected new mutations per genome per replication ($L_g$ = genome length) |

Two things separate viruses at this scale.
**Lytic** viruses (most phages, many animal viruses) accumulate progeny internally and release them in one burst when the cell lyses, so $B$ and $L$ are tightly coupled.
**Budding** viruses (influenza, HIV, coronaviruses) release virions continuously over the cell's lifespan, so the "burst" is a lifetime yield rather than a single event — a distinction that turns out to matter for [stochastic](stochastic-epidemics.md) fate but not for mean dynamics.

## Burst size is accumulated over the latent period

Nothing is released during the eclipse; after it, progeny accumulate at rate $p$, so to a first approximation the burst grows linearly with how long the virus waits to lyse,

\[
B(L) = p\,(L - \tau_E), \qquad L \ge \tau_E. \label{eq:accumulate}
\]

In reality the curve in [@fig:tradeoff] bends over: as the cell's ribosomes, nucleotides, and membrane are exhausted, production saturates toward a ceiling $B_{\max}$, well described by $B(L) = B_{\max}\!\left(1 - e^{-(L-\tau_E)/\kappa}\right)$.
Single-cell measurements confirm both the [rising-then-saturating shape](https://doi.org/10.1128/spectrum.02663-21) and something the deterministic picture hides: burst size is wildly heterogeneous from cell to cell.
For influenza A, single infected cells span [$10^1$ to $10^4$ virions](https://doi.org/10.1371/journal.ppat.1012257), with ~10% of cells ("super-producers") making 40–60% of all progeny; HSV-1 progeny from single keratinocytes [span three orders of magnitude](https://doi.org/10.1128/jvi.01138-25) for the same reason.
The linear law [@eq:accumulate] is the mean of a very broad distribution — a cell-scale echo of the [superspreading](superspreading.md) heterogeneity seen between hosts.

## The cellular reproduction number

The burst is only worth what its virions go on to infect.
A released virion is in a race: it is cleared at hazard $u$ and adsorbs to a fresh target cell at hazard $\beta x_0$, so the probability it wins the race and starts a new infection is

\[
\rho = \frac{\beta x_0}{\beta x_0 + u}. \label{eq:rho}
\]

Multiplying the number of tickets by the chance each one wins gives the **cellular reproduction number** — how many new infected cells one infected cell produces:

\[
R_0 = B\,\rho = B\,\frac{\beta x_0}{\beta x_0 + u}. \label{eq:R0cell}
\]

This is exactly the within-host $R_0$ in disguise.
In the standard [target-cell model](within-host-dynamics.md) an infected cell produces virus at rate $k$ for a mean lifespan $1/a$, so its lifetime burst is $B = k/a$; each virion, in the small-adsorption limit $\beta x_0 \ll u$, infects with probability $\rho \approx \beta x_0/u$.
Substituting into [@eq:R0cell] recovers the familiar

\[
R_0 = \frac{k}{a}\cdot\frac{\beta x_0}{u} = \frac{\beta k x_0}{a u},
\]

which is the formula derived from the [next-generation matrix](next-generation-matrix.md) of the ODE model.
The lesson is that $R_0$ at the cellular scale is *nothing but burst size times per-virion establishment probability* — every route to it is a way of writing $B\rho$.

## Continuous versus burst production: same mean, different fate

Here is a fact that surprises people the first time.
A budding virus that trickles out virus at rate $k$ over a lifespan $1/a$, and a lytic virus that releases the whole burst $B = k/a$ at the instant of lysis, produce **identical deterministic dynamics** — the [ODEs](within-host-dynamics.md) cannot tell them apart, because only the lifetime total enters the mean-field equations.
But [Pearson and colleagues showed](https://doi.org/10.1371/journal.pcbi.1001058) that stochastically they differ, and the difference lives in the *offspring distribution* of a single infected cell.

Model each cell as producing a random number $Z$ of successful secondary infections; by [branching-process](branching-processes.md) theory the probability a lineage started by one infected cell dies out is the smallest root $q \in (0,1]$ of $q = g(q)$, where $g(s) = \mathbb{E}[s^Z]$ is the [probability generating function](moment-generating-functions.md).

**Continuous production, exponential lifespan.** A cell emits successful infections as a Poisson process (rate $\lambda = p\rho$) while it lives, and dies at rate $a$.
Racing production against death gives a *geometric* offspring count with mean $R_0 = \lambda/a$, PGF $g(s) = (1-\theta)/(1-\theta s)$ with $\theta = R_0/(1+R_0)$, and a clean closed-form extinction probability:

\[
q_{\text{cont}} = \frac{1}{R_0}. \label{eq:qcont}
\]

**Lytic burst.** A cell releases a fixed $B$ virions at once, each independently establishing with probability $\rho$, so $Z \sim \text{Binomial}(B, \rho)$, which for large $B$ and small $\rho$ is $\text{Poisson}(R_0)$ with PGF $g(s) = e^{R_0(s-1)}$ and extinction probability solving

\[
q_{\text{burst}} = e^{R_0\,(q_{\text{burst}} - 1)}. \label{eq:qburst}
\]

Both have the *same mean* $R_0$, but the geometric distribution is over-dispersed (variance $R_0 + R_0^2$) while the Poisson burst is not (variance $R_0$).
More variance means more mass on "zero offspring," so the continuous mode is always easier to extinguish: $q_{\text{cont}} > q_{\text{burst}}$ for every $R_0 > 1$, as [@fig:extinction] shows.

![Probability that a single infected cell's lineage dies out, versus the cellular reproduction number, for continuous (geometric) and lytic-burst (Poisson) production. Continuous production sits above the burst curve everywhere, so it is easier to extinguish at the same mean R0.](../assets/figures/burst-continuous-vs-burst.svg "fig:extinction")

> [!NOTE]
> Real cells sit between these extremes.
> With an [eclipse phase and a staged infectious period](https://doi.org/10.1098/rsif.2023.0400), the reproduction number of a single cell is a **negative binomial** random variable, and the probability of establishment depends on that whole distribution, not just its mean — the same reason [dispersion](superspreading.md) governs outbreak fate between hosts.

## The optimal latent period: a marginal-value problem

Waiting longer to lyse trades higher burst for slower turnover — the phage version of "a bird in the hand versus two in the bush."
The classic treatment casts it as [optimal foraging via the marginal value theorem](https://doi.org/10.1007/BF01237884): the cell is a patch, progeny are the resource, and lysis is the decision to leave.
Consider a phage growing in a well-mixed host population where a free phage takes a mean search time $T_a = 1/(k_a S)$ to find and adsorb a host (density $S$).
Each infection cycle multiplies the phage by $B(L)$ over a generation of length $T_a + L$, so the long-run population growth rate is

\[
r(L) = \frac{\ln B(L)}{T_a + L}. \label{eq:fitness}
\]

Maximising [@eq:fitness] — setting $dr/dL = 0$ — gives the optimality condition

\[
\underbrace{\frac{B'(L^\*)}{B(L^\*)}}_{\text{marginal gain rate}} = \underbrace{\frac{r(L^\*)}{1}}_{\text{average gain rate}} \;=\; \frac{\ln B(L^\*)}{T_a + L^\*}, \label{eq:mvt}
\]

the marginal value theorem in one line: **lyse at the moment the marginal rate of building new progeny falls to the average rate of return of the whole cycle.** Because $B(L)$ is concave (it saturates), [@eq:fitness] has a single interior peak — an intermediate latent period is optimal, exactly as [Wang built an isogenic λ-phage panel to confirm](https://doi.org/10.1534/genetics.105.045922) and [Kannoly verified in continuous culture](https://doi.org/10.1128/mbio.03593-21).
The comparative statics fall straight out of [@eq:mvt]: when hosts are abundant ($T_a$ small) the cost of a long wait is high, so the optimum shifts to **shorter** lysis times (right panel of [@fig:tradeoff]), the prediction [Abedon confirmed experimentally](https://doi.org/10.1128/AEM.69.12.7499-7506.2003) by enriching for short-latent-period mutants at high bacterial density.

> [!TIP]
> Notice how *flat* the fitness curve is near its peak in [@fig:tradeoff].
> A broad optimum means selection on lysis timing is weak once you are close, which is why real latent periods are variable and why [cell-to-cell noise in lysis timing](https://doi.org/10.1128/mbio.01376-24) both persists and biases the classic one-step growth-curve estimate of $L$ downward.

## Mutation: burst size is a lottery for variation

Every one of the $B$ progeny is a fresh copy of the genome, and copying is imperfect.
If a specific escape or resistance mutation arises at per-site rate $\mu$, then the number of progeny in a single burst carrying it is $\text{Binomial}(B, \mu)$, so the **expected number of mutant progeny per cell is simply the product**

\[
\mathbb{E}[\text{site mutants}] = B\mu, \qquad
P(\text{burst contains the variant}) = 1 - (1-\mu)^B \approx 1 - e^{-B\mu}. \label{eq:mutants}
\]

Burst size and mutation rate enter only through $B\mu$ — the **per-cell mutational output** — so a large burst is a large draw from sequence space even when fidelity is high ([@fig:mutation]).
Counting *any* mutation rather than one specific site, each progeny genome carries a $\text{Poisson}(U)$ number of new mutations, so the cell emits $B\,(1 - e^{-U})$ mutant progeny per burst; for an RNA virus with $U \sim 0.5$ that is a mutant in roughly two of every five virions produced.

![Left: the probability a single burst contains at least one copy of a specific escape mutation, versus burst size, for three per-site mutation rates. Right: the expected number of such mutants per cell, B times mu, crossing one mutant per cell as burst size grows.](../assets/figures/burst-mutation-supply.svg "fig:mutation")

Two consequences follow.
First, [@eq:mutants] is a *mean*; because a mutation that arises early in the intracellular replication tree is amplified into many progeny, the distribution of mutants per burst is heavy-tailed and Luria–Delbrück-like, with rare "jackpot" cells — the within-cell analogue of the [jackpot lineages](branching-processes.md) that dominate mutation-supply variance.
Second, the total supply of any variant across an infection is $(\text{infected cells}) \times B \times \mu$, so high-burst, high-mutation viruses explore genotype space fastest.
Push the genomic rate $U$ up far enough and this becomes a liability: past the [error threshold](quasispecies.md) the population can no longer maintain its master sequence, the principle behind [lethal mutagenesis](resistance-evolution.md) as an antiviral strategy.
Burst size and mutation rate are the numerator and the per-copy risk of the same lottery.

## A worked example

Take a lytic virus with eclipse $\tau_E = 15$ min, saturating yield $B_{\max} = 250$, time-scale $\kappa = 50$ min, so at a 60-minute latent period $B(60) = 250(1-e^{-0.9}) \approx 148$ virions.
Suppose a released virion adsorbs at hazard $\beta x_0 = 0.8\,\text{h}^{-1}$ and is cleared at $u = 4\,\text{h}^{-1}$, so $\rho = 0.8/4.8 \approx 0.167$ and the cellular $R_0 = 148 \times 0.167 \approx 25$ — a vigorous infection well above threshold.
Near the establishment threshold, though, the production mode matters: at $R_0 = 2$ a continuously-shedding cell's lineage dies out with probability $q_{\text{cont}} = 1/2 = 0.50$, whereas an equal-mean lytic burst dies out only with $q_{\text{burst}} \approx 0.20$ — the budding virus is more than twice as likely to fizzle from a single seeding cell.
On mutation, with per-site $\mu = 3\times10^{-5}$ the 148-virion burst throws a given point mutant with probability $1 - (1-\mu)^{148} \approx 0.0044$; a super-producer cell making $B = 5000$ raises that to $\approx 0.14$, and its expected genome-wide mutant output ($U = 0.5$) is $5000 \times 0.39 \approx 1967$ mutant progeny from that one cell.
The rare high-burst cells are doing most of the evolving.

## Eleven viruses across the cellular parameter space

The equations above are a common currency, so the most useful thing to do with them is compare real viruses that solve the cellular problem in very different ways.
Ten of the eleven below are RNA viruses; the last, variola (smallpox), is a large double-stranded DNA poxvirus — together they span the parameter space along all three axes at once, burst size, mutation rate, and the length of the production window.
Rather than give each virus its own colour, [@fig:threevirus] colours them by **life-history strategy** — how they exploit the cell — so the picture stays legible as viruses are added, with individuals read from the labels and this table.
Four strategies cover them: a **lytic burst** at cell death (poliovirus, and variola's DNA factories are freed much the same way); **acute budding**, continuous release while the cell dies (HIV, influenza, dengue); **syncytial** release, budding but fusing the cell into a dying syncytium (the paramyxo- and pneumoviruses measles, mumps, RSV, and the henipaviruses Nipah and Hendra); and **persistent**, non-cytopathic release with the window held open (hantavirus).
Those differences in how, how many, and how fast explain a great deal of their epidemiology.
(The table lists one virus per row; the same seven traits are the columns.)

| Virus | Genome | Production mode | Infected-cell fate | Eclipse $\tau_E$ | Burst size $B$ | Per-site mutation $\mu$ | Evolutionary signature |
|-------|--------|-----------------|--------------------|--------|--------|--------|------------------------|
| **HIV-1** | retrovirus, +ssRNA → DNA, ~9.7 kb | budding, continuous | dies in ~1–2 days (cytopathic + CTL) | ~18–24 h | ~$10^4$–$10^5$ total, ~1 in $10^2$–$10^3$ infectious | ~$2.4\times10^{-5}$ (RT); ~$4\times10^{-3}$ in vivo via APOBEC | quasispecies, rapid drug/immune escape |
| **Influenza A** | −ssRNA, 8 segments, ~13.5 kb | budding, ~continuous | dies in ~1 day (cytopathic) | ~6 h | ~$10^2$–$10^4$ (single-cell mean ~350–700) | ~$1.8$–$2.5\times10^{-4}$ (2–3 per genome) | antigenic drift + segment reassortment |
| **Hantavirus** | −ssRNA, 3 segments, ~12 kb | budding, continuous | **survives — non-cytopathic, persistent** | ~1–3 days | low–moderate, IFN-limited, sustained | RNA-range but constrained; low diversity | host codivergence, spillover dead-end |
| **Poliovirus** | +ssRNA, non-segmented, ~7.5 kb | **lytic burst** | lysed in ~6–8 h (rapid host shutoff) | ~2–3 h | ~$10^4$–$10^5$ per cell | ~$2\times10^{-4}$ (RdRp, no proofreading) | high diversity but 3 fixed serotypes; vaccine-derived reversion |
| **Measles** | −ssRNA, non-segmented, ~15.9 kb | budding, syncytial | fuses into dying syncytia over ~2–3 days | ~12–24 h | low–moderate (~$10^2$–$10^3$) | ~$10^{-4}$ (RNA-range) | **monotypic** — one serotype, antigenically stable |
| **Mumps** | −ssRNA, non-segmented, ~15.4 kb | budding, syncytial | fuses into dying syncytia (~2–3 days) | ~12–24 h | low–moderate (~$10^2$–$10^3$) | ~$1$–$2\times10^{-4}$ (RNA-range) | **12 genotypes**; vaccine-era outbreaks (waning + escape) |
| **RSV** | −ssRNA, non-segmented, ~15.2 kb | budding, syncytial | fuses into dying syncytia (~2–3 days) | ~10–12 h | low; high particle-to-PFU ratio | ~$10^{-4}$ (RNA-range) | A/B subgroups; variable G, conserved F |
| **Nipah** | −ssRNA, non-segmented, ~18.2 kb | budding, syncytial | fuses into dying syncytia (~2–3 days) | ~12–24 h | moderate (~$10^3$–$10^4$) | ~$10^{-4}$ (RNA-range, conserved) | bat reservoir; **BSL-4** spillover, high CFR |
| **Hendra** | −ssRNA, non-segmented, ~18.2 kb | budding, syncytial | fuses into dying syncytia (~2–3 days) | ~12–24 h | moderate (~$10^3$–$10^4$) | ~$10^{-4}$ (RNA-range, conserved) | flying-fox reservoir; horse-mediated spillover |
| **Dengue** | +ssRNA, non-segmented, ~10.7 kb | budding (secretory) | dies by apoptosis (~2–3 days) | ~12–24 h | ~$10^3$–$10^4$ | ~$1$–$2\times10^{-4}$ (RdRp) | 4 serotypes; cross-serotype ADE |
| **Variola** | **dsDNA**, ~186 kb | released mainly on lysis | dies (cytopathic, ~1–2 days) | ~6–12 h | ~$10^3$–$10^4$ | ~$10^{-6}$ (**proofreading** DNA pol) | genetically stable; **eradicated** by one vaccine |

![Colour marks the life-history strategy, not the individual virus: lytic burst (orange), acute budding (blue), syncytial fuse-and-die (purple), and persistent (green). Left: cumulative virions produced by one cell over time — poliovirus bursts fastest, the acute budders climb to their yields before the cell dies, the syncytial paramyxo- and pneumoviruses (measles, mumps, RSV, Nipah, Hendra) plateau together, variola builds in cytoplasmic factories then is freed on lysis, and hantavirus alone never lyses, so its window stays open. Right: all eleven viruses on the burst-size / mutation-rate plane, individually labelled, with variola sitting far below the RNA viruses in mutation rate, against diagonals of constant per-cell mutational output B times mu.](../assets/figures/burst-three-viruses.svg "fig:threevirus")

**The production window, not the burst rate, is what hantavirus changes.** Recall that lifetime burst is production rate times production window, and for a lytic or cytopathic virus the window is the cell's lifespan $1/a$.
Influenza and HIV both kill the cell — influenza fast, HIV a little slower — so their yield is capped by how long the cell survives (left panel of [@fig:threevirus]); HIV's in-vivo per-cell yield is [~$4$–$5\times10^4$ virions](https://doi.org/10.1073/pnas.0707449104) but only [about one in a few hundred is infectious](https://doi.org/10.1186/1742-4690-9-18), so the *effective* burst that enters $R_0 = B\rho$ is far smaller than the RNA count.
Poliovirus is the same accounting compressed into hours: it packages $10^4$–$10^5$ virions and lyses the cell within about 6–8 h — a very high production rate over a very short window, the steep early climb in the left panel.
Measles, RSV, and dengue sit in between: all three bud yet still kill the cell — measles and RSV by fusing it into dying syncytia, dengue by driving it to apoptosis — so their windows are bounded like influenza's while their production rates stay modest, which is why their curves in the left panel plateau at intermediate yields.
Hantaviruses are the striking case: they replicate in vascular [endothelial cells with no cytopathic effect](https://doi.org/10.3389/fmicb.2014.00727) and establish [persistent infection](https://doi.org/10.1016/s0966-842x(99)01658-3), so $a \to 0$ and the window is set not by lysis but by interferon.
In human cells IFN-β switches on after a few days and [production falls off](https://doi.org/10.1128/JVI.66.10.5929-5936.1992); in the natural rodent reservoir the antiviral response is [never triggered](https://doi.org/10.1371/journal.ppat.1012728), the window stays open indefinitely, and the animal remains a lifelong low-level shedder.
The same $B = \text{rate}\times\text{window}$ accounting, with the death term turned off, is the whole difference between an acute and a persistent infection.

**Production mode sorts their stochastic fate.** The nine budding viruses release virus continuously rather than in a synchronized burst, so the offspring distribution of a single infected cell is closer to the over-dispersed geometric of [@eq:qcont] than to the Poisson of [@eq:qburst], with extinction probability near $1/R_0$.
This is why single-cell seeding is fragile even for a fit virus, and it is consistent with the very narrow transmission bottleneck of HIV, where a productive infection is usually founded by a **single** transmitted variant despite the donor carrying a diverse swarm.
Poliovirus makes the mechanism visible: because it releases its whole burst at lysis, a single cell's successful-offspring count is Poisson [@eq:qburst] rather than geometric, so at the *same* mean $R_0$ a lone poliovirus-infected cell is meaningfully **harder** to extinguish than any of the budding nine — the burst-versus-continuous gap of [@fig:extinction], now a difference between real viruses.
Variola sits on the same side of that gap: its progeny are freed mostly when the cell lyses rather than trickled out over a lifetime, so its single-cell offspring count is burst-like too, another Poisson case set against the geometric budders.

**Mutational output separates the fast evolvers from the stable ones.** The per-cell mutational output is $B\mu$, and the right panel of [@fig:threevirus] places all eleven viruses on the $B$–$\mu$ plane against diagonals of constant $B\mu$.
Influenza sits high on $\mu$ — [~$2\times10^{-4}$ per site, 2–3 mutations per genome copied](https://doi.org/10.7554/eLife.26437) — which, multiplied over large bursts, is the raw material of antigenic drift, compounded by reassortment of its eight segments.
HIV's reverse transcriptase runs at the [canonical RNA-virus rate ~$2\times10^{-5}$](https://doi.org/10.1128/JVI.00694-10), but its enormous within-host replication and [APOBEC-driven hypermutation push the in-vivo rate to ~$4\times10^{-3}$](https://doi.org/10.1371/journal.pbio.1002251) — the highest measured for any biological entity — which is why drug resistance is essentially pre-existing in every patient.
Hantaviruses sit in the low corner: their persistent, low-turnover replication accumulates change slowly, and their tight [codivergence with rodent hosts](https://doi.org/10.1016/s0966-842x(99)01658-3) leaves them genetically stable and host-restricted — part of why human infections are typically epidemiological dead ends rather than the start of sustained human-to-human chains.
Poliovirus and measles are the cautionary corner: poliovirus has the *highest* per-cell mutational output of the eleven ($B\mu \approx 6$, a large burst copied at RdRp fidelity) and measles carries an ordinary RNA-range $\mu$, yet both are antigenically almost frozen — poliovirus in three fixed serotypes, measles as a single serotype the 1960s vaccine still matches — because their capsid and glycoprotein structures are functionally constrained, so most of that variation is either lethal or invisible to immunity.
The syncytial paramyxoviruses fan out around measles precisely because that constraint is not absolute: mumps, its close relative, carries near-identical $B$ and $\mu$ yet its surface proteins are *not* as locked down, so the same mutational supply has produced twelve genotypes and repeated vaccine-era outbreaks in highly immunised populations; the henipaviruses Nipah and Hendra sit the other way, held genetically stable by strong purifying selection and codivergence with their fruit-bat reservoirs, so their menace is spillover and a high case-fatality rate, not antigenic escape — a reminder that whether variation becomes useful is a property of the protein and its selective regime, not of $B\mu$.
RSV and dengue occupy the same middle ground, carrying just enough usable antigenic variation to matter epidemiologically: RSV splits into A and B subgroups on its variable G protein while its fusion protein stays conserved, and dengue's four serotypes are the substrate for [antibody-dependent enhancement](https://doi.org/10.1126/science.aan6836), where prior immunity to one serotype worsens infection by another.
Variola is the opposite extreme in *fidelity*, and the one point that leaves the RNA cloud entirely: its proofreading DNA polymerase holds the per-site rate near $10^{-6}$, an order of magnitude below any RNA virus here, so despite a burst of $\sim\!10^4$ its per-cell mutational output stays low ($B\mu \approx 0.015$, down in the corner with hantavirus) — the molecular reason smallpox stayed a single, antigenically fixed target for centuries and could be driven to global eradication with one vaccine.
They are the standing reminder that $B\mu$ sets the *supply* of variants, not whether any of them can become useful: read through that product, the same quantity that sets a phage's supply of escape mutants explains why influenza and HIV are moving targets, why hantavirus (little variation) and poliovirus, measles, and the henipaviruses (plenty of variation, nowhere to go) are not, why mumps, RSV, and dengue land in between, and why variola — its output low *and* its structure constrained — was the one virus a vaccine could corner into extinction.

## In code

We reproduce all four scenarios: the cellular $R_0$ from a burst, the continuous-versus-burst extinction gap, the optimal latent period, and the mutational output per burst.

### R

```r
eclipse <- 15; Bmax <- 250; kappa <- 50
burst <- function(L) ifelse(L > eclipse, Bmax * (1 - exp(-(L - eclipse) / kappa)), 0)

# cellular R0 = B * rho
beta_x0 <- 0.8; u <- 4
rho <- beta_x0 / (beta_x0 + u)
R0  <- burst(60) * rho
cat(sprintf("B(60) = %.0f, rho = %.3f, cellular R0 = %.1f\n", burst(60), rho, R0))

# continuous (geometric) vs burst (Poisson) extinction at a shared mean R0
q_burst <- function(R) uniroot(function(q) exp(R * (q - 1)) - q, c(1e-9, 1 - 1e-9))$root
for (R in c(1.5, 2, 3))
  cat(sprintf("R0=%.1f: extinction continuous %.3f vs burst %.3f\n", R, 1 / R, q_burst(R)))

# optimal latent period maximising r(L) = ln B(L) / (Ta + L)
grid <- seq(eclipse + 0.5, 160, length.out = 4000)
for (Ta in c(3, 60)) {
  Lstar <- grid[which.max(log(burst(grid)) / (Ta + grid))]
  cat(sprintf("Ta=%2.0f: optimal L = %.1f min, burst = %.0f\n", Ta, Lstar, burst(Lstar)))
}

# mutation: expected mutants and escape probability per burst
mu <- 3e-5; U <- 0.5                            # per-site rate; per-genome rate
for (B in c(30, 148, 5000))
  cat(sprintf("B=%5d: E[site mutants]=%.3f, P(escape)=%.3f, E[mutant progeny]=%.0f\n",
              B, B * mu, 1 - (1 - mu)^B, B * (1 - exp(-U))))
```

### Python

```python
import numpy as np
from scipy.optimize import brentq

# 1. Intracellular accumulation and the cellular reproduction number R0 = B * rho
eclipse, Bmax, kappa = 15.0, 250.0, 50.0
burst = lambda L: np.where(L > eclipse, Bmax * (1 - np.exp(-(L - eclipse) / kappa)), 0.0)
beta_x0, u = 0.8, 4.0                      # per-virion adsorption vs clearance hazards
rho = beta_x0 / (beta_x0 + u)              # prob a released virion infects a new cell
B60 = float(burst(60.0))
print(f"B(60 min) = {B60:.0f} virions, rho = {rho:.3f}, cellular R0 = {B60 * rho:.1f}")

# 2. Same mean R0, two production modes -> different extinction (near threshold)
for R in (1.5, 2.0, 3.0):
    q_burst = brentq(lambda q: np.exp(R * (q - 1)) - q, 1e-9, 1 - 1e-9)
    print(f"R0={R}: extinction  continuous {1/R:.3f}  vs  burst {q_burst:.3f}")

# 3. Optimal latent period maximises r(L) = ln B(L) / (T_a + L)
grid = np.linspace(eclipse + 0.5, 160, 4000)
for Ta in (3.0, 60.0):
    Lstar = grid[np.argmax(np.log(burst(grid)) / (Ta + grid))]
    print(f"T_a={Ta:4.0f}: optimal L = {Lstar:.1f} min, burst = {burst(Lstar):.0f}")

# 4. Mutation: expected mutants and escape probability per burst
mu, U = 3e-5, 0.5                          # per-site rate; per-genome rate (RNA scale)
for B in (30, 148, 5000):
    print(f"B={B:5d}: E[site mutants]={B*mu:.3f}, "
          f"P(escape)={1-(1-mu)**B:.3f}, E[mutant progeny]={B*(1-np.exp(-U)):.0f}")
```

<!-- python-output:auto -->
```text
B(60 min) = 148 virions, rho = 0.167, cellular R0 = 24.7
R0=1.5: extinction  continuous 0.667  vs  burst 0.417
R0=2.0: extinction  continuous 0.500  vs  burst 0.203
R0=3.0: extinction  continuous 0.333  vs  burst 0.060
T_a=   3: optimal L = 21.7 min, burst = 31
T_a=  60: optimal L = 32.9 min, burst = 75
B=   30: E[site mutants]=0.001, P(escape)=0.001, E[mutant progeny]=12
B=  148: E[site mutants]=0.004, P(escape)=0.004, E[mutant progeny]=58
B= 5000: E[site mutants]=0.150, P(escape)=0.139, E[mutant progeny]=1967
```
<!-- /python-output:auto -->

### Julia

```julia
using Roots

eclipse, Bmax, kappa = 15.0, 250.0, 50.0
burst(L) = L > eclipse ? Bmax * (1 - exp(-(L - eclipse) / kappa)) : 0.0

beta_x0, u = 0.8, 4.0
rho = beta_x0 / (beta_x0 + u)
println("B(60) = $(round(burst(60); digits=0)), cellular R0 = $(round(burst(60)*rho; digits=1))")

# continuous (geometric) vs lytic-burst (Poisson) extinction
for R in (1.5, 2.0, 3.0)
    qb = find_zero(q -> exp(R * (q - 1)) - q, (1e-9, 1 - 1e-9))
    println("R0=$R: extinction continuous $(round(1/R; digits=3)) vs burst $(round(qb; digits=3))")
end

# optimal latent period
grid = range(eclipse + 0.5, 160; length = 4000)
for Ta in (3.0, 60.0)
    Lstar = grid[argmax(log.(burst.(grid)) ./ (Ta .+ grid))]
    println("Ta=$Ta: optimal L = $(round(Lstar; digits=1)) min, burst = $(round(burst(Lstar); digits=0))")
end

# mutation: expected mutants and escape probability per burst
mu, U = 3e-5, 0.5                            # per-site rate; per-genome rate
for B in (30, 148, 5000)
    println("B=$B: E[site mutants]=$(round(B*mu; digits=3)), " *
            "P(escape)=$(round(1 - (1 - mu)^B; digits=3)), " *
            "E[mutant progeny]=$(round(B * (1 - exp(-U)); digits=0))")
end
```

## Why it matters

The three cellular traits on this page are the microscopic origins of the macroscopic quantities the rest of infectious-disease modelling takes as given.
Burst size and per-virion establishment set the within-host $R_0$ that decides whether an infection takes hold; the production mode and the eclipse phase set the [stochastic](stochastic-epidemics.md) extinction probability that decides whether a single exposed cell — or a single spilled-over host — starts anything at all.
The latent-period optimum is a life-history [trade-off](evolution-of-virulence.md) that natural selection actually solves, and the same $B(L)$ curve that governs a phage's optimal lysis time governs how a within-host virus tunes its replication against immune clearance.
And the product $B\mu$ is the engine of viral evolution: it is the per-cell supply of the variation that becomes drug resistance, immune escape, and — pushed too far by design — the [error catastrophe](quasispecies.md) that antiviral mutagens exploit.
Reading a virus at the scale of the cell turns "how fast, how many, how sloppy" into equations that connect all the way up to the epidemic.

## Related

- [Within-Host Dynamics and the Immune Response](within-host-dynamics.md) — the target-cell ODEs whose rate constants these per-cell traits encode
- [Branching Processes](branching-processes.md) — the extinction-probability machinery used here
- [Superspreading and Transmission Heterogeneity](superspreading.md) — the between-host analogue of cell-to-cell burst heterogeneity
- [Quasispecies and the Error Threshold](quasispecies.md) — where the mutational-output story leads
- [Resistance Evolution and Lethal Mutagenesis](resistance-evolution.md) — pushing $B\mu$ past the edge of viability
- [The Evolution of Virulence](evolution-of-virulence.md) — life-history trade-offs one scale up
- [Stochastic Epidemics and the Gillespie Algorithm](stochastic-epidemics.md) — simulating the noisy early dynamics
- [The Euler–Lotka Equation](../epidemiology/euler-lotka.md) — the renewal-equation view of the growth rate $r$
- [Quantitative Methods](../math.md)
