---
title: "Writing Methods"
---

# Writing Methods

The test of a good Methods section is that another lab could reproduce the work from what you wrote.
Not brevity, not elegance, reproducibility.
If a competent reader in your field cannot rebuild the study and get comparable answers, the section has failed no matter how polished the prose.

This page complements [scientific writing](../scientific-writing.md), which places Methods inside the IMRaD structure.
Here the focus is what goes in the section and how to organize it.

## Organize by what you did

Order the Methods by the work itself, in the sequence that makes the study easiest to follow.
That sequence is often chronological because studies unfold in time, but pick the order that produces the cleanest narrative, not the order you happened to run things.

Open with a short overview paragraph in plain English so a reader can picture the study before meeting the detail.
State the type of study, the setting, the duration, the population or system, and the analysis approach.
A reader who stops after this paragraph should still be able to parse your Results figures.

Then divide the rest into subsections with informative subheadings.
The usual pieces are study design, data and population, comparators, outcomes, and analysis.

## Enough detail to rebuild the study

Give the design first.
Say whether the study is experimental, observational, a model, or a mix, and describe the layout: treatments, randomization, blinding, sampling scheme, or model architecture.

Describe the data and the population next.
Where did the data come from, over what period, and who or what is in it.
State inclusion and exclusion criteria, the sample size, and how participants or units were selected.
Selection choices shape what the results can mean, so make them explicit.

Name the comparators.
An estimate or an effect only means something against a reference, so state the control group, the baseline, or the counterfactual you compare against.

Define the outcomes.
Say exactly what you measured, how you measured it, and when.
Distinguish the primary outcome from secondary outcomes so a reader knows which result carries the study.

## Name the software, versions, and seeds

Reproducibility depends on the boring specifics.
Name the software and its version, the packages and their versions, and the random seed for any stochastic step.
"Analyses were run in R" tells a reader almost nothing; "R 4.4.0 with `cmdstanr` 0.8.1 and `data.table` 1.15, seed 1834" lets them repeat the work.

Share the data and the code.
Put them in a repository with a stable identifier such as a DOI, and reference it from the Methods.
See [reproducibility](../programming/reproducibility.md) for how to package an analysis so it runs again years later.

## Match the reporting guideline

The community has agreed checklists for what a study must disclose.
Follow the one that fits your design.

- STROBE for observational epidemiology.
- CONSORT for randomized controlled trials.
- ARRIVE for animal research.
- PRISMA for systematic reviews and meta-analyses.

Most journals now ask for the completed checklist at submission.
Filling it in early also catches gaps in the Methods before a reviewer does.

## Pre-registration

Registering the hypotheses and the analysis plan before you see the outcome data separates what you predicted from what you found.
It guards against selective reporting and outcome switching, and it makes the eventual Methods section easier to write because the plan already exists.
Register confirmatory work; label anything decided after seeing the data as exploratory.

## Completeness without losing the reader

Completeness and readability pull against each other, and the answer is a two-tier section.
Keep the main text at the level a reader needs to judge the work, and move replication-grade detail to supplements.

Full protocol steps, complete parameter tables, robustness checks, derivations, and the analysis scripts belong in supplementary material.
Reference each supplement from the main text so nothing is orphaned.
The reader who wants depth follows the pointer; everyone else keeps moving.

## A worked skeleton

> **Overview.** One paragraph, plain English: type of study, setting, duration, population or system, analysis approach.
>
> **Study design.** Experimental, observational, or model; the layout, randomization, and any blinding.
>
> **Data and population.** Source, time span, inclusion and exclusion criteria, sample size, selection.
>
> **Comparators.** The control, baseline, or counterfactual.
>
> **Outcomes.** What was measured, how, and when; primary versus secondary.
>
> **Analysis.** Software and versions, models fitted, assumptions, seeds; a reproducibility statement pointing to code and data.
>
> **Supplements.** Signposts to replication-grade detail throughout.

## A worked infectious-disease example

> We estimated the serial-interval distribution of pathogen X from 214 transmission pairs reported to the regional surveillance system between March and August 2024.
> We fit a gamma distribution by maximum likelihood ([maximum likelihood estimation](../math/maximum-likelihood.md)), with a likelihood that corrected for interval censoring in the onset dates and for right truncation from the study cutoff ([fitting delay distributions](../epidemiology/delay-distributions-censoring.md)).
> We fit the model in Stan via `cmdstanr` 0.8.1 under R 4.4.0, running four chains for 2000 iterations each with seed 1834, and checked convergence with the split-Rhat statistic.
> The primary outcome was the mean serial interval with its 95 percent credible interval; the secondary outcome was the fraction of negative serial intervals.
> Data and code are archived at the accompanying DOI, and the full censoring likelihood and prior predictive checks are in the supplement.

Short as this is, another group could rebuild it: they know the data, the estimand, the likelihood, the software and seed, the outcomes, and where to find the rest.

## Related

- [Scientific Writing](../scientific-writing.md)
- [Writing Results and Discussion](writing-results-and-discussion.md)
- [Reproducibility](../programming/reproducibility.md)
- [Experimental Design](../math/experimental-design.md)
- [Scientific & Policy Writing](../writing.md)
