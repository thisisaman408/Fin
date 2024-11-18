from pulp import *
import pandas as pd

def preprocess_data(data_df):
    cleaned_data = data_df.dropna()
    return_data = cleaned_data.drop(['Date', 'Market Portfolio.1'], axis=1)
    return return_data

def optimize_portfolio(data_df, desired_return):
    returns_data = preprocess_data(data_df)
    asset_count = len(returns_data.columns)
    period_count = len(returns_data)
    avg_returns = returns_data.mean()

    print("Asset count:", asset_count)
    print("Period count:", period_count)
    print("Average returns range:", avg_returns.min(), "to", avg_returns.max())

    problem = LpProblem("Portfolio_Optimization", LpMinimize)

    weight_variables = LpVariable.dicts("weights", returns_data.columns, lowBound=0, upBound=1)
    deviation_variables = LpVariable.dicts("deviation", range(period_count), lowBound=0)

    problem += lpSum(deviation_variables[i] for i in range(period_count)) / period_count

    problem += lpSum(weight_variables[asset] for asset in returns_data.columns) == 1
    problem += lpSum(weight_variables[asset] * avg_returns[asset] for asset in returns_data.columns) >= desired_return

    for idx in range(period_count):
        current_returns = returns_data.iloc[idx]

        problem += lpSum(weight_variables[asset] * current_returns[asset] for asset in returns_data.columns) - \
                    lpSum(weight_variables[asset] * avg_returns[asset] for asset in returns_data.columns) <= deviation_variables[idx]

        problem += -lpSum(weight_variables[asset] * current_returns[asset] for asset in returns_data.columns) + \
                    lpSum(weight_variables[asset] * avg_returns[asset] for asset in returns_data.columns) <= deviation_variables[idx]

    problem.solve(PULP_CBC_CMD(msg=False))

    if LpStatus[problem.status] == 'Optimal':
        final_weights = {asset: value(weight_variables[asset]) for asset in returns_data.columns}

        portfolio_expected_return = sum(final_weights[asset] * avg_returns[asset] for asset in returns_data.columns)
        portfolio_deviation = value(problem.objective)

        return {
            'weights': final_weights,
            'expected_return': portfolio_expected_return,
            'risk_measure': portfolio_deviation,
            'status': LpStatus[problem.status]
        }
    else:
        return {
            'status': LpStatus[problem.status],
            'message': 'Optimization did not succeed'
        }

def show_results(result):
    print("\nOptimization Results:")
    print("-" * 50)
    print(f"Status: {result['status']}")

    if result['status'] == 'Optimal':
        print(f"\nPortfolio Metrics:")
        print(f"Expected Return: {result['expected_return']:.4f}")
        print(f"Risk Measure: {result['risk_measure']:.4f}")

        print("\nOptimal Portfolio Weights:")
        weight_df = pd.DataFrame.from_dict(result['weights'], orient='index', columns=['Weight'])
        weight_df = weight_df[weight_df['Weight'] > 0.0001]
        weight_df = weight_df.sort_values('Weight', ascending=False)
        print(weight_df)
    else:
        print("\nOptimization did not succeed")
