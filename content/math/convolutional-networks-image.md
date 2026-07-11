---
title: "Convolutional Networks and Image Identification"
description: "How convolutional neural networks build image understanding from stacked local filters, with skin-lesion classification as the clinical example — and the caveats that come with it."
---

# Convolutional Networks and Image Identification

A photograph of a skin lesion is tens of thousands of pixels, and a plain [multilayer perceptron](neural-networks.md) that treated each pixel as an independent input would need a colossal number of weights and would still be blind to the fact that a feature means the same thing wherever it appears.
A **convolutional neural network** (CNN) exploits the structure of images directly: it slides small learned filters across the image, detecting the same local pattern — an edge, a texture, a colour transition — everywhere at once.
Stack these layers and the network builds understanding hierarchically, from edges to shapes to lesion-level features, which is what lets CNNs read radiographs, count cells, and flag a suspicious mole.

![A synthetic skin lesion (left), the response of an edge-detecting filter that lights up its irregular border (middle), and a blob filter that responds to the dark core (right) — the low-level features a CNN's first layers learn to extract.](../assets/figures/convolutional-networks-image.svg)

## The convolution operation

The core operation slides a small **filter** (or kernel) $\mathbf{K}$, say $3\times 3$, across the image $\mathbf{I}$ and, at each position, computes a weighted sum of the pixels under it: \[ (\mathbf{I} * \mathbf{K})_{ij} = \sum_{m}\sum_{n} \mathbf{I}_{i+m,\,j+n}\, \mathbf{K}_{m,n}. \label{eq:conv} \] The output is a **feature map** that is large where the local image patch resembles the filter.
Three properties make this the right operation for images.
The filter is **local**, looking at a small neighbourhood, matching how visual features are local.
Its weights are **shared** across all positions, so the same edge detector applies everywhere — far fewer parameters than a dense layer, and built-in **translation equivariance** (a feature shifted in the image shifts in the feature map).
And the filters are **learned** by [backpropagation](neural-networks.md), not hand-designed: the network discovers which patterns are worth detecting for the task.

A convolutional layer applies many filters, producing a stack of feature maps, and passes them through a nonlinear activation (usually [ReLU](neural-networks.md)).

## Pooling and depth

Between convolutions a **pooling** step downsamples each feature map — max pooling keeps the strongest response in each small window — shrinking the spatial resolution while retaining what was detected.
Pooling buys a measure of translation *invariance* and lets deeper layers see a larger effective region of the original image.
A typical CNN alternates convolution and pooling several times, so that early layers respond to edges and colour, middle layers to textures and motifs (the ragged border, the asymmetry), and late layers to whole-object concepts.
A final few [dense layers](neural-networks.md) map the top feature maps to class probabilities — "melanoma" versus "benign nevus", say — through a softmax.

## Transfer learning

Training a deep CNN from scratch needs enormous labelled datasets, which clinical imaging rarely has.
**Transfer learning** solves this: take a network already trained on millions of general images (its early layers have learned reusable edge and texture detectors), replace its final classification layer, and fine-tune on your smaller medical dataset.
The generic visual features transfer, so a dermatology classifier can be trained on thousands rather than millions of images — the standard recipe for medical-imaging models today.

## A worked example

Apply a vertical-edge filter $\mathbf{K} = \begin{bmatrix} 1 & 0 & -1 \\ 2 & 0 & -2 \\ 1 & 0 & -1 \end{bmatrix}$ to a $3\times 3$ patch that straddles a light–dark boundary, $\mathbf{I} = \begin{bmatrix} 9 & 9 & 1 \\ 9 & 9 & 1 \\ 9 & 9 & 1 \end{bmatrix}$.
By [@eq:conv] the response is $1\cdot 9 + 0\cdot 9 + (-1)\cdot 1 + 2\cdot 9 + 0\cdot 9 + (-2)\cdot 1 + 1\cdot 9 + 0\cdot 9 + (-1)\cdot 1 = 9-1+18-2+9-1 = 32$, a large positive value flagging the vertical edge.
A uniform patch (all $9$s) would give $1\cdot9 - 1\cdot9 + 2\cdot9 - 2\cdot9 + 1\cdot9 - 1\cdot9 = 0$: the filter fires on the transition, not the flat region.
Stacking millions of such responses, learned rather than fixed, is all a CNN is doing.

## In code

### Python

Convolution itself is a few lines — here the vertical-edge filter from the worked example run over a small image, showing the feature map that lights up the boundary:

```python
import numpy as np
from scipy.signal import correlate2d

img = np.array([[9, 9, 9, 1, 1],
                [9, 9, 9, 1, 1],
                [9, 9, 9, 1, 1],
                [9, 9, 9, 1, 1],
                [9, 9, 9, 1, 1]], dtype=float)
kernel = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])   # vertical-edge detector
feature_map = correlate2d(img, kernel, mode="valid")       # CNNs cross-correlate
print("feature map (edge responses):")
print(feature_map.astype(int))
```

<!-- python-output:auto -->
```text
feature map (edge responses):
[[ 0 32 32]
 [ 0 32 32]
 [ 0 32 32]]
```
<!-- /python-output:auto -->

For a runnable image-classification demonstration we use scikit-learn on the 8×8 handwritten-digit images — a small stand-in for a real diagnostic image set — training a network to identify each image's class:

```python
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

digits = load_digits()                                  # 1797 8x8 grayscale images
Xtr, Xte, ytr, yte = train_test_split(digits.data, digits.target,
                                      test_size=0.3, random_state=0)
clf = MLPClassifier(hidden_layer_sizes=(64,), max_iter=800,
                    random_state=0).fit(Xtr, ytr)
print(f"image classification test accuracy: {clf.score(Xte, yte):.3f}")
```

<!-- python-output:auto -->
```text
image classification test accuracy: 0.969
```
<!-- /python-output:auto -->

A real dermatology classifier needs a convolutional network and transfer learning; the idiomatic pipeline in Keras (illustrative — shown, not run):

```python
# no-run
import tensorflow as tf
from tensorflow.keras import layers, Model

base = tf.keras.applications.EfficientNetB0(include_top=False, weights="imagenet",
                                            input_shape=(224, 224, 3))
base.trainable = False                                   # start from transferred features
x = layers.GlobalAveragePooling2D()(base.output)
x = layers.Dropout(0.3)(x)
out = layers.Dense(2, activation="softmax")(x)           # benign vs malignant
model = Model(base.input, out)
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy",
              metrics=["accuracy", tf.keras.metrics.AUC(name="auc")])
# model.fit(train_ds, validation_data=val_ds, epochs=20)  # HAM10000 / ISIC images
```

### R

```r
# keras3 mirrors the Python API; transfer learning from a pretrained backbone.
library(keras3)
base <- application_efficientnet_b0(include_top = FALSE, weights = "imagenet",
                                    input_shape = c(224, 224, 3))
freeze_weights(base)
model <- keras_model_sequential() |>
  base() |>
  layer_global_average_pooling_2d() |>
  layer_dense(units = 2, activation = "softmax")
```

### Julia

```julia
# Flux + Metalhead provides pretrained CNN backbones for transfer learning.
using Flux, Metalhead
backbone = ResNet(18; pretrain = true).layers[1]
model = Chain(backbone, AdaptiveMeanPool((1, 1)), Flux.flatten,
              Dense(512 => 2), softmax)
```

## Why it matters, and where it misleads

CNNs are transforming diagnostic imaging: dermatology (classifying skin lesions from photographs, using datasets such as HAM10000 and the [ISIC](https://www.isic-archive.com/) archive), radiology (tuberculosis on chest X-rays, fractures, haemorrhages), pathology (tumour detection on whole-slide images), and ophthalmology (diabetic retinopathy from fundus photos), several now at or above specialist accuracy on curated test sets.
For infectious disease this reaches into the field: automated reading of malaria blood smears, identifying mosquito species or vector habitat from images, and phone-based triage of rashes where dermatologists are scarce.

But a medical image classifier is exactly where machine learning's failure modes bite hardest, so the caveats are not optional.
Dermatology training sets have historically **under-represented darker skin tones**, and a model that never saw them will fail on the patients who can least afford a missed melanoma.
CNNs latch onto **spurious correlates** — a model has learned to call lesions malignant because clinicians placed a ruler beside worrying ones, keying on the ruler, not the lesion.
Performance on a curated benchmark rarely survives the shift to a new clinic's camera, lighting, and patient mix, so **external, prospective validation** is essential before any clinical claim.
And a confident probability is not a calibrated one: these tools belong as a second reader that flags and defers to a clinician, not as an autonomous diagnosis.
The mathematics is powerful; the responsibility is in how honestly it is validated and deployed.

## Related

- [Neural Networks and the Multilayer Perceptron](neural-networks.md)
- [Deep Learning, Foundation Models, and Agentic AI](deep-learning-agentic-models.md)
- [Diagnostic Testing and Screening](diagnostic-testing.md)
- [Proper Scoring Rules](proper-scoring-rules.md)
- [Variational Autoencoders](variational-autoencoders.md)
- [Recurrent Networks and LSTMs](recurrent-networks-lstm.md)
- [Quantitative Methods](../math.md)
