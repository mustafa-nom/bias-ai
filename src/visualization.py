"""Data visualization utilities for displaying analysis results."""

from collections import Counter
import matplotlib.pyplot as plt

def plot_bias_distribution(leaning_tally):
    """Create a bar chart of political bias distribution."""
    if not leaning_tally:
        print("No data to visualize.")
        return
    
    counts = Counter(leaning_tally)
    labels = list(counts.keys())
    values = list(counts.values())
    
    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color=['blue', 'purple', 'red', 'green'])
    plt.title('Distribution of Political Bias in Articles')
    plt.xlabel('Political Leaning')
    plt.ylabel('Number of Articles')
    plt.tight_layout()
    
    # Save or display the chart
    plt.savefig('bias_distribution.png')
    plt.show()

def print_bias_summary(leaning_tally):
    """Print a text summary of political bias distribution."""
    print("\n📊 Political Leaning Comparison:")
    if leaning_tally:
        counts = Counter(leaning_tally)
        for lean, num in counts.items():
            print(f"  - {lean.capitalize()}: {num} article(s)")
    else:
        print("  No political leanings detected.")