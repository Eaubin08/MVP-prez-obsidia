import pandas as pd
import numpy as np

def load_prices_csv(path: str):
    df = pd.read_csv(path)
    # expects at least a 'close' column; if not present, uses last column
    if "close" not in df.columns:
        close = df.iloc[:, -1].astype(float).values
    else:
        close = df["close"].astype(float).values
    returns = np.diff(close) / close[:-1]
    return close, returns
