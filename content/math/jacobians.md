---
title: "Jacobians"
---

# Jacobians

## Example: SIR Model with Frequency-Dependent Transmission

Consider the [SIR model](sir.md): \[ \begin{aligned} \frac{dS}{dt} &= -\beta \frac{S I}{N} \\ \frac{dI}{dt} &= \beta \frac{S I}{N} - \gamma I \\ \frac{dR}{dt} &= \gamma I \end{aligned} \]

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

This Jacobian can be evaluated at a particular point (for example, the disease-free equilibrium $(S^*, I^*, R^*) = (N, 0, 0)$ to analyze [local stability](eigenvalues-and-eigenvectors.md) of the dynamical system.

:::spoiler Show the stability of the disease-free equilibrium

Evaluate the Jacobian at the disease-free equilibrium $(S, I, R) = (N, 0, 0)$.
With the infection term $\beta S I / N$, the partial derivatives at $I = 0$, $S = N$ give

\[
J_{\text{DFE}} = \begin{bmatrix} 0 & -\beta & 0 \\ 0 & \beta - \gamma & 0 \\ 0 & \gamma & 0 \end{bmatrix} .
\]

The characteristic polynomial factors as $\lambda^2(\beta - \gamma - \lambda) = 0$, so the eigenvalues are $\lambda_1 = 0$, $\lambda_2 = 0$, and $\lambda_3 = \beta - \gamma$.
The disease-free equilibrium is unstable — an outbreak can grow — exactly when the nonzero eigenvalue is positive:

\[
\beta - \gamma > 0 \iff R_0 = \frac{\beta}{\gamma} > 1 .
\]

So the eigenvalue that governs invasion recovers the familiar threshold $R_0 = 1$.

:::

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

## Related

- [Gradient](gradient.md)
- [Partial Derivatives](partial-derivatives.md)
- [Eigenvalues and Eigenvectors](eigenvalues-and-eigenvectors.md)
- [Matrix Operations](matrix-operations.md)
- [Inverse, Determinant, and Rank](matrix-inverse-and-determinant.md)
- [Equilibria and Linear Stability](equilibria-and-stability.md)
- [The Community Matrix and Stability](community-matrix.md)
- [Compartmental Models (SIR)](sir.md)
