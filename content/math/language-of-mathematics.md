---
title: "The Language of Mathematics"
---

# The Language of Mathematics

Welcome — if formulas make you nervous, start here.
Mathematics is not a wall of symbols to memorize; it is a compact language for saying precise things about how quantities relate and change.
This page is a friendly glossary of its basic vocabulary, so the rest of the site reads smoothly.

Think of it the way you first met a new scientific field: before the interesting results, you learned the words.
Here the words are number systems, a few famous constants, and the names for the objects we manipulate — variables, functions, and equations.
Once these feel familiar, the equations elsewhere on the site stop looking like code and start reading like sentences.

## Number systems

Numbers come in nested families, each larger than the last, and each family has a standard "blackboard bold" symbol.
Reading these symbols aloud helps: $\in$ means "is an element of" (as in "$3 \in \mathbb{N}$", three is a natural number), and $\subset$ means "is a subset of" (one whole family sits inside another).

- Natural numbers $\mathbb{N} = \{0, 1, 2, \dots\}$ — the counting numbers.
You meet them whenever you count whole things: a population size, a number of cases, a litter of pups.
- Integers $\mathbb{Z}$ — the naturals together with their negatives, $\{\dots, -2, -1, 0, 1, 2, \dots\}$.
You need these once counts can go down as well as up: the change in a population from one year to the next can be $-40$.
- Rational numbers $\mathbb{Q}$ — all ratios of integers, like $\tfrac{3}{4}$ or $\tfrac{17}{5}$.
You meet them as proportions and rates: a prevalence of $0.12$, three deaths per thousand.
- Real numbers $\mathbb{R}$ — the full continuous number line, filling in the gaps between the rationals with irrational numbers such as $\sqrt{2}$, $\pi$, and $e$.
You meet them in measurements that vary continuously: a concentration, a body temperature, an elapsed time.
- Complex numbers $\mathbb{C}$ — numbers with an "imaginary" part built on the imaginary unit $i = \sqrt{-1}$, so that $i^2 = -1$.
A complex number looks like $a + bi$.

These families nest neatly inside one another:

\[
\mathbb{N} \subset \mathbb{Z} \subset \mathbb{Q} \subset \mathbb{R} \subset \mathbb{C}.
\]

Read left to right, this says: every natural number is an integer, every integer is rational, every rational is real, and every real is complex.
So when you write $N \in \mathbb{N}$ for a population count, you are also entitled to treat $N$ as a real number when you do calculus with it.

## Why biologists meet imaginary numbers

Complex numbers can feel like a purely abstract detour, but they show up the moment a biological system oscillates — and that is often.

![A complex eigenvalue a + bi and the damped oscillation e^{at} cos(bt) it produces — the imaginary part sets the frequency of population cycles.](../assets/figures/complex-oscillation.svg)

Here is the payoff.
When you study the stability of a dynamical system, you linearize it near an equilibrium and look at the [eigenvalues](eigenvalues-and-eigenvectors.md) of its [Jacobian](jacobians.md) matrix.
Those eigenvalues can come out complex, $\lambda = a + bi$, and the behavior near the equilibrium grows like $e^{\lambda t}$.
The real part of $e^{\lambda t}$ works out to $e^{at}\cos(bt)$, which is an oscillation wrapped in an exponential envelope.
The real part $a$ sets growth or decay: if $a < 0$ the wiggles die away, if $a > 0$ they blow up.
The imaginary part $b$ sets the oscillation frequency, giving a cycle with period $2\pi / b$.
This is precisely the math behind [predator–prey cycles](predator-prey.md) and behind damped epidemic waves that ripple and settle.
So the imaginary unit is not a curiosity — it is the algebra of anything that cycles.

## Constants worth knowing

A handful of numbers appear so often they earned their own names.

- $\pi \approx 3.14159$ — the ratio of a circle's circumference to its diameter, and the constant that shows up wherever there are angles, rotations, or oscillations (note the $2\pi / b$ above).
- Euler's number $e \approx 2.71828$ — the base of natural growth and decay, and the anchor of the [exponential and logarithm](exponentials-and-logarithms.md) family that describes unchecked population growth, radioactive decay, and drug clearance.
- The imaginary unit $i = \sqrt{-1}$ — the building block of the complex numbers described above.

## The words for the objects

Once the numbers are in place, we need names for the things we do with them.

### Variables, parameters, and constants

A **variable** is a quantity that changes and that we are solving for or tracking.
A **parameter** is a quantity we hold fixed for a given scenario but might tune between scenarios.
A **constant** is a fixed number that never changes, like $\pi$.
For example, in the growth equation $\frac{dN}{dt} = rN$, the population size $N$ is a variable (it changes over time), while the per-capita growth rate $r$ is a parameter (fixed for a given species and setting).

### Functions

A **function** is a rule that takes an input and returns exactly one output.
The input is called the **argument**; the set of allowed inputs is the **domain**; the set of possible outputs is the **range**.
We write $f(x)$ to mean "the function $f$ evaluated at the argument $x$".
See [functions and graphs](functions-and-graphs.md) for the visual picture.

### Equations, identities, and inequalities

An **equation** asserts that two expressions are equal for particular values, like $2x = 6$ (true only when $x = 3$).
An **identity** is an equality that holds for all values, written with $\equiv$, as in $\sin^2\theta + \cos^2\theta \equiv 1$.
An **inequality** compares sizes using $<$, $\le$, $>$, $\ge$, or $\neq$ ("not equal to"), as in $N \ge 0$ for a population count.

### Three symbols that look alike

These are easy to confuse but mean different things.

- $\approx$ means "approximately equal to", as in $e \approx 2.71828$.
- $\propto$ means "proportional to": $y \propto x$ says $y = cx$ for some constant $c$ you may not care to name.
- $\sim$ means "is distributed as", relating a [random variable](random-variables.md) to its probability distribution, as in $X \sim \text{Normal}(\mu, \sigma^2)$.

For the fuller symbol table — sums, products, set operations, and more — see [mathematical notation](mathematical-notation.md).

## How to read an equation

An equation is a sentence; give yourself permission to read it slowly.
Go left to right, name each symbol out loud, decide what varies and what is held fixed, and sanity-check the units on both sides.

Take the logistic growth law:

\[
\frac{dN}{dt} = rN\left(1 - \frac{N}{K}\right).
\]

Read it piece by piece.
The left side $\frac{dN}{dt}$ is the [derivative](derivatives.md) of population size with respect to time — the instantaneous rate of change of $N$, in individuals per unit time.
On the right, $N$ is the variable, while $r$ (growth rate) and $K$ (carrying capacity) are parameters held fixed.
The factor $rN$ is exponential growth, and the bracket $\left(1 - \frac{N}{K}\right)$ is a brake: it is near $1$ when $N$ is small (fast growth) and shrinks to $0$ as $N$ approaches $K$ (growth stalls).
So in words the equation says: "the population grows in proportion to its size, but that growth is throttled as the population fills up its habitat."
The same reading habit unpacks the compartment models on the [SIR](sir.md) and [predator–prey](predator-prey.md) pages.

## Where to learn more

These are genuinely useful starting points for biologists and public-health learners.
Use them the same way: watch or skim first for the intuition, then go back and work a few examples by hand — the understanding sticks only once your own pencil moves.

- Otto & Day, *A Biologist's Guide to Mathematical Modeling in Ecology and Evolution* (Princeton) — the ideal on-ramp written for biologists: [press.princeton.edu](https://press.princeton.edu/books/paperback/9780691123448/a-biologists-guide-to-mathematical-modeling-in-ecology-and-evolution).
- Strogatz, *Nonlinear Dynamics and Chaos* — a beloved, intuition-first tour of oscillations, stability, and bifurcations: [stevenstrogatz.com](https://www.stevenstrogatz.com/books/nonlinear-dynamics-and-chaos).
- 3Blue1Brown, *Essence of Calculus* and *Essence of Linear Algebra* — short animated videos that build visual intuition before symbols: [3blue1brown.com](https://www.3blue1brown.com/).
- Khan Academy — free, self-paced courses in algebra, calculus, and statistics with practice problems: [khanacademy.org/math](https://www.khanacademy.org/math).
- Project Jupyter — executable notebooks so you can try models and plots yourself: [jupyter.org](https://jupyter.org).

## Related

- [Mathematical Notation](mathematical-notation.md)
- [Functions and Graphs](functions-and-graphs.md)
- [Exponentials and Logarithms](exponentials-and-logarithms.md)
- [Eigenvalues and Eigenvectors](eigenvalues-and-eigenvectors.md)
- [Quantitative Methods](../math.md)
