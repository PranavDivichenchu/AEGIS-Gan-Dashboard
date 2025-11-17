#!/usr/bin/env python3
"""
Visualization script for docking results
Generates comprehensive plots for binding affinity analysis
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 10)

# Load data
print("Loading docking results...")
df = pd.read_csv('docking_results/docking_results.csv')

# Create output directory for plots
output_dir = Path('docking_results/plots')
output_dir.mkdir(exist_ok=True)

print(f"Loaded {len(df)} docking results")
print(f"Proteases: {df['protease_name'].nunique()}")

# ============================================
# Plot 1: Overall Binding Affinity Distribution
# ============================================
print("\nGenerating Plot 1: Overall binding affinity distribution...")
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Histogram
axes[0].hist(df['binding_affinity'], bins=40, edgecolor='black', alpha=0.7, color='steelblue')
axes[0].axvline(df['binding_affinity'].mean(), color='red', linestyle='--',
                linewidth=2, label=f'Mean: {df["binding_affinity"].mean():.2f}')
axes[0].axvline(df['binding_affinity'].median(), color='orange', linestyle='--',
                linewidth=2, label=f'Median: {df["binding_affinity"].median():.2f}')
axes[0].set_xlabel('Binding Affinity (kcal/mol)', fontsize=12)
axes[0].set_ylabel('Frequency', fontsize=12)
axes[0].set_title('Distribution of Binding Affinities', fontsize=14, fontweight='bold')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Violin plot
parts = axes[1].violinplot([df['binding_affinity']], positions=[0],
                            showmeans=True, showmedians=True, widths=0.7)
for pc in parts['bodies']:
    pc.set_facecolor('steelblue')
    pc.set_alpha(0.7)
axes[1].set_ylabel('Binding Affinity (kcal/mol)', fontsize=12)
axes[1].set_title('Overall Binding Affinity Distribution', fontsize=14, fontweight='bold')
axes[1].set_xticks([])
axes[1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(output_dir / 'overall_distribution.png', dpi=300, bbox_inches='tight')
print(f"Saved: {output_dir}/overall_distribution.png")
plt.close()

# ============================================
# Plot 2: Binding Affinity by Protease (Boxplot)
# ============================================
print("\nGenerating Plot 2: Binding affinity by protease...")
fig, ax = plt.subplots(figsize=(16, 10))

# Sort by median binding affinity
protease_order = df.groupby('protease_name')['binding_affinity'].median().sort_values().index

sns.boxplot(data=df, y='protease_name', x='binding_affinity',
            order=protease_order, palette='viridis', ax=ax)
ax.axvline(-8, color='red', linestyle='--', alpha=0.5, linewidth=2, label='Strong binding threshold (-8)')
ax.set_xlabel('Binding Affinity (kcal/mol)', fontsize=12)
ax.set_ylabel('Protease', fontsize=12)
ax.set_title('Binding Affinity Distribution by Protease', fontsize=14, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig(output_dir / 'affinity_by_protease_boxplot.png', dpi=300, bbox_inches='tight')
print(f"Saved: {output_dir}/affinity_by_protease_boxplot.png")
plt.close()

# ============================================
# Plot 3: Mean Binding Affinity Heatmap
# ============================================
print("\nGenerating Plot 3: Mean binding affinity heatmap...")
fig, ax = plt.subplots(figsize=(12, 10))

# Calculate statistics by protease
protease_stats = df.groupby('protease_name')['binding_affinity'].agg([
    ('Mean', 'mean'),
    ('Median', 'median'),
    ('Min', 'min'),
    ('Max', 'max'),
    ('Count', 'count')
]).round(3)

# Sort by mean
protease_stats = protease_stats.sort_values('Mean')

# Create heatmap for the statistics
sns.heatmap(protease_stats[['Mean', 'Median', 'Min', 'Max']],
            annot=True, fmt='.2f', cmap='RdYlGn_r',
            cbar_kws={'label': 'Binding Affinity (kcal/mol)'}, ax=ax)
ax.set_title('Binding Affinity Statistics by Protease', fontsize=14, fontweight='bold')
ax.set_ylabel('Protease', fontsize=12)
ax.set_xlabel('Statistic', fontsize=12)

plt.tight_layout()
plt.savefig(output_dir / 'affinity_heatmap.png', dpi=300, bbox_inches='tight')
print(f"Saved: {output_dir}/affinity_heatmap.png")
plt.close()

# ============================================
# Plot 4: Top 20 Strongest Binders
# ============================================
print("\nGenerating Plot 4: Top 20 strongest binders...")
fig, ax = plt.subplots(figsize=(14, 10))

top20 = df.nsmallest(20, 'binding_affinity').copy()
top20['label'] = top20['peptide_id'] + '\n' + top20['peptide_sequence']

colors = plt.cm.viridis(np.linspace(0, 1, len(top20)))
bars = ax.barh(range(len(top20)), top20['binding_affinity'], color=colors, edgecolor='black')

ax.set_yticks(range(len(top20)))
ax.set_yticklabels(top20['label'], fontsize=9)
ax.set_xlabel('Binding Affinity (kcal/mol)', fontsize=12)
ax.set_title('Top 20 Strongest Binders', fontsize=14, fontweight='bold')
ax.axvline(-8, color='red', linestyle='--', alpha=0.5, linewidth=2, label='Strong binding threshold')
ax.invert_yaxis()
ax.legend()
ax.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig(output_dir / 'top20_binders.png', dpi=300, bbox_inches='tight')
print(f"Saved: {output_dir}/top20_binders.png")
plt.close()

# ============================================
# Plot 5: Binding Categories by Protease
# ============================================
print("\nGenerating Plot 5: Binding categories by protease...")
fig, ax = plt.subplots(figsize=(14, 8))

# Categorize binding affinities
df['binding_category'] = pd.cut(df['binding_affinity'],
                                  bins=[-np.inf, -8, -6, -4, np.inf],
                                  labels=['Strong (<-8)', 'Good (-8 to -6)',
                                          'Moderate (-6 to -4)', 'Weak (>-4)'])

# Count by category and protease
category_counts = df.groupby(['protease_name', 'binding_category']).size().unstack(fill_value=0)
category_counts = category_counts.loc[protease_order]

category_counts.plot(kind='barh', stacked=True, ax=ax,
                     color=['darkgreen', 'gold', 'orange', 'lightcoral'])
ax.set_xlabel('Number of Peptides', fontsize=12)
ax.set_ylabel('Protease', fontsize=12)
ax.set_title('Binding Strength Categories by Protease', fontsize=14, fontweight='bold')
ax.legend(title='Binding Strength', bbox_to_anchor=(1.05, 1), loc='upper left')
ax.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig(output_dir / 'binding_categories.png', dpi=300, bbox_inches='tight')
print(f"Saved: {output_dir}/binding_categories.png")
plt.close()

# ============================================
# Plot 6: Scatter plot - Binding Affinity vs Sequence ID
# ============================================
print("\nGenerating Plot 6: Binding affinity scatter plot...")
fig, ax = plt.subplots(figsize=(16, 8))

# Add numeric index
df['index'] = range(len(df))

# Color by protease
proteases = df['protease_name'].unique()
colors_map = dict(zip(proteases, plt.cm.tab20.colors[:len(proteases)]))

for protease in proteases:
    data = df[df['protease_name'] == protease]
    ax.scatter(data['index'], data['binding_affinity'],
              label=protease, alpha=0.6, s=30, color=colors_map[protease])

ax.axhline(-8, color='red', linestyle='--', alpha=0.5, linewidth=2, label='Strong binding threshold')
ax.set_xlabel('Peptide Index', fontsize=12)
ax.set_ylabel('Binding Affinity (kcal/mol)', fontsize=12)
ax.set_title('Binding Affinity Across All Peptides', fontsize=14, fontweight='bold')
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(output_dir / 'affinity_scatter.png', dpi=300, bbox_inches='tight')
print(f"Saved: {output_dir}/affinity_scatter.png")
plt.close()

# ============================================
# Plot 7: Distribution by Protease (Ridge plot style)
# ============================================
print("\nGenerating Plot 7: Ridge plot by protease...")
fig, axes = plt.subplots(len(protease_order), 1, figsize=(14, 2*len(protease_order)), sharex=True)

for idx, protease in enumerate(protease_order):
    data = df[df['protease_name'] == protease]['binding_affinity']
    axes[idx].hist(data, bins=20, alpha=0.7, color='steelblue', edgecolor='black')
    axes[idx].set_ylabel(protease, fontsize=9, rotation=0, ha='right')
    axes[idx].axvline(data.mean(), color='red', linestyle='--', linewidth=1)
    axes[idx].set_yticks([])
    axes[idx].spines['top'].set_visible(False)
    axes[idx].spines['right'].set_visible(False)
    axes[idx].spines['left'].set_visible(False)

axes[-1].set_xlabel('Binding Affinity (kcal/mol)', fontsize=12)
fig.suptitle('Binding Affinity Distributions by Protease (Ridge Plot)',
             fontsize=14, fontweight='bold', y=0.995)

plt.tight_layout()
plt.savefig(output_dir / 'ridge_plot.png', dpi=300, bbox_inches='tight')
print(f"Saved: {output_dir}/ridge_plot.png")
plt.close()

print("\n" + "="*60)
print("ALL VISUALIZATIONS COMPLETED SUCCESSFULLY!")
print("="*60)
print(f"\nAll plots saved to: {output_dir.absolute()}")
print("\nGenerated plots:")
print("  1. overall_distribution.png - Overall binding affinity distribution")
print("  2. affinity_by_protease_boxplot.png - Boxplot by protease")
print("  3. affinity_heatmap.png - Statistics heatmap")
print("  4. top20_binders.png - Top 20 strongest binders")
print("  5. binding_categories.png - Binding strength categories")
print("  6. affinity_scatter.png - Scatter plot of all results")
print("  7. ridge_plot.png - Ridge plot distributions")
