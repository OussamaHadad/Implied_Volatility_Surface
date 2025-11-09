import pandas as pd
import numpy as np
from src.solvers import *

def compute_data_iv(data: pd.DataFrame, S: float, r: float, q: float, solver = iv_brent, verbose: bool = False):
    data["impliedVolatility"] = np.nan

    for i, row in data.iterrows():
        iv = solver(row['midPrice'], S, row['strike'], r, q, row['timeToMaturity'])

        data.loc[i, 'impliedVolatility'] = iv
        if verbose:
            print(f"{i + 1}/{len(data)}: IV = {iv:.4f}")

    data.dropna(subset=["impliedVolatility"], inplace=True)
    return data