import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure
import matplotlib.pyplot as plt 
from typing import List

def _generate_prediction_heatmap(
    heatmap: List[List[float]]
    ) -> pd.DataFrame:

    if not isinstance(heatmap, list) or len(heatmap) == 0:
        raise Exception('Heatmap must be in 2D')

    m = len(heatmap)
    if m == 5:
        idx = ["⚀⚁⚂⚃⚄⚅"[i] for i in range(1, 6)] # range(2, 7)
    elif m == 6:
        idx = ["⚀⚁⚂⚃⚄⚅"[i] for i in range(0, 6)] # range(1, 7)
    else:
        raise Exception('Size error')
        
    heatmap = pd.DataFrame(heatmap)
    heatmap.index = idx
    return heatmap.T[::-1]

def _prunning(heatmap: pd.DataFrame, threshold: float=0.01):
    """
    Prune the heatmap to remove values below the threshold.
    Only the rows that have values above the threshold will be kept.
    """
    n_players = (heatmap.shape[0] - 1) // 6
    heatmap = heatmap[heatmap > threshold]
    heatmap = heatmap.dropna(axis=0, how='all')
    heatmap.fillna(0, inplace=True)
    return heatmap.iloc[:-n_players, :]

def plot_heatmap(
    heatmap: List[List[float]]
    ):

    heatmap = _generate_prediction_heatmap(heatmap)
    heatmap = _prunning(heatmap)

    n = heatmap.shape[0] // 4 * 3
    fig, ax = plt.subplots(1, 1, figsize=(8, n))
    ax = sns.heatmap(heatmap, annot=True, fmt='.4f', linewidth=.5, ax=ax)
    ax.set_xlabel('Faces')
    ax.set_ylabel('Bids')
    ax.set_title('Prediction Heatmap (Probability of #Face >= Bids)')
    return (fig, ax)