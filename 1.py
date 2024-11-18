import re
import matplotlib.pyplot as plt

def extract_important_data(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    # Variables to store extracted data
    portfolios = []
    current_portfolio = {}

    # Extract data
    for line in lines:
        line = line.strip()
        if line.startswith("Expected Return:"):
            current_portfolio["expected_return"] = float(line.split(":")[1].strip())
        elif line.startswith("MAD Risk Measure:"):
            current_portfolio["mad_risk"] = float(line.split(":")[1].strip())
        elif line.startswith("Optimal Portfolio Weights:"):
            current_portfolio["weights"] = {}
        elif current_portfolio.get("weights") is not None and re.match(r".+\s+\d\.\d+$", line):
            asset, weight = line.rsplit(None, 1)
            current_portfolio["weights"][asset] = float(weight)
        elif line.startswith("Optimization Status: Optimal") or line.startswith("End of Portfolio"):
            if "expected_return" in current_portfolio and "mad_risk" in current_portfolio:
                portfolios.append(current_portfolio)
            current_portfolio = {}
        if len(portfolios) == 10:  # Stop after processing 10 portfolios
            break

    # Write to new file
    with open(output_file, 'w') as file:
        file.write("Efficient Frontier Analysis for MAD Model\n")
        file.write("=" * 50 + "\n\n")
        for i, portfolio in enumerate(portfolios, start=1):
            file.write(f"Portfolio {i}:\n")
            file.write(f"  Expected Return: {portfolio['expected_return']:.4f}\n")
            file.write(f"  MAD Risk Measure: {portfolio['mad_risk']:.4f}\n")
            file.write("  Weights:\n")
            for asset, weight in portfolio["weights"].items():
                file.write(f"    {asset}: {weight:.4f}\n")
            file.write("\n")
        file.write("=" * 50 + "\n")
        file.write("End of Report")

    return portfolios

def plot_efficient_frontier(portfolios):
    expected_returns = [p["expected_return"] for p in portfolios]
    mad_risks = [p["mad_risk"] for p in portfolios]

    plt.figure(figsize=(10, 6))
    plt.plot(mad_risks, expected_returns, marker='o', label="Efficient Frontier")
    plt.title("Efficient Frontier of MAD Model")
    plt.xlabel("MAD Risk")
    plt.ylabel("Expected Return")
    plt.grid()
    plt.legend()
    plt.show()

# Define file paths
input_file = 'mainData.txt'  # Update with the correct path
output_file = 'efficient_frontier_analysis.txt'

# Process the file and plot the efficient frontier
portfolios = extract_important_data(input_file, output_file)
plot_efficient_frontier(portfolios)

print(f"Data has been successfully processed and saved to {output_file}")