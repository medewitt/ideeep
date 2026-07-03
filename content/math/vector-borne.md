---
title: "Vector-Borne Disease Models (Ross–Macdonald)"
---

# Vector-Borne Disease Models (Ross–Macdonald)

Malaria, dengue, and Zika do not pass directly from person to person — they travel through a biting insect, the vector.
Modeling them means coupling the infection dynamics of two populations, the human host and the mosquito, into a single system.

![$R_0$ grows with the square of the biting rate in the Ross–Macdonald model, so reducing biting is especially effective.](../assets/figures/vector-borne.svg)

## Why vector-borne is different

In a directly transmitted disease like the [SIR model](sir.md), an infectious human infects another human.
For a vector-borne disease the pathogen must make a round trip: an infectious human infects a mosquito, and later that mosquito infects a susceptible human.
Neither host can infect its own kind.
This two-step cycle is the defining feature of the Ross–Macdonald framework, developed by Ronald Ross and George Macdonald to understand malaria control.

## The Ross–Macdonald equations

Let $x$ be the fraction of humans currently infected and $y$ the fraction of mosquitoes infected.
The classic model tracks these two fractions:

\[
\begin{aligned}
\frac{dx}{dt} &= m\,a\,b\,y\,(1-x) - \gamma\,x \\
\frac{dy}{dt} &= a\,c\,x\,(1-y) - \mu\,y
\end{aligned}
\]

The parameters carry direct biological meaning:

- $m$ — number of mosquitoes per human host
- $a$ — mosquito biting rate (bites per mosquito per unit time)
- $b$ — transmission efficiency from an infectious mosquito to a human per bite
- $c$ — transmission efficiency from an infectious human to a mosquito per bite
- $\gamma$ — human recovery rate (so $1/\gamma$ is the mean human infectious period)
- $\mu$ — mosquito death rate (so $1/\mu$ is the mean mosquito lifespan)

Read the first equation as: susceptible humans (fraction $1-x$) are bitten by infectious mosquitoes and become infected, while infected humans recover at rate $\gamma$.
The rate at which one human is infected involves $m$ mosquitoes each biting at rate $a$, a fraction $y$ of them infectious, with per-bite success $b$.
The second equation is the mirror image for the mosquito population, but mosquitoes never "recover" — they simply die at rate $\mu$ and are replaced by susceptibles.

## The basic reproduction number

Applying the [next-generation matrix](next-generation-matrix.md) to the two-type transmission cycle gives

\[
R_0 = \frac{m\,a^2\,b\,c}{\mu\,\gamma}
\]

There is a clean way to read this.
A single infectious human, over an infectious period $1/\gamma$, delivers bites at rate $a$ to $m$ mosquitoes per human, infecting them with efficiency $c$: that is $m\,a\,c/\gamma$ newly infected mosquitoes.
Each infected mosquito survives for $1/\mu$ and bites humans at rate $a$, infecting them with efficiency $b$: that is $a\,b/\mu$ new human infections per mosquito.
The full human-to-human reproduction number is the product of these two half-cycles.

## Why the biting rate is squared

Notice that $a$ enters $R_0$ **squared**, while every other parameter enters linearly.
This is because a bite is needed in *each* direction of the transmission cycle — once to infect the mosquito and once for that mosquito to infect the next human.
The consequence is dramatic for control: halving the biting rate cuts $R_0$ by a factor of four, not two.
This quadratic leverage is why interventions that reduce biting or shorten mosquito lifespan — bed nets, indoor residual spraying, and larval control — are so much more powerful than they first appear, and it is the mathematical heart of Macdonald's argument that attacking adult mosquito survival is the most efficient path to malaria control.

## Threshold behavior

Setting the derivatives to zero gives the disease-free [equilibrium](equilibria-and-stability.md) $(x,y)=(0,0)$ and, when $R_0>1$, an endemic equilibrium with positive $x^*$ and $y^*$.
As with the SIR family, the disease-free state is stable precisely when $R_0<1$ and transmission establishes only when $R_0>1$.
Control succeeds not by eliminating every mosquito but by pushing the combination $m\,a^2\,b\,c/(\mu\gamma)$ below one.

## Worked example

Take representative malaria values: $m = 10$ mosquitoes per human, biting rate $a = 0.3\ \text{day}^{-1}$, transmission efficiencies $b = 0.5$ and $c = 0.5$, human recovery rate $\gamma = 0.01\ \text{day}^{-1}$ (a $100$-day infectious period), and mosquito death rate $\mu = 0.1\ \text{day}^{-1}$ (a $10$-day lifespan).

\[
R_0 = \frac{m\,a^2\,b\,c}{\mu\,\gamma}
    = \frac{10 \times 0.3^2 \times 0.5 \times 0.5}{0.1 \times 0.01}
    = \frac{10 \times 0.09 \times 0.25}{0.001}
    = \frac{0.225}{0.001} = 225.
\]

This very large $R_0$ reflects malaria's notorious persistence.
Now suppose bed nets halve the biting rate to $a = 0.15$: because $a$ is squared, $R_0$ falls to $225/4 \approx 56$ — still above one, showing why a single intervention rarely eliminates transmission but also why combining biting reduction with shorter mosquito survival is so effective.

## Simulation

We integrate the two-equation system from a small human infection seed and watch it approach the endemic equilibrium.

### R

```r
library(deSolve)

rm_model <- function(t, y, p) {
  with(as.list(c(y, p)), {
    dx <- m * a * b * yv * (1 - xh) - gamma * xh
    dyv <- a * c * xh * (1 - yv) - mu * yv
    list(c(dx, dyv))
  })
}

p  <- c(m = 10, a = 0.3, b = 0.5, c = 0.5, gamma = 0.01, mu = 0.1)
y0 <- c(xh = 0.01, yv = 0)          # 1% humans infected, no infected mosquitoes
t  <- seq(0, 365, by = 1)
out <- ode(y = y0, times = t, func = rm_model, parms = p)

# R0 = m*a^2*b*c/(mu*gamma) = 225
tail(out, 1)   # approaches endemic equilibrium (xh ~ 0.99, yv ~ 0.31)
matplot(out[, "time"], out[, c("xh", "yv")], type = "l",
        xlab = "day", ylab = "infected fraction", lty = 1)
```

### Python

```python
import numpy as np
from scipy.integrate import solve_ivp

def rm(t, u, m, a, b, c, gamma, mu):
    x, y = u
    return [m*a*b*y*(1 - x) - gamma*x,
            a*c*x*(1 - y) - mu*y]

pars = (10, 0.3, 0.5, 0.5, 0.01, 0.1)   # R0 = 225
sol = solve_ivp(rm, [0, 365], [0.01, 0.0], args=pars,
                t_eval=np.arange(0, 366), rtol=1e-8)

print(sol.y[:, -1].round(3))   # endemic eq ~ [0.99, 0.31]
```

### Julia

```julia
using DifferentialEquations

function rm!(du, u, p, t)
    x, y = u
    m, a, b, c, gamma, mu = p
    du[1] = m*a*b*y*(1 - x) - gamma*x
    du[2] = a*c*x*(1 - y) - mu*y
end

p  = (10.0, 0.3, 0.5, 0.5, 0.01, 0.1)   # R0 = 225
u0 = [0.01, 0.0]
prob = ODEProblem(rm!, u0, (0.0, 365.0), p)
sol  = solve(prob, Tsit5(), saveat = 1.0)

sol.u[end]   # endemic equilibrium ~ [0.99, 0.31]
```

## Why it matters

The Ross–Macdonald model is the foundation of quantitative malaria epidemiology and shapes vector-borne disease control to this day.
Its central insight — that the biting rate enters $R_0$ quadratically and mosquito survival enters strongly through $1/\mu$ — explains why bed nets, insecticides, and anything that shortens mosquito life yield outsized gains, and why source reduction alone is often not enough.
The same coupled-population logic extends to dengue, Zika, chikungunya, and Lyme disease, wherever a pathogen shuttles between a host and a biting vector.

## Related

- [The SIR Model](sir.md)
- [SEIR and Compartmental Extensions](seir-models.md)
- [The Next-Generation Matrix and R₀](next-generation-matrix.md)
- [Equilibria and Linear Stability](equilibria-and-stability.md)
- [Stochastic Epidemics and the Gillespie Algorithm](stochastic-epidemics.md)
- [Quantitative Methods](../math.md)
