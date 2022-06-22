import pandas as pd


def cumulative_return(srs: pd.Series) -> pd.Series:
    daily_return = srs.pct_change()
    cum_return = (1 + daily_return).cumprod() - 1
    cum_return = cum_return.fillna(0)

    return cum_return
