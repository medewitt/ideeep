---
title: "Exponential and Logistic Growth"
---

# Exponential and Logistic Growth

Every population, from a bacterial colony to an outbreak's infected class, starts by growing in proportion to its own size.
In the case of bacterial growth undergoing binary fission, each generation begets two offspring, continuing.
Exponential and logistic growth are the two baseline models that describe this — the first for unlimited resources (rarely if ever the case in reality, but realistic in early growth periods), the second for the density dependence that eventually reins growth in due to limited resources driven by the resources or competition for the resources.

![Exponential growth rises without bound while logistic growth levels off at the carrying capacity K.](../assets/figures/logistic-growth.svg)

## Exponential growth

When each individual reproduces at a constant per-capita rate and nothing limits them, the population $N$ obeys $$\frac{dN}{dt}=rN,$$ where $r$ is the **intrinsic growth rate** (births minus deaths per individual per unit time).
This is the simplest [ordinary differential equation](derivatives.md) in ecology: the [rate of change](derivatives.md) is proportional to the current size.
Separating variables and integrating gives the closed-form solution $$N(t)=N_0\,e^{rt},$$ where $N_0=N(0)$ is the initial size.
Deriving this solution is a standard application of [integration](integrals.md) and the [exponential function](exponentials-and-logarithms.md).

When $r>0$ the population grows without bound; when $r<0$ it decays toward zero; when $r=0$ it stays put.

### Doubling time

A useful summary of exponential growth is the **doubling time** $t_2$, the time for the population to double.
Setting $N(t_2)=2N_0$ gives $e^{rt_2}=2$, so $$t_2=\frac{\ln 2}{r}\approx\frac{0.693}{r}.$$ The same $\ln 2/r$ formula (with $r$ the epidemic growth rate) gives the early doubling time of cases in an outbreak.

## Logistic growth

Unlimited growth is unrealistic: crowding reduces per-capita reproduction as resources run short.
The **logistic model** makes the per-capita rate decline linearly with density, $$\frac{dN}{dt}=rN\left(1-\frac{N}{K}\right),$$ where $K$ is the **carrying capacity** — the population size the environment can sustain.
When $N$ is small the bracket is near $1$ and growth is nearly exponential; as $N\to K$ the bracket goes to $0$ and growth stops.

The solution is the **sigmoid** (S-shaped) curve $$N(t)=\frac{K}{1+\left(\dfrac{K-N_0}{N_0}\right)e^{-rt}}.$$ It rises slowly at first, accelerates, then levels off at $K$.

:::spoiler Show how the sigmoid solution is obtained

Separate variables in $\frac{dN}{dt} = rN\!\left(1 - \frac{N}{K}\right)$:

\[
\frac{dN}{N\left(1 - N/K\right)} = r\,dt .
\]

Split the left side with partial fractions, $\dfrac{1}{N(1 - N/K)} = \dfrac{1}{N} + \dfrac{1/K}{1 - N/K}$, and integrate both sides:

\[
\ln N - \ln\!\left(1 - \frac{N}{K}\right) = rt + C \;\Longrightarrow\; \frac{N}{K - N} = A e^{rt},
\]

where $A = e^{C}$.
Fixing $A$ from the initial value $N(0) = N_0$ gives $A = \dfrac{N_0}{K - N_0}$, and solving for $N$ yields the sigmoid

\[
N(t) = \frac{K}{1 + \dfrac{K - N_0}{N_0}\,e^{-rt}} .
\]

:::

### Where growth is fastest

The absolute growth rate $dN/dt$ is a downward parabola in $N$, maximized where its derivative with respect to $N$ vanishes: $r(1-2N/K)=0$, i.e. at $$N=\frac{K}{2}.$$ At the inflection point $N=K/2$ the population is adding individuals fastest, at rate $rK/4$.

## Equilibria and stability

Setting $dN/dt=0$ gives two [equilibria](equilibria-and-stability.md): $N^*=0$ and $N^*=K$.
Linearizing $f(N)=rN(1-N/K)$ gives $f'(N)=r(1-2N/K)$.
At $N^*=0$, $f'(0)=r>0$, so the origin is **unstable** — a few individuals grow away from extinction.
At $N^*=K$, $f'(K)=-r<0$, so the carrying capacity is **stable** — perturbations decay back to $K$.

## A worked example

Take $r=0.5\ \text{yr}^{-1}$, $K=1000$, and $N_0=10$.
The doubling time during early (near-exponential) growth is $t_2=\ln 2/0.5\approx 1.39$ years.
Growth is fastest when $N=K/2=500$, at rate $rK/4=0.5\cdot 1000/4=125$ individuals per year.
Using the closed form at $t=10$ years: the factor $(K-N_0)/N_0=(1000-10)/10=99$, and $e^{-rt}=e^{-5}\approx 0.006738$, so $$N(10)=\frac{1000}{1+99\cdot 0.006738}=\frac{1000}{1.667}\approx 600.$$ The population has climbed from 10 to about 600 and is now just past its fastest-growth point.

## In code

We solve the logistic ODE numerically and overlay the exact sigmoid to confirm they agree.

### R

```r
library(deSolve)

logistic <- function(t, N, p) list(p$r * N * (1 - N / p$K))
p <- list(r = 0.5, K = 1000)
times <- seq(0, 20, by = 0.1)
out <- ode(y = c(N = 10), times = times, func = logistic, parms = p)

# closed form
N0 <- 10
exact <- p$K / (1 + ((p$K - N0) / N0) * exp(-p$r * times))
max(abs(out[, "N"] - exact))   # ~1e-4: numerical and exact agree
```

### Python

```python
import numpy as np
from scipy.integrate import solve_ivp

r, K, N0 = 0.5, 1000.0, 10. 
f = lambda t, N: r * N * (1 - N / K)
t = np.linspace(0, 20, 201)
sol = solve_ivp(f, (0, 20), [N0], t_eval=t, rtol=1e-8)

exact = K / (1 + ((K - N0) / N0) * np.exp(-r * t))
print(np.max(np.abs(sol.y[0] - exact)))  # ~1e-6: they match
print(exact[t == 10.0])                  # ~600 at t = 10
```

<!-- python-output:auto -->
```text
4.199852662623016e-05
[599.85960181]
```
<!-- /python-output:auto -->

### Julia

```julia
using DifferentialEquations

r, K, N0 = 0.5, 1000.0, 10.0
f(N, p, t) = r * N * (1 - N / K)
prob = ODEProblem(f, N0, (0.0, 20.0))
sol = solve(prob, Tsit5(); saveat = 0.1)

t = sol.t
exact = @. K / (1 + ((K - N0) / N0) * exp(-r * t))
maximum(abs.(sol.u .- exact))   # tiny: numerical solution matches the sigmoid
```

## Why it matters

Exponential growth is the null model of population change and the engine of early epidemic spread, where case counts double every $\ln 2/r$ time units.
The logistic adds the single most important biological correction — density dependence — which is exactly the mechanism that makes an epidemic's susceptible pool deplete and turns unlimited growth into a saturating curve.
Understanding these two models, their equilibria, and their stability is the foundation on which structured, discrete, and compartmental models are built.

## Related

- [Discrete-Time Models and the Logistic Map](discrete-population-models.md)
- [Equilibria and Stability](equilibria-and-stability.md)
- [Compartmental Models (SIR)](sir.md)
- [Derivatives](derivatives.md)
- [Integrals](integrals.md)
- [Exponentials and Logarithms](exponentials-and-logarithms.md)
- [Quantitative Methods](../math.md)
