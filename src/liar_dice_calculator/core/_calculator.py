from math import comb
from typing import List, Dict

class LiarDiceCalculator:
    def __init__(self):
        self.p_wild = 1 / 3
        self.p_not_wild = 1 / 6
        self.n_dice = 5
        self.total_faces = 6

        self.pmf = {
            'wild': self._single_player_pmf(self.p_wild),
            'not_wild': self._single_player_pmf(self.p_not_wild)
        }
    
    def _binom(self, n: int, k: int, p: float) -> float:
        """
        assume X ~ bin(n, p), calculate P(X = k) and return
        """
        if n < 0 or k < 0 or n < k:
            raise ValueError("n, k must be >= 0 and n >= k")
        if p < 0 or p > 1:
            raise ValueError("p must be in [0, 1]")
        return comb(n, k) * p ** k * (1 - p) ** (n - k)
    
    def _single_player_pmf(self, p: float) -> Dict[int, float]:
        """
        return the distribution of Liar Dice's count,
        where it is a variant of binomial
        """
        if p < 0 or p > 1:
            raise ValueError("p must be in [0, 1]")
        
        dist = {}

        for i in range(self.n_dice):
            dist[i] = self._binom(self.n_dice, i, p)

        dist[5] = 0.0
        dist[6] = self._binom(self.n_dice, self.n_dice, p)

        return dist
    
    def _single_player_cond_pmf(
        self, 
        dist: Dict[int, float], 
        at_least: int
        ) -> Dict[int, float]:

        """
        We believe that opponent has at least a count,
        where a is a positive number => k + a > a.

        Then,
        - Bayes: P(X >= k + a | X >= a) = P(X >= k + a) / P(X >= a)
        - given that: P(X < a) = 0
        """
        if at_least > 6 or at_least < 0:
            raise ValueError("at_least must be in [0, 6]")
        
        if not isinstance(dist, dict) or len(dist) == 0:
            raise ValueError("dist must be a non-empty dict")

        cond_dist = {
            i: 0.0 
            for i in range(at_least)
        }

        p_at_least = 1.0
        for i in range(at_least):
            p_at_least -= dist[i]

        for i in range(at_least, self.n_dice + 2):
            cond_dist[i] = dist[i] / p_at_least
        
        return cond_dist
        
    def _conv(
        self, 
        n_players: int, 
        dist: Dict[int, float],
        conv_dist: Dict[int, float] = {0: 1.0}
        ) -> Dict[int, float]:
        """
        calculate convolution of probability distribution
        Init D_0(s) = 1.0 for s <= 0
        for i in {1, ..., n}
            D_i(s) = summation of k (D_i-1(s-k) * P(X=k))
        """
        if n_players < 0:
            raise ValueError('n_players must be >= 0')

        for _ in range(n_players):
            tmp_dist = {}
            for s, pr_s in conv_dist.items():
                for k, pr_k in dist.items():
                    tmp_dist[s+k] = (
                        tmp_dist.get(s + k, 0) + pr_s * pr_k
                    )
            conv_dist = tmp_dist

        return conv_dist

    def predict(
        self, 
        n_players: int, 
        is_wild: bool,
        player_dice: Dict[int, int],
        degree_of_belief: int = 0
        ) -> List[List[float]]:
        """
        get prediction heatmap of each possible outcome
        value of each cell in the heatmap = probability >= some count
        """
        if is_wild:
            single_player_dist = self.pmf['wild']
            n_faces = self.total_faces - 1
            # adding the wild one into each face value
            player_dice = {
                i: player_dice.get(1, 0) + player_dice.get(i, 0) 
                for i in range(2, self.total_faces + 1)
            }
        else:
            single_player_dist = self.pmf['not_wild']
            n_faces = self.total_faces

        if degree_of_belief == 0:
            # n - 1 as exclude player themselves (too left wing using they/them)
            dist = self._conv(n_players - 1, single_player_dist)
            
        elif degree_of_belief <= 2:
            opponent_dist = self._single_player_cond_pmf(
                single_player_dist, 
                degree_of_belief
            )
            dist = self._conv(n_players - 2, single_player_dist, opponent_dist)

        else:
            raise ValueError("degree_of_belief must be 0, 1, or 2")

        # if 5 -> 6 for the count
        player_dice = {
            i: player_dice.get(i) if player_dice.get(i) < 5 else 6
            for i in player_dice
        }
        
        # initialize a heatmap
        hmap = [
            [0.0] * ((self.n_dice + 1) * n_players + 1) 
            for _ in range(n_faces)
        ]

        for i in range(n_faces):
            if is_wild:
                cnt = player_dice.get(i + 2, 0)
            else:
                cnt = player_dice.get(i + 1, 0)

            for j in range(cnt + 1):
                # deterministic based on what we have in our hand
                hmap[i][j] = 1.0
            for j in range(cnt + 1, len(hmap[i])):
                # P(X >= a) = 1 - P(X = 0) - ... - P(X = a - 1)
                hmap[i][j] = max(0.0, hmap[i][j-1] - dist.get(j - cnt - 1, 0))
        
        return hmap

