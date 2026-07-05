---
title: "Research and Data Ethics, Governance, and Responsible Sharing"
description: "The values-and-ethics layer of infectious-disease research — human-subjects review, FAIR data, re-identification risk, and equitable pathogen-data sharing."
---

# Research and Data Ethics, Governance, and Responsible Sharing

Quantitative training teaches you to make an estimate defensible, but rarely to ask whether the data behind it was collected, stored, and shared responsibly.
That second question is not a footnote to the science; in outbreak work it is often the science, because the people in your rows are patients, communities, and the source countries of the pathogens you sequence.
This page treats ethics and governance as a cross-cutting thread woven through every course in the concentration, not a one-time compliance form.

## Human subjects, review, and consent

Any work that collects data about identifiable living people, or uses their existing data, is human-subjects research and needs review before it starts, not after.
An Institutional Review Board (IRB) or ethics committee weighs the risks to participants against the value of the knowledge and checks that consent is genuinely informed.
Informed consent means a person understands what is collected, why, who will see it, and that they may decline without penalty — a signature on a form no one explained is not consent.
Secondary use of data collected for another purpose, such as clinical records repurposed for surveillance, still needs a governance basis even when re-consent is impractical.

## Ethics of collection in outbreaks and emergencies

Emergencies do not suspend ethics; they raise the stakes, because power is unequal and the pressure to act fast is enormous.
Data gathered under duress — from displaced people, during a lockdown, or from patients desperate for care — carries a heightened risk of coercion and of harms that outlast the outbreak.
Bardosh and colleagues argue that outbreak response needs formal codes of conduct and real integration of social science, so that communities are partners rather than subjects (Bardosh et al., 2020, *Globalization and Health*: [link](https://consensus.app/papers/details/96b9bf44b3d75d9cb8dca9e7a541c43b/?utm_source=claude_desktop)).
The practical test is simple: collect the minimum you need, be honest about what you will do with it, and plan for the data's whole life before you gather the first record.

## Data governance, stewardship, and FAIR

Governance is the set of agreements that answer who may do what with a dataset, under which conditions, and who is accountable when something goes wrong.
A data steward is the named person responsible for a dataset's quality, access rules, and lifecycle — a role, not a job title, that should exist for every project.
The FAIR principles (Wilkinson et al., 2016) give stewardship a concrete target: data should be **F**indable, **A**ccessible, **I**nteroperable, and **R**eusable.
FAIR is about machines and metadata, not open-to-everyone: a dataset can be findable through a documented catalog and richly described while access remains controlled for genuinely sensitive fields.

## Privacy and re-identification risk

Removing names does not make data anonymous, because combinations of ordinary attributes — age, sex, a coarse location, a date — can single a person out.
These attributes are **quasi-identifiers**, and their re-identification power grows sharply in spatial and mobility data, where a home location and a work location together are nearly unique.
A common guardrail is **k-anonymity**: every combination of quasi-identifiers must appear at least k times, so no record stands alone.
When a combination is too rare you coarsen it — widen an age band, drop the last ZIP digits, aggregate to the week — trading a little resolution for real protection, as the worked example shows.

## Sharing pathogen and genomic data equitably

Fast, open sharing of pathogen genomes powers genomic surveillance, but it also raises questions of fairness that a FASTA file hides.
"Helicopter research" is the pattern where samples and data flow from lower-income settings to distant labs that publish first and share no benefit back.
Equitable sharing means rich, standardized metadata, clear provenance, authorship for the people who generated the samples, and benefit-sharing agreements negotiated up front.
Lukhele and colleagues review how genomic data science depends on exactly this governance layer to be both useful and just (Lukhele et al., 2025, *Annual Review of Genomics and Human Genetics*: [link](https://consensus.app/papers/details/2134b9b77e9a51dabe4c898e371fefc6/?utm_source=claude_desktop)).

## Dual-use research and biosafety

Some findings can help and harm — knowledge that improves a vaccine could also guide a bad actor — and this is called **dual-use research of concern** (DURC).
Biosafety awareness means recognizing when a method, sequence, or result warrants extra review before it is generated or published, and knowing who to ask.
You do not need to be a biosecurity specialist to hold this responsibility; you need to notice the question early, when it is still easy to act on.

## Where this sits in the One Health competencies

None of this is peripheral to the field's own definition of what a practitioner should know.
The One Health core-competency frameworks place "values and ethics" and "roles and responsibilities" at the center, alongside the technical domains (Frankson et al., 2016, *Frontiers in Public Health*: [link](https://consensus.app/papers/details/f73f3384df3157f19117c2872c3a3296/?utm_source=claude_desktop)).
The updated competencies keep ethics and stewardship as a foundational, cross-cutting domain rather than an optional add-on (Laing et al., 2023, *CABI One Health*: [link](https://consensus.app/papers/details/f8c069b3bd235270865949f75d841d98/?utm_source=claude_desktop)).

## A worked example

Suppose you hold twelve line-list records with four quasi-identifiers: an age band, the first three ZIP digits, sex, and the reporting week.
Grouped by the full combination, some groups are tiny: the group `(30-39, 021, F, 28)` has only two records, and `(40-49, 021, M, 28)` has two as well.
With a threshold of k = 5, three of the four combinations fail, meaning those people are re-identifiable from these fields alone.
Now coarsen by dropping the week — the least essential identifier for this analysis — and the records collapse into just two groups of size 5 and 7.
The minimum group size rises from 2 to 5, and every remaining combination clears the k = 5 bar, all without touching the two variables you actually need.

## In code

The check is a group-by on the quasi-identifiers, a size per group, and a comparison to the threshold.

### R

```r
library(dplyr)

records <- tibble(
  age_band = c(rep("30-39", 5), rep("40-49", 7)),
  zip3     = "021",
  sex      = c(rep("F", 5), rep("M", 7)),
  week     = c(27, 27, 27, 28, 28, 27, 27, 27, 27, 27, 28, 28)
)

records |>
  count(age_band, zip3, sex, week, name = "k") |>
  mutate(risk = k < 5)
```

### Python

```python
import pandas as pd

records = pd.DataFrame({
    "age_band": ["30-39"] * 5 + ["40-49"] * 7,
    "zip3":     ["021"] * 12,
    "sex":      ["F"] * 5 + ["M"] * 7,
    "week":     [27, 27, 27, 28, 28, 27, 27, 27, 27, 27, 28, 28],
})
K = 5

full = records.groupby(["age_band", "zip3", "sex", "week"]).size()
print("4 quasi-identifiers -> group sizes k:")
print(full.to_string())
print("failing combos:", list(full[full < K].index))
print(f"min k = {full.min()}, failing k<{K}: {(full < K).sum()} of {len(full)}")

coarse = records.groupby(["age_band", "zip3", "sex"]).size()   # drop 'week'
print(f"after coarsening -> min k = {coarse.min()}, "
      f"failing k<{K}: {(coarse < K).sum()} of {len(coarse)}")
```

<!-- python-output:auto -->
```text
4 quasi-identifiers -> group sizes k:
age_band  zip3  sex  week
30-39     021   F    27      3
                     28      2
40-49     021   M    27      5
                     28      2
failing combos: [('30-39', '021', 'F', 27), ('30-39', '021', 'F', 28), ('40-49', '021', 'M', 28)]
min k = 2, failing k<5: 3 of 4
after coarsening -> min k = 5, failing k<5: 0 of 2
```
<!-- /python-output:auto -->

### Julia

```julia
using DataFrames

records = DataFrame(
    age_band = [fill("30-39", 5); fill("40-49", 7)],
    zip3     = fill("021", 12),
    sex      = [fill("F", 5); fill("M", 7)],
    week     = [27, 27, 27, 28, 28, 27, 27, 27, 27, 27, 28, 28],
)

g = combine(groupby(records, [:age_band, :zip3, :sex, :week]), nrow => :k)
transform(g, :k => ByRow(<(5)) => :risk)
```

## Why it matters

An estimate built on data collected without consent, stored without safeguards, or extracted without benefit-sharing is not neutral just because the arithmetic is correct.
The habits on this page — review before collection, minimum necessary data, FAIR metadata, a k-anonymity check before you release, equitable credit — are what let your work be trusted and reused rather than quietly harmful.
Treat them as part of the analysis, applied in the same commits where you clean the data and fit the model, and they cost little; bolted on at the end, they cost the project.

## Related

- [Reproducibility](reproducibility.md)
- [Handling secrets](handling-secrets.md)
- [Spatial epidemiology and disease mapping](../spatial-epidemiology.md)
- [Genomic surveillance](../epidemiology/genomic-surveillance.md)
- [Programming and Computing](../programming.md)
