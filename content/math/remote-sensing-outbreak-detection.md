---
title: "Remote Sensing, Object Counting, and Outbreak Detection"
description: "Turning overhead imagery into counts — cars in a hospital parking deck — and counts into an early outbreak signal, with a hard look at the assumptions that make or break the idea."
---

# Remote Sensing, Object Counting, and Outbreak Detection

Sometimes the most useful epidemiological signal is not a case report but a proxy for one — a sign that people are *behaving* as if sick before any of them are counted.
Hospital activity is one such proxy, and it is visible from above: a full parking deck is a crude, real-time gauge of how many people are seeking care.
This page ties three threads together — **remote sensing** (imagery of the physical world), **machine-learning object counting** (turning that imagery into numbers), and **outbreak detection** (turning numbers into an alarm) — using a hospital parking deck as the worked example.
It is deliberately a cautionary tale as much as a method: the pipeline is easy to build and easy to fool.

![Left: a synthetic overhead view of a hospital parking deck; a simple detector finds the dark car-shaped blobs and counts them. Right: the daily occupancy count becomes a time series, and a surge above the control limit trips an alarm. The imagery is synthetic and the detector deliberately crude — a licensing- and privacy-safe illustration, not a validated system.](../assets/figures/remote-sensing-outbreak-detection.svg)

## From classification to counting

The [convolutional networks](convolutional-networks-image.md) page asked *what is in this image?*.
Counting asks a harder question — *how many, and where?* — which is the task of **object detection**: locate every instance of a class and draw a box around it.
Modern detectors (the YOLO family, Faster R-CNN, RetinaNet) are CNNs with two heads on top of a shared backbone, one predicting a box's location and one its class, trained on images with boxes drawn by hand.
Count the boxes of class "car" and you have counted the cars.
For clean overhead imagery you often do not even need deep learning: cars are dark, roughly car-sized blobs on light asphalt, so classical computer vision — threshold the image, label the connected components, keep the car-sized ones — already gives a serviceable count, as in the figure and the runnable code below.
The deep detector earns its keep when the scene is cluttered, the lighting varies, or the objects are cells, mosquitoes, or people rather than cars.

## Remote sensing as a data source

**Remote sensing** is measurement at a distance — satellites, aircraft, drones, and fixed cameras imaging the physical world.
Epidemiology has long borrowed from it: satellite-derived rainfall, temperature, and vegetation feed [vector-borne disease](vector-borne.md) and [climate-forcing](climate-forcing-in-transmission-models.md) models, and night-time lights serve as a proxy for economic activity and population.
What is newer is using high-resolution overhead imagery of *human activity* — how full a parking lot is, how busy a road is — as a near-real-time behavioural signal.
The appeal is that it is passive, needs no cooperation from the people it observes, and can update daily; the peril, as below, is that it measures behaviour, and behaviour has many causes.

## The proxy chain, and its assumptions

The logic linking a parking count to disease is a chain of assumptions, each of which can break: \[ \text{cars parked} \;\to\; \text{hospital visits} \;\to\; \text{people seeking care} \;\to\; \text{disease burden}. \] Reading a rise in cars as a rise in disease assumes that occupancy tracks visits (not staff shifts, construction, or a nearby event), that visits track care-seeking (not elective procedures or visitors), that care-seeking tracks illness (not fear or a policy change), and that the illness is the one you care about.
None of these holds exactly, and several fail badly under exactly the conditions — a novel outbreak, a public scare — when you most want the signal.
The count is therefore best treated as **one weak, non-specific indicator** to be corroborated against specific data (syndromic surveillance, test positivity), never as a standalone diagnosis of an outbreak.

## From counts to an alarm

Once each day yields a count, you have a time series, and detecting an outbreak becomes detecting an **aberration** in that series — the subject of [aberration detection](../epidemiology/aberration-detection.md).
The simplest detector is a control chart: estimate a baseline mean and standard deviation from a quiet period, and flag any day that exceeds an upper control limit such as $\mu + 3\sigma$, as on the right of the figure.
More robust versions account for the day-of-week and seasonal structure (a deck is fuller on weekdays), use the [EWMA or CUSUM](../epidemiology/aberration-detection.md) to catch gradual rises, or feed the multivariate signal to a [variational autoencoder](variational-autoencoders.md) whose reconstruction error flags the unusual day.
The same [proper scoring](proper-scoring-rules.md) and validation discipline as any [forecast](reproduction-number-rt.md) applies: an alarm is a prediction, and it must be checked against what actually happened.

## A practical example: the Eden Terrace deck

Make it concrete with a real facility — the **Eden Terrace parking deck** serving a hospital campus, a long two-to-three-row deck plainly visible in overhead maps.
Imagine acquiring a daily overhead image of the deck, running a detector to count occupied bays, and plotting the count over time.
Suppose the deck holds about $180$ cars and typically sits near $150$ occupied on a weekday, and that over two weeks the daily count climbs past $210$ — above a $\mu + 3\sigma$ control limit built from the prior quiet months.
That is an alarm worth *a look*: it might reflect a wave of respiratory visits, or it might be a staff-parking change, a nearby road closure pushing cars onto the deck, a home football weekend, or simply better weather.
The figure and code here use a **synthetic** deck that mimics this layout — the pipeline is real, the imagery and numbers are invented, and every caveat in the next section applies with full force.

> [!WARNING]
> This example is illustrative only.
> It rests on many unverified assumptions, uses synthetic imagery in place of any real (and license-restricted) aerial photograph, and has not been validated against actual case data.
> Nothing here should be read as a claim that parking counts detected, or could detect, any specific outbreak.

## What the literature actually shows

The best-known attempt at exactly this was a 2020 analysis arguing that [satellite images of Wuhan hospital parking lots](https://dash.harvard.edu/handle/1/42669767), together with Baidu searches for symptoms, hinted at elevated activity in the autumn of 2019 (Nsoesie et al.).
It drew wide attention and equally wide criticism: the parking lots were confounded by seasonality, construction, and image-quality differences, the comparison images were sparse, and the search-term signal was weak — a textbook case of an intriguing proxy that cannot bear the causal weight placed on it.
The honest lesson is not that overhead imagery is useless but that it is *suggestive, not confirmatory*: it can flag where to look, and it fails when used as evidence on its own.
Remote sensing has firmer footing elsewhere in the field — night-time lights and mobility for population and movement, satellite climate variables for vector suitability — where the proxy chain is shorter and better validated.

## In code

### Python

Counting cars in a clean overhead image needs no neural network — threshold, label the connected components, and keep the car-sized ones:

```python
import numpy as np
from scipy import ndimage
rng = np.random.default_rng(7)

H, W = 96, 320                                      # a synthetic overhead deck
img = np.full((H, W), 0.78)                        # light asphalt
planted = 0
for ry in (26, 50, 74):                            # three rows of bays
    for cx in range(16, W - 12, 12):
        if rng.random() < 0.82:                    # ~82% of bays occupied
            planted += 1
            img[ry - 8:ry + 8, cx - 4:cx + 4] = rng.choice([.12, .18, .24, .30])
img = np.clip(img + 0.02 * rng.standard_normal((H, W)), 0, 1)

mask = img < 0.55                                  # dark pixels are cars
labels, n = ndimage.label(mask)                    # connected components
sizes = ndimage.sum(np.ones_like(labels), labels, range(1, n + 1))
detected = int((sizes > 30).sum())                 # keep car-sized blobs
print(f"planted {planted} cars, detected {detected}")
```

<!-- python-output:auto -->
```text
planted 62 cars, detected 62
```
<!-- /python-output:auto -->

Turning the daily count into an alarm is a control chart: baseline from a quiet period, then flag days above $\mu + 3\sigma$.

```python
days = np.arange(120)
base = 150 + 14 * np.sin(2 * np.pi * days / 7)      # weekly rhythm around 150
counts = base + rng.normal(0, 6, 120)
counts[104:] += np.linspace(0, 62, 16)              # a two-week surge
mu, sd = counts[:100].mean(), counts[:100].std()    # baseline from quiet weeks
ucl = mu + 3 * sd                                    # upper control limit
alarm_days = days[counts > ucl]
print(f"baseline mean {mu:.0f}, control limit {ucl:.0f}")
print(f"alarm on days: {alarm_days.tolist()}")
```

<!-- python-output:auto -->
```text
baseline mean 149, control limit 185
alarm on days: [113, 114, 115, 116, 118, 119]
```
<!-- /python-output:auto -->

For real overhead imagery a pretrained detector does the counting; the idiomatic pipeline (illustrative — it fetches model weights over the network, so it is shown, not run):

```python
# no-run
from ultralytics import YOLO                        # a pretrained object detector

model = YOLO("yolov8n.pt")                           # COCO-pretrained weights
result = model("deck_2026-07-11.jpg", classes=[2])   # class 2 = "car"
print(f"{len(result[0].boxes)} cars detected")
```

### R

```r
# torch/luz for detection; classical counting with EBImage (Bioconductor).
library(EBImage)
img  <- readImage("deck.png")
mask <- img < 0.55                       # threshold to car pixels
labs <- bwlabel(channel(mask, "gray"))   # connected components
n    <- max(labs)                        # number of blobs (approx. car count)
```

### Julia

```julia
# Images.jl + a connected-components pass for the classical route.
using Images, ImageMorphology
img  = Gray.(load("deck.png"))
mask = img .< 0.55
labels = label_components(mask)
ncars  = maximum(labels)
```

## Confounders, privacy, and validation

This idea lives or dies on three non-technical issues, and they deserve as much care as the model.

**Confounding.** A parking count responds to weather, holidays, day of week, staff schedules, construction, nearby events, and parking-policy changes far more reliably than to any single disease.
Without adjusting for these — and without a specific comparison series — a rise is uninterpretable, and the risk of crying wolf (or missing a real signal buried in the noise) is high.

**Privacy and ethics.** Persistent overhead surveillance of a specific facility, even counting only cars, raises real concerns: it can expose sensitive patterns (who visits a clinic, when), and imagery good enough to see cars can often see people or plates.
Aggregate to counts, avoid tracking individuals, respect the terms and copyright of the imagery source, and ask whether the public-health value justifies the surveillance at all.

**Validation.** A proxy is worthless until it is shown to track the thing you care about.
That means correlating the count against real case or syndromic data over a long period, quantifying its lead time and false-alarm rate with [proper scoring rules](proper-scoring-rules.md), and testing it prospectively before anyone acts on it.
An unvalidated proxy that *feels* predictive is exactly how a confounded coincidence becomes a confident mistake.

## Why it matters

Activity proxies from remote sensing are a genuine addition to the surveillance toolkit — cheap, passive, and fast — and object-counting models make them usable at scale.
At their best they are an early, non-specific tripwire that tells an epidemiologist *where to point the specific instruments*: test more here, pull the line list there.
But every strength is shadowed by the proxy chain's fragility, so the right posture is humility: treat the count as one weak signal among many, corroborate before believing, adjust for the obvious confounders, guard privacy, and validate against ground truth.
Used that way — as a hypothesis generator feeding the [aberration-detection](../epidemiology/aberration-detection.md) and [forecasting](reproduction-number-rt.md) machinery, not replacing it — remote sensing ties the physical world to the epidemiological one without overpromising.

## Related

- [Convolutional Networks and Image Identification](convolutional-networks-image.md)
- [Variational Autoencoders](variational-autoencoders.md)
- [Aberration Detection](../epidemiology/aberration-detection.md)
- [The Effective Reproduction Number and Forecasting](reproduction-number-rt.md)
- [Proper Scoring Rules](proper-scoring-rules.md)
- [Deep Learning, Foundation Models, and Agentic AI](deep-learning-agentic-models.md)
- [Climate Forcing in Transmission Models](climate-forcing-in-transmission-models.md)
- [Quantitative Methods](../math.md)
