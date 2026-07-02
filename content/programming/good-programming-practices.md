---
title: "Good Programming Practices"
---

# Good Programming Practices

Code you write for an analysis is read far more often than it is written — by reviewers, by collaborators, and by you six months from now. A few habits make your code easier to read, harder to break, and cheaper to fix.

## Name things well

Names are the cheapest documentation you have. Spend them wisely.

- **Functions are verbs / actions**: `simulate_epidemic`, `fit_model`, `load_cases`.
- **Variables are nouns**: `case_count`, `contact_matrix`, `posterior_draws`.
- **Booleans are yes/no questions**: `is_infected`, `has_converged`, `should_resample`.

```r
# BAD: opaque, abbreviated, ambiguous
d <- read.csv("f.csv")
x <- d[d$v > 0, ]
flag <- nrow(x) > 100

# GOOD: names say what things are
cases <- read.csv("cases.csv")
positive_cases <- cases[cases$viral_load > 0, ]
has_many_positives <- nrow(positive_cases) > 100
```

```python
# GOOD
cases = pd.read_csv("cases.csv")
positive_cases = cases[cases["viral_load"] > 0]
has_many_positives = len(positive_cases) > 100
```

```julia
# GOOD
cases = CSV.read("cases.csv", DataFrame)
positive_cases = filter(row -> row.viral_load > 0, cases)
has_many_positives = nrow(positive_cases) > 100
```

## Write small functions that do one thing

If you can't describe a function without saying "and", it probably wants to be two functions. Small, single-purpose functions are easy to name, test, and reuse.

```r
# BAD: one function loads, cleans, models, and plots
analyze <- function(path) {
  d <- read.csv(path)
  d <- d[!is.na(d$y), ]
  d$logy <- log(d$y)
  m <- lm(logy ~ x, data = d)
  plot(d$x, d$logy); abline(m)
  return(m)
}

# GOOD: each step is its own verb
load_data  <- function(path) read.csv(path)
clean_data <- function(d) transform(d[!is.na(d$y), ], logy = log(y))
fit_model  <- function(d) lm(logy ~ x, data = d)
```

## Don't Repeat Yourself (DRY)

Copy-pasted code drifts: you fix a bug in one copy and forget the other three. When you see the same lines twice, extract a function.

```python
# BAD: same transformation, three times, easy to get out of sync
train_z = (train - train.mean()) / train.std()
valid_z = (valid - train.mean()) / train.std()
test_z  = (test  - train.mean()) / train.std()

# GOOD: one definition, one place to fix
def standardize(x, center, scale):
    return (x - center) / scale

mu, sigma = train.mean(), train.std()
train_z, valid_z, test_z = (standardize(s, mu, sigma) for s in (train, valid, test))
```

## Avoid magic numbers

A bare `0.05` or `1000` buried in code is a mystery. Give it a name.

```r
# BAD
if (p_value < 0.05) reject <- TRUE
draws <- rnorm(10000)

# GOOD
significance_level <- 0.05
n_draws <- 10000L
reject <- p_value < significance_level
draws  <- rnorm(n_draws)
```

## Fail loudly

A wrong answer is worse than an error. Check your assumptions and stop early with a clear message rather than silently producing nonsense.

```r
# GOOD: validate inputs up front
estimate_rate <- function(counts, exposure) {
  stopifnot(
    length(counts) == length(exposure),
    all(exposure > 0)
  )
  sum(counts) / sum(exposure)
}
```

```python
# GOOD
def estimate_rate(counts, exposure):
    if len(counts) != len(exposure):
        raise ValueError("counts and exposure must be the same length")
    if any(e <= 0 for e in exposure):
        raise ValueError("exposure must be positive")
    return sum(counts) / sum(exposure)
```

```julia
# GOOD
function estimate_rate(counts, exposure)
    @assert length(counts) == length(exposure) "lengths must match"
    @assert all(>(0), exposure) "exposure must be positive"
    sum(counts) / sum(exposure)
end
```

## Comment the *why*, and format consistently

- Comment intent and gotchas, not the obvious (`i = i + 1  # add one` helps no one).
- Pick a style and let a formatter enforce it: `styler`/`lintr` (R), `black`/`ruff` (Python), `JuliaFormatter.jl` (Julia). Consistency removes noise from [diffs](version-control-git.md) and lets reviewers focus on substance.

```r
# BAD: explains the code we can already read
x <- x + 1  # increment x

# GOOD: explains why
# Offset by 1 because the assay reports 0-based well indices.
well_index <- well_index + 1
```

## A messy snippet, refactored

```r
# BAD: unnamed steps, magic numbers, repetition, no checks
f <- function(a) {
  b <- a[a[,2] > 0.05,]
  m1 <- mean(b[,1]); m2 <- mean(b[b[,3]==1,1]); m3 <- mean(b[b[,3]==0,1])
  c(m1, m2, m3)
}
```

```r
# GOOD: named, checked, DRY
group_mean <- function(df, group_value) {
  mean(df$value[df$group == group_value])
}

summarize_by_group <- function(df, min_weight = 0.05) {
  stopifnot(all(c("value", "weight", "group") %in% names(df)))
  kept <- df[df$weight > min_weight, ]
  c(
    overall = mean(kept$value),
    treated = group_mean(kept, 1),
    control = group_mean(kept, 0)
  )
}
```

## Related

- [Project Workflow](project-workflow.md)
- [Reproducibility](reproducibility.md)
- [Debugging and Troubleshooting](debugging-and-troubleshooting.md)
- [Version Control with Git](version-control-git.md)
- [Programming & Computing](../programming.md)
