---
title: "Manipulating Data Frames"
---

# Manipulating Data Frames

Most of applied analysis is data wrangling — reshaping, filtering, and summarizing tables before any model is fit.
The same handful of verbs shows up in every ecosystem, so this page is a Rosetta stone across **R** ([dplyr](https://dplyr.tidyverse.org) and [data.table](https://rdatatable.gitlab.io/data.table/)), **Python** ([pandas](https://pandas.pydata.org) and [Polars](https://pola.rs)), and **Julia** ([DataFrames.jl](https://dataframes.juliadata.org)).

## The core verbs

Almost every pipeline is built from six operations.

| Operation | dplyr (R) | data.table (R) | pandas (Python) | Polars (Python) | DataFrames.jl (Julia) |
|-----------|-----------|----------------|-----------------|-----------------|-----------------------|
| pick columns | `select(df, a, b)` | `dt[, .(a, b)]` | `df[["a", "b"]]` | `df.select("a", "b")` | `select(df, :a, :b)` |
| filter rows | `filter(df, x > 0)` | `dt[x > 0]` | `df[df.x > 0]` | `df.filter(pl.col("x") > 0)` | `subset(df, :x => ByRow(>(0)))` |
| new column | `mutate(df, y = 2*x)` | `dt[, y := 2*x]` | `df.assign(y=2*df.x)` | `df.with_columns(y=2*pl.col("x"))` | `transform(df, :x => ByRow(x -> 2x) => :y)` |
| sort | `arrange(df, x)` | `dt[order(x)]` | `df.sort_values("x")` | `df.sort("x")` | `sort(df, :x)` |
| group + summarize | `group_by(df, g) |> summarise(m = mean(x))` | `dt[, .(m = mean(x)), by = g]` | `df.groupby("g").agg(m=("x","mean"))` | `df.group_by("g").agg(m=pl.col("x").mean())` | `combine(groupby(df, :g), :x => mean => :m)` |
| join | `left_join(a, b, by = "id")` | `b[a, on = "id"]` | `a.merge(b, on="id", how="left")` | `a.join(b, on="id", how="left")` | `leftjoin(a, b, on = :id)` |

## A worked pipeline

The same task in each dialect: from weekly case counts, keep the first two weeks, add a per-100k **rate**, then summarize total cases and mean rate **by region**.

### R — dplyr

```r
library(dplyr)
df <- tibble(
  region = c("A", "A", "A", "B", "B", "B"),
  week   = c(1, 2, 3, 1, 2, 3),
  cases  = c(10, 15, 9, 3, 7, 12),
  pop    = c(1e5, 1e5, 1e5, 5e4, 5e4, 5e4)
)
df |>
  filter(week <= 2) |>
  mutate(rate = cases / pop * 1e5) |>
  group_by(region) |>
  summarise(total = sum(cases), mean_rate = mean(rate))
```

### R — data.table

```r
library(data.table)
dt <- data.table(
  region = c("A", "A", "A", "B", "B", "B"),
  week   = c(1, 2, 3, 1, 2, 3),
  cases  = c(10, 15, 9, 3, 7, 12),
  pop    = c(1e5, 1e5, 1e5, 5e4, 5e4, 5e4)
)
dt[week <= 2
   ][, rate := cases / pop * 1e5
   ][, .(total = sum(cases), mean_rate = mean(rate)), by = region]
```

### Python — pandas

```python
import pandas as pd
df = pd.DataFrame({
    "region": ["A", "A", "A", "B", "B", "B"],
    "week":   [1, 2, 3, 1, 2, 3],
    "cases":  [10, 15, 9, 3, 7, 12],
    "pop":    [1e5, 1e5, 1e5, 5e4, 5e4, 5e4],
})
out = (
    df[df["week"] <= 2]
    .assign(rate=lambda d: d["cases"] / d["pop"] * 1e5)
    .groupby("region", as_index=False)
    .agg(total=("cases", "sum"), mean_rate=("rate", "mean"))
)
print(out)
```

<!-- python-output:auto -->
```text
  region  total  mean_rate
0      A     25       12.5
1      B     10       10.0
```
<!-- /python-output:auto -->

### Python — Polars

Polars uses an **expression** API (`pl.col(...)`), reads as a clean pipeline, and has a lazy mode (`pl.scan_csv(...).collect()`) that optimizes the whole query — often much faster on large data.

```python
import polars as pl
df = pl.DataFrame({
    "region": ["A", "A", "A", "B", "B", "B"],
    "week":   [1, 2, 3, 1, 2, 3],
    "cases":  [10, 15, 9, 3, 7, 12],
    "pop":    [1e5, 1e5, 1e5, 5e4, 5e4, 5e4],
})
out = (
    df.filter(pl.col("week") <= 2)
      .with_columns(rate=pl.col("cases") / pl.col("pop") * 1e5)
      .group_by("region")
      .agg(total=pl.col("cases").sum(), mean_rate=pl.col("rate").mean())
      .sort("region")
)
print(out)
```

<!-- python-output:auto -->
```text
shape: (2, 3)
┌────────┬───────┬───────────┐
│ region ┆ total ┆ mean_rate │
│ ---    ┆ ---   ┆ ---       │
│ str    ┆ i64   ┆ f64       │
╞════════╪═══════╪═══════════╡
│ A      ┆ 25    ┆ 12.5      │
│ B      ┆ 10    ┆ 10.0      │
└────────┴───────┴───────────┘
```
<!-- /python-output:auto -->

### Julia — DataFrames.jl

```julia
using DataFrames, Statistics
df = DataFrame(region = ["A","A","A","B","B","B"],
               week   = [1, 2, 3, 1, 2, 3],
               cases  = [10, 15, 9, 3, 7, 12],
               pop    = [1e5, 1e5, 1e5, 5e4, 5e4, 5e4])
sub = subset(df, :week => ByRow(<=(2)))
transform!(sub, [:cases, :pop] => ByRow((c, p) -> c / p * 1e5) => :rate)
combine(groupby(sub, :region),
        :cases => sum => :total,
        :rate  => mean => :mean_rate)
```

`DataFramesMeta.jl` adds a `@chain`/`@rsubset`/`@transform` layer that reads much like dplyr if you prefer piped, macro-based syntax.

## Reshaping: long ↔ wide

Tidy analysis usually wants **long** data (one row per observation); reporting often wants **wide**.

- dplyr: `pivot_longer()` / `pivot_wider()`
- data.table: `melt()` / `dcast()`
- pandas: `df.melt()` / `df.pivot(...)` (or `pivot_table`)
- Polars: `df.melt()` / `df.pivot(...)`
- DataFrames.jl: `stack()` / `unstack()`

## Which should you use?

- **dplyr** — the most readable; the default for interactive analysis and teaching.
- **data.table** — terse and extremely fast, with in-place (`:=`) updates; excellent for large data in R.
- **pandas** — ubiquitous and well-documented; the safe default in Python.
- **Polars** — a modern, multi-threaded, expression-based alternative to pandas with a lazy query optimizer; noticeably faster and more memory-efficient on large tables.
- **DataFrames.jl** — fast and composable in Julia, pairing naturally with the modeling code in these pages.

## Why it matters

Clean, correct data manipulation is the foundation every analysis on this site stands on — a summary, a [regression](linear-regression.md), or a fitted [epidemic model](model-calibration.md) is only as good as the table feeding it.
Knowing the same verbs across languages lets you read collaborators' code and pick the right tool for the dataset in front of you.

## Related

- [Good Programming Practices](../programming/good-programming-practices.md)
- [Reproducibility](../programming/reproducibility.md)
- [Project Workflow](../programming/project-workflow.md)
- [Measures of Center](measures-of-center.md)
- [Linear Regression](linear-regression.md)
- [Quantitative Methods](../math.md)
