---
title: "Within-Host Dynamics and the Immune Response"
description: "A compartmental model of virus replication inside one host, with B-cell (antibody) and T-cell (CTL) immunity, in the style of Nowak and May."
---

# Within-Host Dynamics and the Immune Response

The [SIR](sir.md) and [SEIR](seir-models.md) models track a pathogen as it spreads *between* hosts, but the same compartmental thinking describes what happens *inside* a single host.
Here the compartments are target cells, infected cells, and free virus, and the immune system plays the role that recovery and removal play at the population scale.
This page builds the standard within-host model and adds an explicit B-cell (antibody) and T-cell (CTL) response, following Nowak and May.

![Within-host virus dynamics under a strong immune response that clears the virus versus a weak response that persists, with the T-cell and B-cell effectors that drive clearance.](../assets/figures/within-host-dynamics.svg)

## The target-cell model

Let $x$ be uninfected target cells, $y$ infected cells, and $v$ free virus.
Target cells are produced at rate $\lambda$, die at per-capita rate $d$, and become infected on contact with virus at rate $\beta$.
Infected cells die at rate $a$ and shed virus at rate $k$; free virus is cleared at rate $u$.

\[
\begin{aligned}
\frac{dx}{dt} &= \lambda - d x - \beta x v \\
\frac{dy}{dt} &= \beta x v - a y \\
\frac{dv}{dt} &= k y - u v
\end{aligned}
\]

This is the exact analogue of the between-host compartmental model: susceptible target cells replace susceptible hosts, and infected cells replace infectious hosts.
The uninfected steady state is $x_0 = \lambda / d$, and the infection can establish only when the within-host basic reproductive ratio exceeds one.

\[
R_0 = \frac{\beta k x_0}{a u}
\]

The interpretation is the same as at the population scale: $R_0$ counts how many new infected cells one infected cell produces, through the burst of virus it releases, in an otherwise uninfected host.

## Adding B-cell and T-cell responses

The immune system removes virus in two complementary ways.
Cytotoxic T lymphocytes (CTL) kill infected cells, and antibodies produced by B cells neutralize free virus.
We add a CTL compartment $z$ that grows in response to infected cells and an antibody compartment $w$ that grows in response to virus.

\[
\begin{aligned}
\frac{dx}{dt} &= \lambda - d x - \beta x v \\
\frac{dy}{dt} &= \beta x v - a y - p y z \\
\frac{dv}{dt} &= k y - u v - q v w \\
\frac{dz}{dt} &= c y z - b z \\
\frac{dw}{dt} &= g v w - h w
\end{aligned}
\]

The term $p y z$ is extra killing of infected cells by CTL, and $q v w$ is neutralization of virus by antibody.
The effector equations are the same predator-prey logic used elsewhere in ecology: CTL proliferate at rate $c y$ in proportion to their infected-cell "prey" and decay at rate $b$, while antibody proliferates at rate $g v$ and decays at rate $h$.
This is why within-host immunology and [predator-prey](predator-prey.md) dynamics share so much mathematical structure.

## Clearance versus persistence

The strength of the adaptive response decides the outcome.
When CTL and antibody responses are strong, they drive infected cells and virus down to a low set point, far below the peak — functional clearance.
When the adaptive response is weak or absent, the virus is limited only by the supply of target cells and settles at a high, persistent set point, the hallmark of a chronic infection.
The figure above contrasts the two regimes for the same virus and the same initial seed, changing only the responsiveness of the effectors.

## A worked example

Take scaled parameters $\lambda = 1$, $d = 0.1$, $\beta = 1$, $a = 0.5$, $k = 5$, $u = 3$.
The uninfected target-cell level is $x_0 = \lambda/d = 10$, so \[ R_0 = \frac{\beta k x_0}{a u} = \frac{1 \cdot 5 \cdot 10}{0.5 \cdot 3} \approx 33, \] a vigorous infection.
Without an effective adaptive response the virus reaches the target-cell-limited set point $v^\* \approx 3.2$.
With a strong response the antibody set point $v^\* = h/g$ and the CTL set point $y^\* = b/c$ both fall as the effectors grow, pushing viral load down by about two orders of magnitude.

## In code

### R

```r
library(deSolve)

within_host <- function(t, y, p) {
  with(as.list(c(y, p)), {
    dx <- lam - d * x - beta * x * v
    dy <- beta * x * v - a * y - pk * y * z
    dv <- k * y - u * v - q * v * w
    dz <- c * y * z - b * z
    dw <- g * v * w - h * w
    list(c(dx, dy, dv, dz, dw))
  })
}

base <- c(lam = 1, d = 0.1, beta = 1, a = 0.5, k = 5, u = 3,
          pk = 1, q = 1, b = 0.3, h = 0.3)
y0 <- c(x = 10, y = 0, v = 1e-2, z = 1e-3, w = 1e-3)
t  <- seq(0, 200, by = 0.5)

strong <- ode(y0, t, within_host, c(base, c = 10, g = 10))
weak   <- ode(y0, t, within_host, c(base, c = 0,  g = 0))
tail(strong[, "v"], 1)   # low set point (clearance)
tail(weak[, "v"], 1)     # high set point (persistence)
```

### Python

```python
import numpy as np
from scipy.integrate import solve_ivp

lam, d, beta = 1.0, 0.1, 1.0
a, k, u = 0.5, 5.0, 3.0
p, q, b, h = 1.0, 1.0, 0.3, 0.3

def rhs(t, y, c, g):
    x, yi, v, z, w = y
    return [lam - d*x - beta*x*v,
            beta*x*v - a*yi - p*yi*z,
            k*yi - u*v - q*v*w,
            c*yi*z - b*z,
            g*v*w - h*w]

x0 = lam / d
R0 = beta * k * x0 / (a * u)
y0 = [x0, 0.0, 1e-2, 1e-3, 1e-3]
strong = solve_ivp(rhs, [0, 200], y0, args=(10.0, 10.0),
                   method="LSODA", rtol=1e-8, atol=1e-10, max_step=0.5)
weak = solve_ivp(rhs, [0, 200], y0, args=(0.0, 0.0),
                 method="LSODA", rtol=1e-8, atol=1e-10, max_step=0.5)
print(f"within-host R0 = {R0:.1f}")
print(f"strong immunity: set-point v = {strong.y[2][-1]:.3f}")
print(f"no adaptive immunity: set-point v = {weak.y[2][-1]:.3f}")
```

<!-- python-output:auto -->
```text
within-host R0 = 33.3
strong immunity: set-point v = 0.029
no adaptive immunity: set-point v = 3.233
```
<!-- /python-output:auto -->

### Julia

```julia
using DifferentialEquations

function within_host!(du, y, p, t)
    x, yi, v, z, w = y
    lam, d, beta, a, k, u, pk, q, b, h, c, g = p
    du[1] = lam - d*x - beta*x*v
    du[2] = beta*x*v - a*yi - pk*yi*z
    du[3] = k*yi - u*v - q*v*w
    du[4] = c*yi*z - b*z
    du[5] = g*v*w - h*w
end

y0 = [10.0, 0.0, 1e-2, 1e-3, 1e-3]
strong = solve(ODEProblem(within_host!, y0, (0.0, 200.0),
    (1,0.1,1,0.5,5,3,1,1,0.3,0.3, 10, 10)), Rosenbrock23())
last(strong.u)[3]   # low viral set point (stiff solver)
```

## Why it matters

Within-host models connect the molecular events of infection to the epidemiology of transmission.
The viral load they predict is what a diagnostic [qPCR](../diagnostics/qpcr.md) measures, what shapes the [infectiousness profile](../epidemiology/epidemiological-intervals.md) over the course of an infection, and what antiviral therapy tries to suppress.
They also set up the multi-scale view that links within-host selection to the between-host [evolution of virulence](evolution-of-virulence.md): a virus that replicates fast may reach a high transmissible load but provoke a stronger immune response or kill its host sooner, the same trade-off written one scale down.

## Related

- [The SIR Model](sir.md)
- [SEIR and Compartmental Extensions](seir-models.md)
- [Predator-Prey Dynamics](predator-prey.md)
- [The Evolution of Virulence](evolution-of-virulence.md)
- [Quantitative Methods](../math.md)
