# Liar-Dice-Calculator

## Installation

```bash
git clone https://github.com/yourusername/liar-dice-calculator.git
cd liar-dice-calculator
poetry install
```

## Basic Usage

To self-host the web application: 

```bash
cd liar-dice-calculator
streamlit run src/liar-dice-calculator/frontend/app.py
```

The following example demonstrates how to use the class `LiarDiceCalculator` to generate a predicion heatmap

```python
from typing import List
from liar_dice_calculator.core import LiarDiceCalculator

calculator = LiarDiceCalculator()

# n_players (including you)
n_players = 5

# wild 1
is_wild = True

# what do you have at your hand
player_dice = {
    1: 2,
    2: 1,
    5: 2
}

# do you believe the call of others
degree_of_belief = 0

cummulative_probability_heatmap: List[List[float]] = calculator.predict(
    n_players,
    is_wild,
    player_dice,
    degree_of_belief
)
```
## How it works
n dices that have the targeted face value(s), including wild 1 let's say, follows a binomial distribution:

- Each die roll is an independent trial.
- Each die has six faces, so the probability of success (rolling the target face and wild one) is $$ p=\frac{2}{6} $$.
- The total number of unknown dice is $$ n=5 $$.
- The random variable $$ X $$, representing the count of dice showing the target face, counts the number of successes in $$ n $$ independent Bernoulli trials.
- If have 5 same faces (incl wild 1), the count will be added 1, i.e. 6.

Thus, the probability of exactly $$ q $$ dice showing the target face is given by the binomial probability mass function:

$$
P(X = k) = \binom{5}{k} \left(\frac{2}{6}\right)^k \left(\frac{4}{6}\right)^{5-k} for k >= 0 and k <= 4
P(X = 6) = \left(\frac{2}{6}\right)^5
$$

where $$ \binom{n}{q} $$ is the binomial coefficient (number of ways to choose $$ q $$ dice from $$ n $$).

---

## The Effect of Wild 1's and Convolution of Probability Distributions

The effect of adding 1 if the real count = 5 makes the binomial distribution not binomial.

The total count distribution among all players is then the **convolution** of each player dice's distribution. Convolution is the mathematical operation used to find the probability distribution of the sum of two independent random variables.

Formally, if $$ X \sim \text{Binomial}(n, \frac{2}{6}) $$ counts the target face and $$ Y \sim \text{Binomial}(n, \frac{2}{6}) $$ counts the wild ones, then the total count $$ Z = X + Y $$ has probability:

$$
P(Z = k) = \sum_{i=0}^k P(X = i) \cdot P(Y = k - i)
$$

This convolution sums over all ways to partition the total count $$ k $$ between the target face and the wild ones