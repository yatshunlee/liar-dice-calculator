# Liar-Dice-Calculator

## Basic Usage

The following example demonstrates how to use the class `LiarDiceCalculator` to generate a predicion heatmap

```python
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

cummulative_probability_heatmap = calculator.predict(
    n_players,
    is_wild,
    player_dice,
    degree_of_belief
)
```
