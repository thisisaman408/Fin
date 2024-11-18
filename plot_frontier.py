import matplotlib.pyplot as plt
from MAD_optimizer import mad_portfolio_optimization, display_portfolio_results
import numpy as np


def plot_frontier(data_df, min_return, max_return, step=0.0005):
    target_vals = np.arange(min_return, max_return, step)
    risks = []
    returns = []

    for target in target_vals:
        output = mad_portfolio_optimization(data_df, target)
        display_portfolio_results(output)
        if output['status'] == 'Optimal':
            risks.append(output['portfolio_mad'])
            returns.append(output['portfolio_return'])
        else:
            risks.append(np.nan)
            returns.append(np.nan)

    plt.figure(figsize=(10, 6))
    plt.plot(returns, risks, label='Frontier Curve', color='b')
    plt.xlabel('Return')
    plt.ylabel('Risk (MAD)')
    plt.title('Efficient Frontier (MAD Optimization)')
    plt.grid(True)
    plt.show()


