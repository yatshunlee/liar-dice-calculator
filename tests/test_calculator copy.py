import pytest
from src.liar_dice_calculator.core import LiarDiceCalculator

def test_binom():
    calculator = LiarDiceCalculator()
    assert calculator._binom(5, 2, 0.5) == pytest.approx(0.3125, rel=1e-2)
    assert calculator._binom(5, 0, 0.5) == pytest.approx(0.03125, rel=1e-2)
    assert calculator._binom(5, 5, 0.5) == pytest.approx(0.03125, rel=1e-2)
    with pytest.raises(ValueError):
        calculator._binom(-1, 2, 0.5)
    with pytest.raises(ValueError):
        calculator._binom(5, -1, 0.5)
    with pytest.raises(ValueError):
        calculator._binom(5, 6, 0.5)
    with pytest.raises(ValueError):
        calculator._binom(5, 2, -1)
    with pytest.raises(ValueError):
        calculator._binom(5, 2, 2)

def test_single_player_pmf():
    calculator = LiarDiceCalculator()
    dist = calculator._single_player_pmf(0.5)
    assert dist[0] == pytest.approx(0.03125, rel=1e-2)
    assert dist[1] == pytest.approx(0.15625, rel=1e-2)
    assert dist[2] == pytest.approx(0.3125, rel=1e-2)
    assert dist[3] == pytest.approx(0.3125, rel=1e-2)
    assert dist[4] == pytest.approx(0.15625, rel=1e-2)
    assert dist[5] == 0.0
    assert dist[6] == pytest.approx(0.03125, rel=1e-2)
    with pytest.raises(ValueError):
        calculator._single_player_pmf(-1)

def test_single_player_cond_pmf():
    calculator = LiarDiceCalculator()
    dist = calculator._single_player_pmf(0.5)
    cond_dist = calculator._single_player_cond_pmf(dist, 2)
    assert cond_dist[0] == 0.0
    assert cond_dist[1] == 0.0
    assert cond_dist[2] == pytest.approx(0.25, rel=1e-2)
    assert cond_dist[3] == pytest.approx(0.25, rel=1e-2)
    assert cond_dist[4] == pytest.approx(0.25, rel=1e-2)
    assert cond_dist[5] == 0.0
    assert cond_dist[6] == pytest.approx(0.25, rel=1e-2)
    with pytest.raises(ValueError):
        calculator._single_player_cond_pmf(dist, -1)
    with pytest.raises(ValueError):
        calculator._single_player_cond_pmf(dist, 7)
    with pytest.raises(ValueError):
        calculator._single_player_cond_pmf({}, 1)

def test_predict():
    calculator = LiarDiceCalculator()
    n_players = 2
    is_wild = True
    player_dice = {1: 2, 2: 1, 3: 1}
    degree_of_belief = 0

    hmap = calculator.predict(n_players, is_wild, player_dice, degree_of_belief)
    assert len(hmap) == 5
    assert len(hmap[0]) == 13
    