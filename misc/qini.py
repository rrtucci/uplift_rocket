import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def qini_curve(data, treatment_col, outcome_col, uplift_col, n_bins=10):
    # Sort data by predicted uplift descending
    data_sorted = data.sort_values(by=uplift_col, ascending=False).reset_index(
        drop=True)
    data_sorted['rank'] = np.arange(1, len(data_sorted) + 1)

    # Total number of treated and control
    treated = data_sorted[data_sorted[treatment_col] == 1]
    control = data_sorted[data_sorted[treatment_col] == 0]

    total_treated = len(treated)
    total_control = len(control)

    # Cumulative uplift gain calculation
    qini_values = []
    population_pct = []

    step = len(data_sorted) // n_bins
    for i in range(step, len(data_sorted) + 1, step):
        subset = data_sorted.iloc[:i]
        treat_resp = subset[(subset[treatment_col] == 1)][outcome_col].sum()
        ctrl_resp = subset[(subset[treatment_col] == 0)][outcome_col].sum()

        # Expected control outcome if treated population was randomly selected
        ctrl_adj = (ctrl_resp / total_control) * len(
            subset[subset[treatment_col] == 1])
        uplift = treat_resp - ctrl_adj

        qini_values.append(uplift)
        population_pct.append(i / len(data_sorted))

    return population_pct, qini_values


def plot_qini_curve(pop_pct, qini_vals):
    plt.figure(figsize=(8, 6))
    plt.plot(pop_pct, qini_vals, label="Qini Curve", marker='o')
    plt.plot([0, 1], [0, max(qini_vals)], 'k--', label="Random Model")
    plt.fill_between(pop_pct, qini_vals, step="mid", alpha=0.2)
    plt.xlabel("Proportion of Population Targeted")
    plt.ylabel("Incremental Responses (Uplift)")
    plt.title("Qini Curve for Uplift Model")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def calculate_qini_auc(pop_pct, qini_vals):
    return np.trapezoid(qini_vals, pop_pct)


# Example usage
if __name__ == "__main__":
    # Load or simulate data
    # Sample simulated dataset
    np.random.seed(42)
    size = 10000
    df = pd.DataFrame({
        'treatment': np.random.binomial(1, 0.5, size),
        'outcome': np.random.binomial(1, 0.1, size),
        'predicted_uplift': np.random.normal(0, 1, size)
    })

    # Calculate Qini curve
    pop_pct, qini_vals = qini_curve(df, 'treatment', 'outcome',
                                    'predicted_uplift', n_bins=20)

    # Plot Qini curve
    plot_qini_curve(pop_pct, qini_vals)

    # Calculate Qini AUC
    auc = calculate_qini_auc(pop_pct, qini_vals)
    print(f"Qini AUC: {auc:.4f}")
