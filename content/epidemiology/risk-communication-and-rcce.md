---
title: "Risk Communication and Community Engagement (RCCE)"
description: "The timely, accurate, two-way exchange of information between authorities and at-risk people, treated as a core epidemiologic function rather than a press-office afterthought."
---

# Risk Communication and Community Engagement (RCCE)

An outbreak response is only as good as the information that reaches the people who must act on it.
Risk communication and community engagement (RCCE) is the timely, accurate, two-way exchange of information, advice, and opinion between experts or officials and the people who face a threat.
Treated seriously, it is a core epidemiologic function on equal footing with surveillance and case investigation, not a message drafted after the science is done.

![A jargon-heavy message and its plain-language rewrite scored on the Flesch Reading Ease scale, where the rewrite is markedly easier to read.](../assets/figures/risk-communication-and-rcce.svg)

## A core capacity, not an afterthought

Risk communication is one of the eight core capacities that the International Health Regulations (IHR 2005) require every country to build and maintain.
It sits alongside surveillance, laboratory diagnostics, and response, because a detection that no one can act on prevents nothing.
Reviews of the European COVID-19 response found risk communication repeatedly under-resourced and improvised, despite this formal mandate ([Warren et al., 2021, Journal of Risk Research](https://doi.org/10.1080/13669877.2021.1947874)).
Building the capacity deliberately, rather than assembling it during a crisis, is what the regulation actually asks for ([Capurro et al., 2025, Canadian Journal of Public Health](https://doi.org/10.17269/s41997-025-01002-y)).

## The communication continuum

It helps to think of engagement along a continuum of increasing participation.
One-way dissemination pushes information out: a press release, a poster, a broadcast advisory.
Two-way dialogue listens back, so that questions, rumors, and lived constraints from the community shape the next message.
Three-way community participation goes further, treating affected people as partners who help design and deliver the response itself.
Responses that stop at one-way dissemination tend to fail, because behavior change depends on trust and relevance that only dialogue can build ([Bardosh et al., 2020, Globalization and Health](https://doi.org/10.1186/s12992-020-00652-6)).

![The risk-communication continuum from one-way dissemination through two-way dialogue to three-way community participation.](../assets/figures/rcce-communication-continuum.svg)

## Audiences are not one public

There is no single "general public," and a message tuned to an average reaches no one well.
Audience segmentation divides the population into groups that differ in risk, language, media habits, and trust, so that each receives something usable.
This matters most for equity-deserving groups, those who are marginalized by language, disability, migration status, or distrust rooted in past mistreatment, and who are often at highest risk yet hardest to reach.
Reaching them is not a matter of translating the same leaflet, but of engaging trusted local voices and channels that already carry weight in those communities.

## Plain language and the curse of knowledge

Once an expert knows a concept, it becomes almost impossible to imagine not knowing it, a bias called the curse of knowledge.
Jargon such as "attack rate," "nonpharmaceutical intervention," or "seroprevalence" then leaks into public messages that the audience cannot parse.
Plain-language design is the discipline of writing for the reader's vocabulary and reading level, using short sentences, common words, and concrete instructions.
Readability formulas give a rough, automatable check on whether a message has drifted out of reach, which the worked example below makes concrete.

## Trust, and how to keep it

Trust is the currency of risk communication, slow to earn and quick to spend.
It is built by being first, being right, being credible, and being empathetic, and by openly acknowledging what is not yet known.
Crucially, trust is earned at the individual level: it is not conferred on institutions by default but built person by person, through each honest and reliable interaction.
Trust is built by being clear, credible, and openly acknowledging what is not yet known.
A single confident claim that later proves wrong can undo months of careful engagement, which is why honesty about uncertainty protects trust rather than eroding it.

## Infodemics and misinformation

An outbreak of disease now travels alongside an outbreak of information.
Misinformation is false content shared without intent to harm; disinformation is false content spread deliberately to deceive.
An infodemic is the overwhelming flood of both, mixed with accurate information, that makes it hard for people to find trustworthy guidance when they need it.
Infodemic management treats this as a measurable problem: listening for circulating rumors, filling information voids quickly, and amplifying credible sources rather than only debunking false ones.

![A false rumor spreading widely through a social network compared with an accurate pamphlet that is true but reaches far fewer people.](../assets/figures/misinformation-network-reach.svg)

## Communicating uncertainty honestly

Epidemic forecasts are probabilistic, and pretending otherwise sets up the audience to feel misled when reality lands in the tail.
Honest communication reports ranges and probabilities, explains why the future is uncertain, and distinguishes what is known from what is estimated.
Well-designed probabilistic messages, paired with [proper scoring rules](../math/proper-scoring-rules.md) to hold forecasters accountable, let people plan for a distribution of outcomes instead of a single wrong number.

## A worked example

Take one public-health message written two ways.
The jargon-heavy version reads: "Implementation of nonpharmaceutical interventions necessitates epidemiological characterization of transmission heterogeneity prior to operationalization of mitigation strategies."
The plain rewrite carries the same meaning: "Some people catch this illness more easily than others.
We must find out who is most at risk first.
Then we can choose the best ways to keep them safe."
The Flesch Reading Ease score combines average sentence length and average syllables per word, on a scale where higher is easier and roughly 60 is plain English.
Scoring both by hand gives about -137 for the jargon version, effectively unreadable, and about 101 for the rewrite, a gain of some 238 points from nothing but word and sentence choice.

## In code

We implement Flesch Reading Ease from scratch, counting sentences by terminal punctuation, words by whitespace, and syllables with a simple vowel-group heuristic.

### R

```r
syllables <- function(word) {
  w <- tolower(gsub("[^a-z]", "", word, ignore.case = TRUE))
  if (nchar(w) == 0) return(0)
  g <- length(gregexpr("[aeiouy]+", w)[[1]])
  if (grepl("e$", w) && g > 1) g <- g - 1
  max(1, g)
}
flesch <- function(text) {
  sents <- max(1, lengths(regmatches(text, gregexpr("[.!?]", text))))
  words <- strsplit(text, "\\s+")[[1]]
  syl <- sum(sapply(words, syllables))
  206.835 - 1.015 * (length(words) / sents) - 84.6 * (syl / length(words))
}
```

### Python

```python
import numpy as np

def syllables(word):
    w = "".join(c for c in word.lower() if c.isalpha())
    if not w:
        return 0
    vowels = "aeiouy"
    groups, prev = 0, False
    for c in w:
        is_v = c in vowels
        if is_v and not prev:
            groups += 1
        prev = is_v
    if w.endswith("e") and groups > 1:
        groups -= 1
    return max(1, groups)

def flesch(text):
    sentences = max(1, sum(text.count(p) for p in ".!?"))
    words = text.split()
    n_syll = sum(syllables(w) for w in words)
    return 206.835 - 1.015 * (len(words) / sentences) - 84.6 * (n_syll / len(words))

jargon = ("Implementation of nonpharmaceutical interventions necessitates "
          "epidemiological characterization of transmission heterogeneity "
          "prior to operationalization of mitigation strategies.")
plain = ("Some people catch this illness more easily than others. "
         "We must find out who is most at risk first. "
         "Then we can choose the best ways to keep them safe.")

scores = np.array([flesch(jargon), flesch(plain)])
print("jargon-heavy score:", round(float(scores[0]), 1))
print("plain-language score:", round(float(scores[1]), 1))
print("gain in readability:", round(float(scores[1] - scores[0]), 1), "points")
print("higher is easier; the rewrite is far more readable")
```

<!-- python-output:auto -->
```text
jargon-heavy score: -137.2
plain-language score: 100.8
gain in readability: 238.0 points
higher is easier; the rewrite is far more readable
```
<!-- /python-output:auto -->

### Julia

```julia
function syllables(word)
    w = lowercase(filter(isletter, word))
    isempty(w) && return 0
    g = length(collect(eachmatch(r"[aeiouy]+", w)))
    endswith(w, "e") && g > 1 && (g -= 1)
    max(1, g)
end
function flesch(text)
    sents = max(1, count(c -> c in ".!?", text))
    words = split(text)
    syl = sum(syllables.(words))
    206.835 - 1.015 * (length(words) / sents) - 84.6 * (syl / length(words))
end
```

## Why it matters

The best surveillance and the sharpest model change nothing if the guidance they produce cannot be understood, trusted, and acted on by the people at risk.
RCCE is the function that closes that gap, and it fails predictably when it is improvised late, written in jargon, or pushed one way into communities that were never engaged.
Notably, science communication is rarely a formal part of scientific training, so most epidemiologists were never taught it ([Singh et al., 2021, Neuropsychopharmacology](https://doi.org/10.1038/s41386-021-01084-5)).
The encouraging finding is that structured training measurably improves it, so this is a skill to build rather than a talent to hope for ([Greer et al., 2024, European Journal of Public Health](https://doi.org/10.1093/eurpub/ckae144.441)).
Formal training of this kind already exists and is used in practice: the CDC's Crisis and Emergency Risk Communication (CERC) program is a widely adopted body of training and doctrine that guides how responders communicate during investigations and outbreak responses.
Its core principles are compact and teachable: be first, be right, be credible, express empathy, promote action, and show respect.
CERC is a concrete demonstration that risk communication can be taught as a discipline rather than left to improvisation.

## Related

- [Communicating uncertainty and proper scoring rules](../math/proper-scoring-rules.md)
- [Social and structural drivers of transmission](social-drivers-of-transmission.md)
- [Qualitative and mixed methods](qualitative-and-mixed-methods.md)
- [Scientific writing](../scientific-writing.md)
- [Epidemiology](../epidemiology.md)
