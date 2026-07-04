---
title: "Scientific Writing"
description: "The craft of scientific communication: generating a testable hypothesis, framing Specific Aims, and structuring a manuscript reviewers can follow."
---

# Scientific Writing

Science is not finished until it is communicated.
A result that cannot be explained, a hypothesis that cannot be stated sharply, or an aim that a reviewer cannot follow will not advance — no matter how good the underlying work.
This page covers the craft from the first spark of a question through the structure of a paper: how to **generate a testable hypothesis**, how to frame **Specific Aims**, and how to organize a manuscript so a reader grasps it.
It is a companion to [scientific pathways](scientific-pathways.md), where these skills meet the funding system.

## Generating a hypothesis

Good research questions are made, not found, and there is a recognizable path from a vague interest to a testable claim.

1. **Observation** — something in the data or the field that is surprising or unexplained.
2. **Question** — a specific, answerable version of the puzzle.
3. **Hypothesis** — a proposed explanation stated so that it makes **predictions** that could turn out false.
4. **Prediction** — the concrete, measurable consequence you will look for.

A hypothesis earns its keep by being **falsifiable** (Popper): it must forbid some outcomes, or it explains nothing.
"The pathogen spreads through the population" is not a hypothesis; "pre-symptomatic transmission accounts for more than half of secondary infections, so isolating only symptomatic cases will not stop spread" is — it predicts specific, measurable failures of a specific intervention.

**Strong inference** (Platt) sharpens this further: design studies around **competing hypotheses** and experiments whose outcomes will *distinguish* between them, rather than accumulating evidence consistent with a single favored idea.
Framing a question as "which of these mechanisms is responsible?" rather than "is my mechanism plausible?" is one of the most reliable routes to work that matters.
Distinguishing genuine mechanism from confounding is the domain of [causal inference](math/causal-inference.md), and testing a hypothesis against data is the domain of [hypothesis testing](math/hypothesis-testing.md).

## The Specific Aims page

For an NIH proposal, the one-page **Specific Aims** is the single most-read, most-important thing you write — many reviewers form their opinion here.
It follows a reliable, almost hourglass, structure: broad importance, narrowing to your specific gap and hypothesis, then broadening again to impact.

- **The hook** — one paragraph establishing the problem and why it matters.
- **The gap** — what is unknown or unresolved, and why it blocks progress.
- **The central hypothesis and objective** — your proposed explanation and what this project will do about it, stated in one or two crisp sentences.
- **The aims** — typically two or three, each a self-contained, testable objective; aims should be **related but not dependent**, so that if one fails the others still stand.
- **The payoff** — the expected outcomes and the impact on the field if you succeed.

### Example aims for an infectious-disease study

To make the structure concrete, here is a worked set of aims built around the pre-symptomatic-transmission hypothesis above.

> **Central hypothesis.** Pre-symptomatic transmission is a major driver of spread for pathogen X, and its contribution can be estimated from the timing of infections and quantified well enough to predict when symptom-based isolation will fail.
>
> **Aim 1. Estimate the generation- and serial-interval distributions of pathogen X, correcting for censoring and right truncation.** Using contact-tracing pairs, fit delay distributions with a censoring- and truncation-aware likelihood ([delay distributions](epidemiology/delay-distributions-censoring.md)). *Outcome:* unbiased interval estimates, including the fraction of negative serial intervals.
>
> **Aim 2. Quantify the pre-symptomatic fraction of transmission.** Combine the estimated intervals with the incubation-period distribution to infer the share of transmission occurring before symptom onset. *Outcome:* an estimate, with uncertainty, of the pre-symptomatic transmission fraction.
>
> **Aim 3. Predict the impact of symptom-based versus test-based isolation.** Embed the estimates in a transmission model ([the reproduction number](math/reproduction-number-rt.md)) to compare control strategies. *Outcome:* quantitative guidance on which strategy can drive $R_t$ below 1.

Note how each aim has a **method** and an **outcome**, the aims build a single argument, and no aim's success requires another's — the design a study section rewards.

## Structuring the paper: IMRaD

Most scientific papers follow **IMRaD** — Introduction, Methods, Results, and Discussion — a structure that itself mirrors an hourglass.

- **Introduction** (broad → narrow) — the field, the gap, and your specific question or hypothesis.
- **Methods** — enough detail for another lab to **reproduce** the work; the test of a good Methods section is reproducibility, not brevity.
- **Results** — what you found, led by the figures, reported without interpretation.
- **Discussion** (narrow → broad) — what the results mean, their limitations, and their implications for the field.

Two elements carry disproportionate weight.
The **abstract** is what almost everyone reads and often all they read — it should state the question, approach, key result (with numbers), and conclusion.
The **figures** are the backbone of the Results: a reader should be able to follow the paper's argument from the figures and captions alone, which is why designing figures is a first-class scientific skill, not decoration (see [graphing data](math/graphing-data.md)).

## Rigor, reproducibility, and reporting guidelines

Credible writing is transparent about how the work was done, and the community has codified this into **reporting guidelines** — checklists that specify what a paper must disclose.

- **STROBE** — observational epidemiological studies.
- **CONSORT** — randomized controlled trials.
- **ARRIVE** — animal research.
- **PRISMA** — systematic reviews and meta-analyses.

Following the relevant guideline is increasingly required by journals and makes a study easier to evaluate, reproduce, and synthesize.
Pre-registering hypotheses and analysis plans, and sharing data and code, extend the same principle of transparency (see [reproducibility](programming/reproducibility.md) and [experimental design](math/experimental-design.md)).

## Peer review, revision, and preprints

Publication is a **conversation**.
A manuscript is reviewed by peers, and the response is almost always "revise" — the productive move is a **point-by-point response** that addresses every comment directly, whether by making the change or by explaining, courteously and with evidence, why not.
**Preprints** (bioRxiv, medRxiv) let you share findings before formal review, which speeds dissemination — vital during outbreaks — and invites feedback, while the peer-reviewed version remains the version of record.
Learning to receive criticism as data, rather than as verdict, is one of the quieter but more important skills of a scientific career.

## Why it matters

Writing is thinking made visible.
The discipline of stating a falsifiable hypothesis, structuring aims that a stranger can evaluate, and reporting methods that another lab can reproduce is not separate from doing good science — it *is* doing good science, and it is what turns individual results into shared, cumulative knowledge.

## Related

- [Scientific Pathways](scientific-pathways.md) — fellowships and grant writing
- [Hypothesis Testing](math/hypothesis-testing.md)
- [Experimental Design](math/experimental-design.md)
- [Causal Inference](math/causal-inference.md)
- [Graphing Data](math/graphing-data.md)
- [Fitting Delay Distributions](epidemiology/delay-distributions-censoring.md)
