---
title: "Systems Thinking and Systems Mapping"
description: "Seeing an interconnected health problem as a web of feedback loops rather than a chain of separate causes, and drawing that web so a whole team can reason about it together."
---

# Systems Thinking and Systems Mapping

A malaria outbreak is not a line of dominoes from rainfall to cases; it is a web in which control effort feeds back on the very vectors it targets and success quietly breeds the complacency that lets the next wave build.
Systems thinking is the habit of seeing that web — the loops, delays, and boundaries — instead of a single chain of causes, and systems mapping is how a team draws it down so everyone can argue about the same picture.
It is the cross-cutting meta-competency that ties the seminar and its courses together, because the human-animal-environment problems at the heart of One Health simply do not sit inside one discipline.

![A signed causal-loop diagram linking rainfall, vector abundance, cases, control effort, and complacency, with reinforcing and balancing feedback loops.](../assets/figures/systems-thinking-and-systems-mapping.svg)

## Why interconnected problems resist reductionism

The reductionist reflex is to cut a problem into pieces, hand each piece to a specialist, and reassemble the answers.
That works when the pieces are nearly independent, and it fails exactly when they are not — when the pathogen, the host, the vector, the climate, and the policy response are all coupled and each responds to the others.
A One Health problem is the second kind: the interesting behavior lives in the interactions, so any single-discipline slice averages away the structure that actually drives the dynamics.
This is why "systems thinking" is named as a core competency domain for the field rather than an optional flourish ([Frankson et al., 2016, Frontiers in Public Health](https://consensus.app/papers/details/f73f3384df3157f19117c2872c3a3296/?utm_source=claude_desktop)), and why later revisions keep it central as the competencies are updated ([Laing et al., 2023, CABI One Health](https://consensus.app/papers/details/f8c069b3bd235270865949f75d841d98/?utm_source=claude_desktop)).

## Causal loop diagrams

A causal loop diagram (CLD) is the simplest systems map: nodes are variables and signed arrows are influences.
A `+` arrow means the two variables move together — more rainfall, more standing water — and a `-` arrow means they move oppositely — more control effort, fewer vectors.
The power of the notation is that arrows close into loops, and a loop's character is read off the signs around it, not off any single arrow.

## Stocks, flows, and feedback

Beneath the arrows sit **stocks** (accumulations like the number of infected people or the vector population) and **flows** (the rates that fill and drain them).
Stocks give a system memory and inertia: you cannot change a stock instantly, only bend the flows that feed it, which is why interventions take time to bite.
A loop is **reinforcing** when a nudge amplifies itself (an even number of negative links around the loop) and **balancing** when the loop pushes back toward a setpoint (an odd number of negative links).
Real systems mix the two, and the mix decides whether a perturbation runs away, settles, or oscillates.

## Delays make loops misbehave

Almost every link in a health system carries a **delay**: incubation before a case is counted, weeks before a control program is funded, a season before mosquito numbers respond.
Balancing loops with long delays overshoot and oscillate rather than settling smoothly, so a slow-responding control program can chase the epidemic instead of damping it.
Delays are the quiet reason that intuitively sensible interventions produce boom-and-bust cycles, and they are invisible unless the map draws them.

## Leverage points and policy resistance

Donella Meadows, in *Thinking in Systems*, ranked **leverage points** — places to intervene — from weak to strong, and her lasting warning is that the obvious levers are usually the weak ones.
Pushing harder on a parameter (spray more, fund more) is low-leverage because a balancing loop absorbs the push; changing the loop structure, the rules, or the goals is high-leverage.
**Policy resistance** is what a system does when an intervention fights a loop instead of redesigning it: the loop compensates, the problem returns, and the effort is spent holding the status quo in place.
The classic form here is complacency — control succeeds, urgency fades, effort drops, and the pathogen recovers the ground it lost.

## Unintended consequences and the boundary

Because everything is connected, an intervention that helps one stock often shifts a flow somewhere the planner was not looking — the **unintended consequence**.
Which consequences you can see depends on where you draw the **system boundary**: too tight and you externalize the very feedbacks that will defeat you, too wide and the map becomes unusable.
Boundary-drawing is therefore a design choice to make explicitly and revisit, not a fact to assume.

## Systems mapping as team science

The deepest value of a systems map is social: it externalizes each expert's private mental model onto a shared canvas where clinicians, veterinarians, ecologists, and policymakers can see where their arrows disagree.
That shared picture is what lets cross-sector teams reason about the same problem instead of talking past one another, and it maps directly onto the One Health competency domains of **teams and collaboration**, **leadership**, and **roles and responsibilities** alongside **systems thinking** ([Muehlen et al., 2025, One Health Outlook](https://consensus.app/papers/details/86fcb14b71545f3995fb5112ff87ce2a/?utm_source=claude_desktop)).
Graduate programs increasingly build this capacity deliberately, treating interdisciplinary thinking as a skill to teach rather than a trait to hope for ([Sullivan et al., 2026, One Health](https://consensus.app/papers/details/53964361b4525e25b9a30bffe5c160cd/?utm_source=claude_desktop)), and pairing it with integrative pedagogy that puts learners from different fields around one map ([Cai et al., 2024, Science in One Health](https://consensus.app/papers/details/7f8cd7bbd31d527793176d6e9219c345/?utm_source=claude_desktop)).

## A worked example

Take a five-variable CLD for a vector-borne outbreak: rainfall, vector abundance, cases, control effort, and complacency.
Rainfall raises vectors (`+`), vectors raise cases (`+`), cases both trigger official control (`+`) and, when they drag on, breed complacency (`+`); complacency erodes control (`-`), and control suppresses vectors (`-`).
Rainfall has no incoming arrow, so it is an exogenous driver and sits in no loop, leaving exactly two feedback loops in the graph.
The first, vector → cases → control → vector, carries one negative link (control suppresses vectors), so it is **balancing** — the official response damps outbreaks toward a setpoint.
The second, vector → cases → complacency → control → vector, carries two negative links, so it is **reinforcing** — a vicious cycle in which a grinding caseload breeds fatigue, fatigue erodes control, and weakened control lets vectors and cases climb again.
We classify each loop by multiplying the edge signs around it: a product of `+1` (an even count of negatives) is reinforcing, and `-1` (an odd count) is balancing.

## In code

We store the signed CLD as a directed graph, enumerate its directed cycles, and classify each by the product of edge signs around the loop.

### R

```r
library(igraph)
edges <- rbind(
  c("rainfall","vector"), c("vector","cases"), c("cases","control"),
  c("cases","complacency"), c("complacency","control"), c("control","vector"))
sign <- c(1, 1, 1, 1, -1, -1)
g <- graph_from_edgelist(edges)
# enumerate cycles, multiply signs, classify reinforcing vs balancing
```

### Python

```python
import networkx as nx
import numpy as np

# Signed causal loop diagram: +1 links move together, -1 links move oppositely.
edges = [
    ("rainfall",    "vector",      +1),  # rain fills breeding sites
    ("vector",      "cases",       +1),  # more vectors, more infections
    ("cases",       "control",     +1),  # outbreaks trigger official control
    ("cases",       "complacency", +1),  # a grinding caseload breeds fatigue
    ("complacency", "control",     -1),  # complacency erodes control
    ("control",     "vector",      -1),  # control suppresses vectors
]

G = nx.DiGraph()
for u, v, s in edges:
    G.add_edge(u, v, sign=s)

for cycle in sorted(nx.simple_cycles(G), key=len):
    ring = cycle + [cycle[0]]
    signs = [G[ring[i]][ring[i + 1]]["sign"] for i in range(len(cycle))]
    n_neg = sum(1 for s in signs if s < 0)
    kind = "reinforcing" if int(np.prod(signs)) > 0 else "balancing"
    print(f"{kind:11s} ({n_neg} neg): {' -> '.join(ring)}")
```

<!-- python-output:auto -->
```text
balancing   (1 neg): vector -> cases -> control -> vector
reinforcing (2 neg): vector -> cases -> complacency -> control -> vector
```
<!-- /python-output:auto -->

### Julia

```julia
using Graphs
# label nodes 1..5, store edge signs in a dict, enumerate simplecycles,
# then multiply the signs around each cycle to label it reinforcing/balancing.
```

## Why it matters

The two loops share every node yet pull in opposite directions, and which one dominates decides whether an outbreak is self-correcting or self-feeding — a distinction no single arrow, and no single discipline, can reveal.
Reading it off the map tells a team where to intervene: strengthening the balancing loop or, better, redesigning the reinforcing one at the complacency link is far higher-leverage than simply spraying harder against a system built to resist it.
That is the whole case for systems thinking as a threaded capability: it turns a tangle of expert opinions into a shared, testable picture of how a health problem actually behaves, which is the precondition for the cross-sector collaboration One Health demands.

## Related

- [Networks](../math/networks.md)
- [Ecological networks](../math/ecological-networks.md)
- [One Health surveillance](one-health-surveillance.md)
- [Social and structural drivers of transmission](social-drivers-of-transmission.md)
- [Epidemiology](../epidemiology.md)
