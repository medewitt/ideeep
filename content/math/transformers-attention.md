---
title: "Transformers and Attention"
description: "How self-attention lets every element of a sequence look at every other, and how stacking it into transformer blocks built the architecture behind foundation models."
---

# Transformers and Attention

The [deep-learning overview](deep-learning-agentic-models.md) introduced attention in a sentence; it deserves a page, because the **transformer** is the single most consequential neural architecture of the last decade and the engine under every [foundation model](deep-learning-agentic-models.md).
Its core idea is **self-attention**: rather than processing a sequence step by step like an [LSTM](recurrent-networks-lstm.md), let every element look directly at every other and decide, for itself, what to pay attention to.
That one operation — parallelizable and able to reach across an entire sequence at once — is what let models train on internet-scale data, and it powers genomic language models, protein-structure prediction, and clinical-text understanding as readily as it powers chatbots.

![Left: a self-attention weight matrix over a short sentence — each row shows how much a token attends to every other, forming blocks because related tokens (symptom words, function words) attend to one another. Right: the scaled dot-product attention pipeline that produces those weights, from queries, keys, and values to a weighted blend.](../assets/figures/transformers-attention.svg)

## Self-attention

Each element of the input is first turned into three vectors by learned linear maps: a **query** $\mathbf{q}$ (what am I looking for?), a **key** $\mathbf{k}$ (what do I offer?), and a **value** $\mathbf{v}$ (what do I carry?).
A token's query is compared against every token's key by a dot product, the scores are scaled and softmaxed into weights that sum to one, and the output is the weighted average of the values.
Stacking the per-token vectors into matrices $Q$, $K$, $V$, the whole operation is one expression: \[ \text{Attention}(Q, K, V) = \operatorname{softmax}\!\left(\frac{Q K^\top}{\sqrt{d_k}}\right) V, \label{eq:attention} \] where $d_k$ is the key dimension and the $\sqrt{d_k}$ scaling keeps the dot products from growing large and saturating the softmax.
The softmaxed matrix is exactly the heatmap on the left of the figure: row $i$ says how much token $i$ draws from each other token, and because it is a genuine average over *all* positions, a token can pull information from the far end of the sequence in a single step — the long-range reach an [LSTM](recurrent-networks-lstm.md) struggles for.

## Multi-head attention and positional encoding

One attention operation captures one kind of relationship; a transformer runs several in parallel.
**Multi-head attention** projects the input into $h$ independent sets of queries, keys, and values, applies attention [@eq:attention] in each **head**, and concatenates the results, so different heads can specialize — one tracking syntax, another long-range dependencies, another, in a genomic model, base-pairing.
Attention has one blind spot: it is **permutation-invariant**, treating the input as a *set*, so on its own it cannot tell "cough since Monday" from "Monday since cough".
The fix is **positional encoding** — adding to each element a vector that encodes its position (classically a bank of sines and cosines of different frequencies) — so order is restored as information the attention can use.

## The transformer block

A transformer stacks identical **blocks**, each pairing a multi-head self-attention layer with a small position-wise [feedforward network](neural-networks.md), and wrapping both in two tricks that make deep stacks trainable: a **residual connection** (add the input back to the output) and **layer normalization**.
Two structural variants matter.
An **encoder** uses unmasked self-attention so every token sees the whole sequence — right for understanding tasks (classify a clinical note, embed a genome).
A **decoder** uses **causal masking** so a token sees only earlier positions — right for generation, where the model predicts the next token from the past, the mechanism behind [large language models](deep-learning-agentic-models.md).
**Cross-attention**, where queries come from one sequence and keys/values from another, links the two in translation-style tasks.

## Why it took over

The transformer displaced recurrent networks for three reasons.
It is **parallel**: every position is processed at once, not one step at a time, so it trains far faster on modern hardware.
It has a **short path** between any two positions — one attention hop — so gradients and information travel across long sequences without the vanishing-gradient decay that plagues [RNNs](recurrent-networks-lstm.md).
And it **scales**: performance keeps improving predictably with more data, parameters, and compute, which is what made [foundation models](deep-learning-agentic-models.md) possible.
The cost is that attention is $\mathcal{O}(L^2)$ in the sequence length $L$ — every token attends to every other — which is why long-sequence variants (sparse, linear, and windowed attention) are an active field, especially for genomics, where sequences are enormous.

## A worked example

Take three tokens with $d_k = 4$.
Form the $3\times 3$ matrix of scaled dot products $QK^\top/\sqrt{4}$; softmax each row so its three weights sum to one; then multiply by $V$ to blend the value vectors by those weights.
If token 1's query aligns most with token 2's key, row 1 of the softmax puts the most weight on token 2, so token 1's output is dominated by token 2's value — token 1 has "attended to" token 2.
Running this in every head and every block, over billions of tokens, is the whole of a transformer.

## In code

### Python

Positional encodings and a full transformer encoder block are a few lines with PyTorch — here we build the sinusoidal positions and run one encoder layer over a short sequence:

```python
import numpy as np, torch, torch.nn as nn
torch.manual_seed(0)

def positional_encoding(seq_len, d):            # sinusoidal position vectors
    pos = np.arange(seq_len)[:, None]
    i = np.arange(d)[None, :]
    angle = pos / (10000 ** (2 * (i // 2) / d))
    return np.where(i % 2 == 0, np.sin(angle), np.cos(angle))

pe = positional_encoding(seq_len=6, d=16)
layer = nn.TransformerEncoderLayer(d_model=16, nhead=4, dim_feedforward=32,
                                   batch_first=True)               # one block
x = torch.randn(1, 6, 16) + torch.tensor(pe, dtype=torch.float32)  # tokens + positions
out = layer(x)                                    # self-attention + FFN + residuals
print("positional encoding shape:", pe.shape)
print("encoder output shape:", tuple(out.shape))
print("block parameters:", sum(p.numel() for p in layer.parameters()))
```

<!-- python-output:auto -->
```text
positional encoding shape: (6, 16)
encoder output shape: (1, 6, 16)
block parameters: 2224
```
<!-- /python-output:auto -->

In practice you rarely build one from scratch — you load a pretrained transformer for your domain (illustrative — HuggingFace fetches weights over the network, so shown, not run):

```python
# no-run
from transformers import AutoModel, AutoTokenizer

# a genomic language model: a transformer pretrained on DNA sequences
tok = AutoTokenizer.from_pretrained("InstaDeepAI/nucleotide-transformer-500m-human-ref")
model = AutoModel.from_pretrained("InstaDeepAI/nucleotide-transformer-500m-human-ref")
emb = model(**tok("ACGTACGTACGT", return_tensors="pt")).last_hidden_state
```

### R

```r
# torch for R exposes nn_transformer_encoder_layer; text/keras3 for NLP pipelines.
library(torch)
layer <- nn_transformer_encoder_layer(d_model = 16, nhead = 4,
                                      dim_feedforward = 32, batch_first = TRUE)
out <- layer(torch_randn(1, 6, 16))
```

### Julia

```julia
# Transformers.jl implements attention, multi-head blocks, and pretrained models.
using Transformers, Transformers.Layers
block = TransformerBlock(4, 16, 32)     # heads, model dim, feedforward dim
y = block(randn(Float32, 16, 6))        # (features, sequence length)
```

## Why it matters

Transformers are not just for language.
In genomics, DNA and protein **language models** (the Nucleotide Transformer, DNABERT, ESM) pretrain on sequence and transfer to variant-effect prediction, regulatory-element detection, and function annotation; **AlphaFold** uses attention over residues to predict protein structure, reshaping structural biology.
In clinical data, transformers read unstructured notes to extract diagnoses and outcomes, and structured-EHR transformers model a patient's timeline as a sequence of events.
The same cautions from the [foundation-model](deep-learning-agentic-models.md) and [overfitting](overfitting-regularization.md) pages apply with force — these models are enormous pattern-matchers that must be validated, calibrated, and watched for the biases in their training data — but the architecture itself is now the default whenever the data are a sequence and the relationships are long-range.

## Related

- [Deep Learning, Foundation Models, and Agentic AI](deep-learning-agentic-models.md)
- [Recurrent Networks and LSTMs](recurrent-networks-lstm.md)
- [Neural Networks and the Multilayer Perceptron](neural-networks.md)
- [Convolutional Networks and Image Identification](convolutional-networks-image.md)
- [Phylogenetic Inference](phylogenetic-inference.md)
- [Quantitative Methods](../math.md)
