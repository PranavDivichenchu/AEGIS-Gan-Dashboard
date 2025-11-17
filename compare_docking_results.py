#!/usr/bin/env python3
"""
Compare Docking Results: ConditionalGAN vs SupremeGAN
Analyzes and compares binding affinity results from two different GAN models
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
from scipy import stats

print("="*80)
print("DOCKING RESULTS COMPARISON: ConditionalGAN vs SupremeGAN")
print("="*80)

# Load both docking result files
print("\nLoading docking results...")
cgan_results = pd.read_csv('docking_results/docking_results_conditionalgan.csv')
supreme_results = pd.read_csv('docking_results/docking_results.csv')

# Add model labels
cgan_results['model'] = 'ConditionalGAN'
supreme_results['model'] = 'SupremeGAN'

# Combine datasets
all_results = pd.concat([cgan_results, supreme_results], ignore_index=True)

print(f"ConditionalGAN: {len(cgan_results)} docking results")
print(f"SupremeGAN: {len(supreme_results)} docking results")
print(f"Total: {len(all_results)} docking results")

# Filter only successful docking results
all_results = all_results[all_results['status'] == 'success'].copy()
print(f"\nSuccessful dockings: {len(all_results)}")

# ============================================
# OVERALL PERFORMANCE COMPARISON
# ============================================
print("\n" + "="*80)
print("OVERALL PERFORMANCE METRICS")
print("="*80)

for model in ['ConditionalGAN', 'SupremeGAN']:
    model_data = all_results[all_results['model'] == model]
    affinities = model_data['binding_affinity']

    print(f"\n{model}:")
    print(f"  Total peptides: {len(model_data)}")
    print(f"  Mean affinity: {affinities.mean():.3f} kcal/mol")
    print(f"  Median affinity: {affinities.median():.3f} kcal/mol")
    print(f"  Std dev: {affinities.std():.3f} kcal/mol")
    print(f"  Best affinity: {affinities.min():.3f} kcal/mol")
    print(f"  Worst affinity: {affinities.max():.3f} kcal/mol")

    # Binding categories
    excellent = (affinities < -10).sum()
    strong = ((affinities >= -10) & (affinities < -8)).sum()
    good = ((affinities >= -8) & (affinities < -6)).sum()
    moderate = (affinities >= -6).sum()

    print(f"\n  Binding Categories:")
    print(f"    Excellent (<-10 kcal/mol): {excellent} ({100*excellent/len(model_data):.1f}%)")
    print(f"    Strong (-10 to -8): {strong} ({100*strong/len(model_data):.1f}%)")
    print(f"    Good (-8 to -6): {good} ({100*good/len(model_data):.1f}%)")
    print(f"    Moderate (>-6): {moderate} ({100*moderate/len(model_data):.1f}%)")

# Statistical comparison
print("\n" + "="*80)
print("STATISTICAL COMPARISON")
print("="*80)

cgan_affinities = all_results[all_results['model'] == 'ConditionalGAN']['binding_affinity']
supreme_affinities = all_results[all_results['model'] == 'SupremeGAN']['binding_affinity']

# T-test
t_stat, p_value = stats.ttest_ind(cgan_affinities, supreme_affinities)
print(f"\nIndependent t-test:")
print(f"  t-statistic: {t_stat:.4f}")
print(f"  p-value: {p_value:.6f}")

if p_value < 0.05:
    winner = 'ConditionalGAN' if cgan_affinities.mean() < supreme_affinities.mean() else 'SupremeGAN'
    print(f"  ✓ Statistically significant difference (p < 0.05)")
    print(f"  Winner: {winner}")
else:
    print(f"  No statistically significant difference (p >= 0.05)")

# Effect size (Cohen's d)
pooled_std = np.sqrt(((len(cgan_affinities)-1)*cgan_affinities.std()**2 +
                       (len(supreme_affinities)-1)*supreme_affinities.std()**2) /
                      (len(cgan_affinities) + len(supreme_affinities) - 2))
cohens_d = (cgan_affinities.mean() - supreme_affinities.mean()) / pooled_std
print(f"\nEffect Size (Cohen's d): {cohens_d:.4f}")
if abs(cohens_d) < 0.2:
    print("  (Small effect)")
elif abs(cohens_d) < 0.5:
    print("  (Medium effect)")
else:
    print("  (Large effect)")

# ============================================
# PROTEASE-SPECIFIC COMPARISON
# ============================================
print("\n" + "="*80)
print("PROTEASE-SPECIFIC PERFORMANCE")
print("="*80)

protease_stats = all_results.groupby(['protease_name', 'model'])['binding_affinity'].agg([
    ('count', 'count'),
    ('mean', 'mean'),
    ('median', 'median'),
    ('min', 'min'),
    ('std', 'std')
]).round(3)

print(f"\n{'Protease':<40} {'Model':<15} {'Count':>6} {'Mean':>8} {'Median':>8} {'Best':>8} {'Std':>7}")
print("-"*100)
for (protease, model), row in protease_stats.iterrows():
    print(f"{protease:<40} {model:<15} {row['count']:>6.0f} {row['mean']:>8.3f} {row['median']:>8.3f} {row['min']:>8.3f} {row['std']:>7.3f}")

# Determine winner per protease
print("\n" + "="*80)
print("WINNER PER PROTEASE (by mean affinity)")
print("="*80)
print(f"{'Protease':<40} {'Winner':<15} {'Difference':>12}")
print("-"*80)

winner_counts = {'ConditionalGAN': 0, 'SupremeGAN': 0, 'Tie': 0}
protease_winners = []

for protease in all_results['protease_name'].unique():
    protease_data = all_results[all_results['protease_name'] == protease]
    means = protease_data.groupby('model')['binding_affinity'].mean()

    if len(means) == 2:
        diff = means['ConditionalGAN'] - means['SupremeGAN']

        if abs(diff) < 0.1:  # Tie threshold
            winner = 'Tie'
            winner_counts['Tie'] += 1
        elif means['ConditionalGAN'] < means['SupremeGAN']:
            winner = 'ConditionalGAN'
            winner_counts['ConditionalGAN'] += 1
        else:
            winner = 'SupremeGAN'
            winner_counts['SupremeGAN'] += 1

        protease_winners.append({
            'protease': protease,
            'winner': winner,
            'difference': abs(diff)
        })

        print(f"{protease:<40} {winner:<15} {abs(diff):>12.3f}")

print(f"\n\nOverall Winner Count:")
print(f"  ConditionalGAN wins: {winner_counts['ConditionalGAN']}")
print(f"  SupremeGAN wins: {winner_counts['SupremeGAN']}")
print(f"  Ties: {winner_counts['Tie']}")

# ============================================
# TOP PERFORMERS
# ============================================
print("\n" + "="*80)
print("TOP 10 BEST BINDERS")
print("="*80)

top10_overall = all_results.nsmallest(10, 'binding_affinity')
print(f"\n{'Rank':<6} {'Model':<15} {'Affinity':>10} {'Protease':<40} {'Sequence'}")
print("-"*120)
for idx, (_, row) in enumerate(top10_overall.iterrows(), 1):
    print(f"{idx:<6} {row['model']:<15} {row['binding_affinity']:>10.3f} {row['protease_name']:<40} {row['peptide_sequence']}")

print("\n\nTop 10 per Model:")
for model in ['ConditionalGAN', 'SupremeGAN']:
    print(f"\n{model} Top 10:")
    model_data = all_results[all_results['model'] == model]
    top10 = model_data.nsmallest(10, 'binding_affinity')

    for idx, (_, row) in enumerate(top10.iterrows(), 1):
        print(f"  {idx}. {row['binding_affinity']:>7.3f} kcal/mol - {row['peptide_sequence']} ({row['protease_name']})")

# ============================================
# VISUALIZATIONS
# ============================================
print("\n" + "="*80)
print("GENERATING VISUALIZATIONS")
print("="*80)

output_dir = Path('docking_results/plots')
output_dir.mkdir(exist_ok=True)

# Set style
sns.set_style("whitegrid")
plt.rcParams['font.size'] = 10

# Plot 1: Overall Distribution Comparison
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Boxplot
sns.boxplot(data=all_results, x='model', y='binding_affinity',
            palette={'ConditionalGAN': '#FF6B6B', 'SupremeGAN': '#4ECDC4'},
            ax=axes[0, 0])
axes[0, 0].axhline(-8, color='red', linestyle='--', alpha=0.5, label='Strong binding')
axes[0, 0].axhline(-10, color='darkred', linestyle='--', alpha=0.5, label='Excellent binding')
axes[0, 0].set_title('Binding Affinity Distribution Comparison', fontweight='bold', fontsize=14)
axes[0, 0].set_xlabel('GAN Model', fontsize=12)
axes[0, 0].set_ylabel('Binding Affinity (kcal/mol)', fontsize=12)
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# Violin plot
parts = axes[0, 1].violinplot([cgan_affinities, supreme_affinities],
                               positions=[0, 1], showmeans=True, showmedians=True)
for pc, color in zip(parts['bodies'], ['#FF6B6B', '#4ECDC4']):
    pc.set_facecolor(color)
    pc.set_alpha(0.7)
axes[0, 1].set_xticks([0, 1])
axes[0, 1].set_xticklabels(['ConditionalGAN', 'SupremeGAN'])
axes[0, 1].set_ylabel('Binding Affinity (kcal/mol)', fontsize=12)
axes[0, 1].set_title('Distribution Shape Comparison', fontweight='bold', fontsize=14)
axes[0, 1].axhline(-8, color='red', linestyle='--', alpha=0.5)
axes[0, 1].grid(True, alpha=0.3)

# Histogram overlay
axes[1, 0].hist(cgan_affinities, bins=30, alpha=0.6, label='ConditionalGAN',
                color='#FF6B6B', edgecolor='black')
axes[1, 0].hist(supreme_affinities, bins=30, alpha=0.6, label='SupremeGAN',
                color='#4ECDC4', edgecolor='black')
axes[1, 0].axvline(cgan_affinities.mean(), color='#FF6B6B', linestyle='--', linewidth=2)
axes[1, 0].axvline(supreme_affinities.mean(), color='#4ECDC4', linestyle='--', linewidth=2)
axes[1, 0].set_xlabel('Binding Affinity (kcal/mol)', fontsize=12)
axes[1, 0].set_ylabel('Frequency', fontsize=12)
axes[1, 0].set_title('Overlaid Distributions', fontweight='bold', fontsize=14)
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

# Cumulative distribution
cgan_sorted = np.sort(cgan_affinities)
supreme_sorted = np.sort(supreme_affinities)
cgan_cumulative = np.arange(1, len(cgan_sorted) + 1) / len(cgan_sorted)
supreme_cumulative = np.arange(1, len(supreme_sorted) + 1) / len(supreme_sorted)

axes[1, 1].plot(cgan_sorted, cgan_cumulative, label='ConditionalGAN',
                color='#FF6B6B', linewidth=2)
axes[1, 1].plot(supreme_sorted, supreme_cumulative, label='SupremeGAN',
                color='#4ECDC4', linewidth=2)
axes[1, 1].axvline(-8, color='red', linestyle='--', alpha=0.5, label='Strong binding')
axes[1, 1].set_xlabel('Binding Affinity (kcal/mol)', fontsize=12)
axes[1, 1].set_ylabel('Cumulative Probability', fontsize=12)
axes[1, 1].set_title('Cumulative Distribution Function', fontweight='bold', fontsize=14)
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(output_dir / 'overall_comparison.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: {output_dir}/overall_comparison.png")
plt.close()

# Plot 2: Protease-specific comparison
proteases = sorted(all_results['protease_name'].unique())
fig, ax = plt.subplots(figsize=(16, max(10, len(proteases) * 0.5)))

data_for_plot = []
positions = []
colors = []

for i, protease in enumerate(proteases):
    protease_data = all_results[all_results['protease_name'] == protease]

    for j, model in enumerate(['ConditionalGAN', 'SupremeGAN']):
        model_data = protease_data[protease_data['model'] == model]
        if len(model_data) > 0:
            data_for_plot.append(model_data['binding_affinity'].values)
            positions.append(i*3 + j)
            colors.append('#FF6B6B' if model == 'ConditionalGAN' else '#4ECDC4')

bp = ax.boxplot(data_for_plot, positions=positions, widths=0.6, patch_artist=True,
                showfliers=True)

for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

ax.axhline(-8, color='red', linestyle='--', alpha=0.3, linewidth=1.5, label='Strong binding')
ax.axhline(-10, color='darkred', linestyle='--', alpha=0.3, linewidth=1.5, label='Excellent binding')
ax.set_xticks([i*3 + 0.5 for i in range(len(proteases))])
ax.set_xticklabels(proteases, rotation=45, ha='right', fontsize=9)
ax.set_ylabel('Binding Affinity (kcal/mol)', fontsize=12)
ax.set_title('GAN Model Performance by Protease', fontweight='bold', fontsize=14)
ax.grid(True, alpha=0.3, axis='y')

from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#FF6B6B', alpha=0.7, label='ConditionalGAN'),
    Patch(facecolor='#4ECDC4', alpha=0.7, label='SupremeGAN'),
    plt.Line2D([0], [0], color='red', linestyle='--', alpha=0.5, label='Strong binding'),
    plt.Line2D([0], [0], color='darkred', linestyle='--', alpha=0.5, label='Excellent binding')
]
ax.legend(handles=legend_elements, loc='upper right')

plt.tight_layout()
plt.savefig(output_dir / 'protease_comparison.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: {output_dir}/protease_comparison.png")
plt.close()

# Plot 3: Winner pie chart
fig, ax = plt.subplots(figsize=(10, 8))
colors_pie = ['#FF6B6B', '#4ECDC4', '#95E1D3']
wedges, texts, autotexts = ax.pie(
    winner_counts.values(),
    labels=[f"{k}\n({v} proteases)" for k, v in winner_counts.items()],
    autopct='%1.1f%%',
    colors=colors_pie,
    startangle=90,
    textprops={'fontsize': 12, 'fontweight': 'bold'}
)
ax.set_title(f'Protease-Level Winner Distribution\n(Total: {len(proteases)} proteases)',
             fontsize=14, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig(output_dir / 'winner_distribution.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: {output_dir}/winner_distribution.png")
plt.close()

# Plot 4: Top binders comparison
fig, axes = plt.subplots(1, 2, figsize=(18, 10))

for idx, model in enumerate(['ConditionalGAN', 'SupremeGAN']):
    model_data = all_results[all_results['model'] == model]
    top10 = model_data.nsmallest(10, 'binding_affinity')

    colors_bar = plt.cm.viridis(np.linspace(0, 1, len(top10)))
    bars = axes[idx].barh(range(len(top10)), top10['binding_affinity'],
                          color=colors_bar, edgecolor='black', linewidth=1.5)

    axes[idx].set_yticks(range(len(top10)))
    axes[idx].set_yticklabels([f"{row['peptide_sequence']}\n({row['protease_name'][:20]}...)"
                                for _, row in top10.iterrows()], fontsize=9)
    axes[idx].set_xlabel('Binding Affinity (kcal/mol)', fontsize=12)
    axes[idx].set_title(f'Top 10 Binders - {model}', fontweight='bold', fontsize=14)
    axes[idx].axvline(-8, color='red', linestyle='--', alpha=0.5, linewidth=2, label='Strong')
    axes[idx].axvline(-10, color='darkred', linestyle='--', alpha=0.5, linewidth=2, label='Excellent')
    axes[idx].invert_yaxis()
    axes[idx].grid(True, alpha=0.3, axis='x')
    axes[idx].legend()

plt.tight_layout()
plt.savefig(output_dir / 'top_binders_comparison.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: {output_dir}/top_binders_comparison.png")
plt.close()

# Plot 5: Performance summary bar chart
fig, ax = plt.subplots(figsize=(12, 8))

metrics = ['Mean Affinity', 'Median Affinity', 'Best Affinity', 'Std Dev']
cgan_values = [
    cgan_affinities.mean(),
    cgan_affinities.median(),
    cgan_affinities.min(),
    cgan_affinities.std()
]
supreme_values = [
    supreme_affinities.mean(),
    supreme_affinities.median(),
    supreme_affinities.min(),
    supreme_affinities.std()
]

x = np.arange(len(metrics))
width = 0.35

bars1 = ax.bar(x - width/2, cgan_values, width, label='ConditionalGAN',
               color='#FF6B6B', alpha=0.8, edgecolor='black')
bars2 = ax.bar(x + width/2, supreme_values, width, label='SupremeGAN',
               color='#4ECDC4', alpha=0.8, edgecolor='black')

ax.set_xlabel('Metrics', fontsize=12)
ax.set_ylabel('Binding Affinity (kcal/mol)', fontsize=12)
ax.set_title('Performance Metrics Comparison', fontweight='bold', fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(metrics)
ax.legend()
ax.grid(True, alpha=0.3, axis='y')

# Add value labels on bars
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}',
                ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig(output_dir / 'metrics_comparison.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: {output_dir}/metrics_comparison.png")
plt.close()

# Save detailed comparison data
comparison_df = pd.DataFrame({
    'Metric': ['Total Peptides', 'Mean Affinity', 'Median Affinity', 'Std Dev',
               'Best Affinity', 'Worst Affinity', 'Excellent (<-10)', 'Strong (-10 to -8)',
               'Good (-8 to -6)', 'Moderate (>-6)'],
    'ConditionalGAN': [
        len(cgan_affinities),
        cgan_affinities.mean(),
        cgan_affinities.median(),
        cgan_affinities.std(),
        cgan_affinities.min(),
        cgan_affinities.max(),
        (cgan_affinities < -10).sum(),
        ((cgan_affinities >= -10) & (cgan_affinities < -8)).sum(),
        ((cgan_affinities >= -8) & (cgan_affinities < -6)).sum(),
        (cgan_affinities >= -6).sum()
    ],
    'SupremeGAN': [
        len(supreme_affinities),
        supreme_affinities.mean(),
        supreme_affinities.median(),
        supreme_affinities.std(),
        supreme_affinities.min(),
        supreme_affinities.max(),
        (supreme_affinities < -10).sum(),
        ((supreme_affinities >= -10) & (supreme_affinities < -8)).sum(),
        ((supreme_affinities >= -8) & (supreme_affinities < -6)).sum(),
        (supreme_affinities >= -6).sum()
    ]
})

comparison_df.to_csv('docking_results/summary_comparison.csv', index=False)
print(f"✓ Saved: docking_results/summary_comparison.csv")

# Save combined results with model labels
all_results.to_csv('docking_results/combined_results_with_models.csv', index=False)
print(f"✓ Saved: docking_results/combined_results_with_models.csv")

print("\n" + "="*80)
print("ANALYSIS COMPLETE!")
print("="*80)
print(f"\nAll results saved to: {output_dir.absolute()}")
print("\nGenerated files:")
print("  1. summary_comparison.csv - Statistical summary")
print("  2. combined_results_with_models.csv - Full dataset with model labels")
print("  3. overall_comparison.png - Overall distribution comparison")
print("  4. protease_comparison.png - Protease-specific comparison")
print("  5. winner_distribution.png - Winner breakdown")
print("  6. top_binders_comparison.png - Top 10 binders per model")
print("  7. metrics_comparison.png - Performance metrics summary")

print("\n" + "="*80)
print("KEY FINDINGS SUMMARY")
print("="*80)
overall_winner = 'ConditionalGAN' if cgan_affinities.mean() < supreme_affinities.mean() else 'SupremeGAN'
print(f"1. Overall Best Model: {overall_winner}")
print(f"2. Statistical Significance: {'Yes' if p_value < 0.05 else 'No'} (p={p_value:.4f})")
print(f"3. Protease-Level Winners:")
print(f"   - ConditionalGAN: {winner_counts['ConditionalGAN']} proteases")
print(f"   - SupremeGAN: {winner_counts['SupremeGAN']} proteases")
print(f"   - Ties: {winner_counts['Tie']} proteases")
print(f"4. Best Overall Binder: {top10_overall.iloc[0]['binding_affinity']:.3f} kcal/mol ({top10_overall.iloc[0]['model']})")
