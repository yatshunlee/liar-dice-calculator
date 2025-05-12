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
