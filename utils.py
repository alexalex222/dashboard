import pandas as pd
import numpy as np
from empyrical import (
    sharpe_ratio,
    calmar_ratio,
    sortino_ratio,
    max_drawdown,
    downside_risk,
    annual_return,
    annual_volatility,
    # cum_returns,
)


def cumulative_return(srs: pd.Series) -> pd.Series:
    daily_return = srs.pct_change()
    cum_return = (1 + daily_return).cumprod() - 1
    cum_return = cum_return.fillna(0)

    return cum_return


def calc_performance_metrics(
        captured_returns,
        ):
    if len(captured_returns.shape) == 1:
        n_assets = 1
        captured_returns = captured_returns.reshape(-1, 1)
    else:
        _, n_assets = captured_returns.shape
    performance_results = np.zeros((7, n_assets))
    for i in range(n_assets):
        performance_results[0, i] = annual_return(captured_returns[:, i])
        performance_results[1, i] = annual_volatility(captured_returns[:, i])
        performance_results[2, i] = sharpe_ratio(captured_returns[:, i])
        performance_results[3, i] = downside_risk(captured_returns[:, i])
        performance_results[4, i] = sortino_ratio(captured_returns[:, i])
        performance_results[5, i] = -max_drawdown(captured_returns[:, i])
        performance_results[6, i] = calmar_ratio(captured_returns[:, i])

    return performance_results
