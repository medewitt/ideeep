---
title: "Jacobians"
---

# Jacobians

## Example: SIR Model with Frequency-Dependent Transmission

Consider the SIR model:
\[
\begin{aligned}
\frac{dS}{dt} &= -\beta \frac{S I}{N} \\
\frac{dI}{dt} &= \beta \frac{S I}{N} - \gamma I \\
\frac{dR}{dt} &= \gamma I
\end{aligned}
\]

where:
- $\beta$ = transmission rate (frequency dependent)
- $\gamma$ = recovery rate
- $N = S + I + R$ = total population size

The [Jacobian matrix](https://en.wikipedia.org/wiki/Jacobian_matrix_and_determinant) for the system (with variables \(S, I, R\)) is:

\[
J =
\begin{bmatrix}
-\beta \frac{I}{N} & -\beta \frac{S}{N} & 0 \\
\beta \frac{I}{N} & \beta \frac{S}{N} - \gamma & 0 \\
0 & \gamma & 0 \\
\end{bmatrix}
\]

This Jacobian can be evaluated at a particular point (for example, the disease-free equilibrium $(S^*, I^*, R^*) = (N, 0, 0)$ to analyze local stability of the dynamical system.

## In Julia

Using the `Symbolics.jl` package, we can compute the Jacobian symbolically:

```julia
using Symbolics

@variables S, I, R, β, γ, N

# Define the system of ODEs
dS_dt = -β * S * I / N
dI_dt = β * S * I / N - γ * I
dR_dt = γ * I

# Create the vector of functions
f = [dS_dt, dI_dt, dR_dt]
vars = [S, I, R]

# Compute the Jacobian matrix
J = Symbolics.jacobian(f, vars)
```

To evaluate the Jacobian at a specific point (e.g., the disease-free equilibrium), we can use:

```julia
using Symbolics

@variables S, I, R, β, γ, N

# Define the system
dS_dt = -β * S * I / N
dI_dt = β * S * I / N - γ * I
dR_dt = γ * I

f = [dS_dt, dI_dt, dR_dt]
vars = [S, I, R]

# Compute the Jacobian
J = Symbolics.jacobian(f, vars)

# Evaluate at disease-free equilibrium: (S*, I*, R*) = (N, 0, 0)
J_DFE = substitute(J, Dict(S => N, I => 0, R => 0))
```

Alternatively, for numerical evaluation, you can use `ForwardDiff.jl`:

```julia
using ForwardDiff

function sir_model(u, p)
    S, I, R = u
    β, γ, N = p
    
    dS = -β * S * I / N
    dI = β * S * I / N - γ * I
    dR = γ * I
    
    return [dS, dI, dR]
end

# Parameters
β = 0.5
γ = 0.1
N = 1000.0
p = [β, γ, N]

# Point to evaluate Jacobian
u = [N, 0.0, 0.0]  # Disease-free equilibrium

# Compute Jacobian numerically
J = ForwardDiff.jacobian(u -> sir_model(u, p), u)
```


