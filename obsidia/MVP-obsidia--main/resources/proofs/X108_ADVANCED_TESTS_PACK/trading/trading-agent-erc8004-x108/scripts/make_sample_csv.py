import argparse
import numpy as np
import pandas as pd

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, default=600)
    args = ap.parse_args()

    # simple geometric random walk
    rng = np.random.default_rng(108)
    rets = rng.normal(0.0005, 0.01, size=args.n)
    price = 100 * np.cumprod(1 + rets)
    df = pd.DataFrame({"close": price})
    df.to_csv(args.out, index=False)
    print("wrote", args.out)

if __name__ == "__main__":
    main()
