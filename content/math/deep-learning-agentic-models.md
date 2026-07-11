---
title: "Deep Learning, Foundation Models, and Agentic AI"
description: "How the neural-network family fits together, what foundation models and attention add, and how agentic AI — a language model in a loop with tools — is starting to appear in outbreak analytics."
---

# Deep Learning, Foundation Models, and Agentic AI

The previous pages built up a family of neural networks — the [multilayer perceptron](neural-networks.md), the [recurrent LSTM](recurrent-networks-lstm.md), the [variational autoencoder](variational-autoencoders.md), the [convolutional network](convolutional-networks-image.md).
This page steps back to the shared idea that unites them, introduces the **transformer** and the **foundation models** built on it, and then turns to **agentic AI**: language models placed in a loop with tools, which are beginning to appear in outbreak analytics and public-health workflows.
The aim is a map and a sense of proportion — what is genuinely new, what is old machinery at new scale, and where the honest cautions lie.

![An agentic model is a language model in a loop with tools: it reasons about a goal, calls a tool such as a database query or an Rt model, observes the result, and repeats until it can hand a human a checked draft.](../assets/figures/deep-learning-agentic-models.svg)

## One idea, many architectures

Every network on these pages is the same recipe — compose simple linear-then-nonlinear units, and learn their weights by [gradient descent](optimization.md) on a loss via [backpropagation](neural-networks.md).
What differs is the **inductive bias**: the structure baked into the architecture to match the data.
A convolutional layer assumes *locality and translation equivariance*, right for images.
A recurrent layer assumes *sequential order*, right for time series.
An autoencoder assumes a *low-dimensional latent structure*, right for compression and generation.
Choosing an architecture is choosing which assumptions to hard-wire so the network does not have to learn them from scratch.

| Architecture | Inductive bias | Typical epidemiological use |
|---|---|---|
| [MLP](neural-networks.md) | none (fully connected) | tabular risk prediction, nowcasting from mixed signals |
| [CNN](convolutional-networks-image.md) | local, translation-equivariant | medical imaging, blood smears, X-rays |
| [RNN / LSTM](recurrent-networks-lstm.md) | sequential order | case-count and wastewater forecasting |
| [VAE](variational-autoencoders.md) | low-dimensional latent | anomaly detection, representation learning, [prior encoding](prior-encoding-vae.md) |
| Transformer | all-pairs attention | genomic sequences, clinical text, foundation models |

## Attention and the transformer

The **transformer** replaced recurrence with **attention**: instead of passing information step by step, every element of a sequence looks directly at every other and decides what to attend to.
For a set of vectors packed into queries $Q$, keys $K$, and values $V$, scaled dot-product attention is \[ \text{Attention}(Q, K, V) = \operatorname{softmax}\!\left(\frac{Q K^\top}{\sqrt{d}}\right) V, \label{eq:attn} \] where the softmax turns query–key similarities into weights that sum to one, and the output is a weighted blend of the values.
Because attention compares all positions at once, it captures long-range dependencies that defeat an [LSTM](recurrent-networks-lstm.md) and it parallelizes across the sequence, which is what made training on internet-scale data feasible.
Transformers now underpin protein-structure prediction, genomic language models, and the large language models below.

## Foundation models

A **foundation model** is a large network — almost always a transformer — pre-trained on a broad corpus with a self-supervised objective (predict the next token, fill in the masked pixel) and then adapted to many downstream tasks.
The strategy is [transfer learning](convolutional-networks-image.md) at scale: one expensive pre-training run yields general-purpose representations that fine-tune cheaply, or that can be steered with a prompt alone.
**Large language models** (LLMs) are foundation models for text; there are also foundation models for images, for protein and DNA sequences, and for electronic health records.
For public health they offer plausible value in summarizing literature, extracting structured data from unstructured clinical notes and outbreak reports, and drafting communications — always as a first pass a human verifies.

## Agentic AI

An **agentic model** is the shift from a model that *answers* to a model that *acts*.
Wrap a language model in a loop: give it a goal, let it choose and call **tools** — query a line-list database, run an [$R_t$ estimator](reproduction-number-rt.md), search the literature, render a map — observe each result, and repeat until the task is done, as in the figure.
The intelligence is the same transformer; the leverage is the loop and the tools it can reach, which let it break a messy goal into steps, gather evidence, and act on it rather than emit a single response.
In outbreak analytics this looks like an assistant that, asked whether a county's counts are aberrant, pulls the recent data, runs an [aberration-detection](../epidemiology/aberration-detection.md) routine and an $R_t$ model, cross-checks the literature for a plausible cause, and returns a draft situation brief with its evidence — leaving the epidemiologist to judge and sign off.

> [!WARNING]
> Agency multiplies both usefulness and risk.
> An agent that can *act* can act wrongly: run the wrong query, misread an ambiguous result, or state a fabricated fact ("hallucination") with the same fluent confidence as a true one.
> Keep a human in the loop for consequential decisions, demand that every claim carry its source and every number its computation, constrain which tools an agent may touch, and validate the end-to-end workflow — not just the model — before trusting it in surveillance or clinical settings.

## A worked example: one attention step

Attention is concrete once you compute it.
Take three tokens with 4-dimensional query, key, and value vectors.
Form the $3\times 3$ matrix of scaled dot products $QK^\top/\sqrt{d}$, softmax each row into attention weights, and blend the value vectors by those weights — the runnable code below does exactly this and prints the weight matrix, whose rows sum to one because each token distributes a unit of "attention" across all tokens.

## In code

### Python

The heart of a transformer — one attention step from [@eq:attn] — is a few lines of array math:

```python
import numpy as np
rng = np.random.default_rng(0)

def softmax(z):
    z = z - z.max(axis=-1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=-1, keepdims=True)

d = 4                                             # 3 tokens, 4-dim embeddings
Q = rng.standard_normal((3, d))
K = rng.standard_normal((3, d))
V = rng.standard_normal((3, d))
scores = Q @ K.T / np.sqrt(d)                     # query-key similarity
attn = softmax(scores)                            # weights, each row sums to 1
out = attn @ V                                    # blend the value vectors
print("attention weights:")
print(np.round(attn, 3))
print("row sums:", np.round(attn.sum(axis=1), 3))
```

<!-- python-output:auto -->
```text
attention weights:
[[0.226 0.475 0.298]
 [0.144 0.598 0.259]
 [0.668 0.235 0.097]]
row sums: [1. 1. 1.]
```
<!-- /python-output:auto -->

In practice you use the framework primitive; **PyTorch**'s `nn.MultiheadAttention` is the same operation, batteries included:

```python
import torch, torch.nn as nn
torch.manual_seed(0)

mha = nn.MultiheadAttention(embed_dim=4, num_heads=1, batch_first=True)
x = torch.randn(1, 3, 4)                       # one sequence: 3 tokens, dim 4
out, weights = mha(x, x, x)                     # self-attention: query = key = value
print("weights rows sum to 1:",
      bool(torch.allclose(weights.sum(-1), torch.ones(1, 3), atol=1e-5)))
print("output shape:", tuple(out.shape))
```

<!-- python-output:auto -->
```text
weights rows sum to 1: True
output shape: (1, 3, 4)
```
<!-- /python-output:auto -->

An agent loop is, in essence, a `while` loop around a model call and a tool call (illustrative — the Anthropic API call reaches the network, so it is shown, not run):

```python
# no-run
from anthropic import Anthropic
client = Anthropic()

def run_agent(goal, tools, max_steps=8):
    messages = [{"role": "user", "content": goal}]
    for _ in range(max_steps):
        reply = client.messages.create(model="claude-sonnet-5", tools=tools,
                                        messages=messages, max_tokens=1024)
        if reply.stop_reason != "tool_use":
            return reply                          # the agent is done
        result = dispatch_tool(reply)             # e.g. run an Rt model, query data
        messages += [{"role": "assistant", "content": reply.content},
                     {"role": "user", "content": result}]   # observe, then loop
```

### R

```r
# ellmer provides tool-calling agents against LLM backends in R.
library(ellmer)
chat <- chat_anthropic(model = "claude-sonnet-5")
chat$register_tool(tool(estimate_rt, "Estimate Rt from a case series",
                        cases = type_array("weekly case counts")))
chat$chat("Is the recent case series for county X growing?")
```

### Julia

```julia
# PromptingTools.jl supports tool/function calling for agentic workflows.
using PromptingTools
msg = aitools("Estimate Rt for the attached county series and flag if > 1";
              tools = [estimate_rt, query_linelist])
```

## Why it matters

Deep learning gives epidemiology a set of flexible function approximators, and agentic AI is beginning to give it assistants that can carry out multi-step analytical tasks.
Used well, they compress drudgery — reading images, fusing surveillance signals, extracting data from reports, drafting briefs — and free human experts for judgement.
But every architecture here is a *pattern learner*: it interpolates the data it was trained on and has no built-in notion of cause, of a novel dynamic, or of when it is wrong.
That is why these tools are strongest paired with the mechanistic and Bayesian models across this site — [renewal equations](renewal-equation.md), [compartmental models](sir.md), [hierarchical models](hierarchical-models.md) — which encode causal structure and honest uncertainty, and why the recurring discipline is the same one good epidemiology already demands: validate out of sample, quantify uncertainty, watch for bias, and keep a human accountable for the decision.

## Related

- [Neural Networks and the Multilayer Perceptron](neural-networks.md)
- [Recurrent Networks and LSTMs](recurrent-networks-lstm.md)
- [Variational Autoencoders](variational-autoencoders.md)
- [Encoding Spatial Priors with VAEs (PriorVAE)](prior-encoding-vae.md)
- [Convolutional Networks and Image Identification](convolutional-networks-image.md)
- [Epidemic Forecasting](../epidemiology/epidemic-forecasting.md)
- [Proper Scoring Rules](proper-scoring-rules.md)
- [Quantitative Methods](../math.md)
