---
title: "Writing Results and Discussion"
---

# Writing Results and Discussion

Results says what happened.
Discussion says what it means.
Keeping that line clean is the single most useful habit for these two sections.
Everything the reader needs to trust your findings goes in Results, reported without interpretation.
Everything you want the reader to take away goes in Discussion, where interpretation is the whole point.

This page complements [scientific writing](../scientific-writing.md), which covers the paper as a whole.
Here we focus on the two sections that most often blur into each other.

## Results: led by the figures

Design the figures first, then write the prose that walks the reader through them.
A reader should be able to follow your argument from the figures and captions alone (see [graphing data](../math/graphing-data.md)).
The text points to each figure and table and states the finding in plain words, past tense, without saying what it means.

A few rules keep a Results section honest and readable.

- One message per figure.
Give each figure a single job and lead the paragraph with that job.
- Report direction and magnitude, not just significance.
"A significant effect" tells the reader nothing.
"Cases fell by 40 percent" tells them what happened.
- Report effect sizes with uncertainty.
Give the estimate with a confidence or credible interval, not a bare p-value (see [confidence intervals](../math/confidence-intervals.md)).
- Lead with the important result.
Within each subsection, the headline comes first and gets the most space.
Condense null and secondary results into short combined statements.
- Stay in the past tense and keep out interpretation.
Mechanism, comparison to theory, and "so what" belong in the Discussion.

The order of results follows the argument, not the order in which you ran the analyses.
If one result clarifies another, present them in the order that reads best, and match the Methods to that order.

## Discussion: narrow to broad

The Discussion is the inverted funnel, the mirror image of the Introduction.
It opens narrow with your key finding and widens outward to the field.

1. Restate the key finding in one or two sentences, with a figure call-out.
2. Interpret it.
Offer the mechanism or explanation for what you found.
3. Place it against prior work.
Say where your result agrees with the literature and where it does not, and why.
4. State limitations honestly and specifically.
Name the actual threats to your conclusion, not boilerplate.
"Sample size was small" says little; "with 12 transmission pairs the serial-interval tail is poorly constrained" tells the reader exactly what to distrust.
5. Give the implications for the field, ending broad.

Order the interpretation paragraphs by importance, and give space in proportion to importance.
Three to five paragraphs is normal.
More than five is a signal to move specialist material to supplementary information.
Never open on a limitation, and never simply repeat the Results.
Close on a forward-looking sentence, not "further research is needed," which is always true and adds nothing.

## A worked skeleton

> **Results**
> Lead paragraph, headline finding: plain statement of what changed, with direction and magnitude (estimate and interval), pointing to Figure 1.
> Supporting paragraph: secondary and null results, condensed, with combined reporting.
>
> **Discussion**
> P1, summary: the key finding restated, with a figure call-out.
> P2, most important result: interpretation, agreement or disagreement with prior work, one specific limitation, a testable next step.
> P3 onward: remaining results in decreasing order of importance, same shape.
> Final paragraph: the implication for the field, ending on a single memorable sentence.

## A worked example

Suppose the study estimated the pre-symptomatic share of transmission for a respiratory pathogen.

> **Results.**
> Pre-symptomatic infections accounted for 48 percent of transmission (95% CI 39 to 57 percent; Figure 2).
> The estimated serial interval was shorter than the incubation period, producing negative serial intervals in 12 percent of pairs (Figure 1).
>
> **Discussion.**
> Nearly half of transmission occurred before symptom onset (Figure 2), which places this pathogen among those where symptom-based isolation alone cannot hold the reproduction number below one.
> The short serial interval relative to the incubation period is the mechanism, and it matches earlier contact-tracing estimates for related pathogens while exceeding the fraction reported by studies that excluded household pairs.
> The estimate rests on 84 transmission pairs, so the upper tail of the pre-symptomatic fraction is not tightly constrained, and recall bias in reported onset dates could shift the serial interval.
> If the pattern holds, control will depend on measures that act before symptoms appear, such as testing of contacts, rather than on isolation triggered by illness.

Notice that the Results state the numbers and point to the figures with no interpretation, and the Discussion supplies the mechanism, the comparison, the specific limitation, and the implication in that order.

## Related

- [Scientific Writing](../scientific-writing.md)
- [Writing Methods](writing-methods.md)
- [Writing an Abstract](writing-an-abstract.md)
- [Graphing Data](../math/graphing-data.md)
- [Scientific & Policy Writing](../writing.md)
