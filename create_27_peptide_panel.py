#!/usr/bin/env python3
"""
Create 27-Peptide Panel: Ensemble Approach
Select the best peptide for each protease from either ConditionalGAN or SupremeGAN
"""

import pandas as pd
import numpy as np
from pathlib import Path

print("="*80)
print("27-PEPTIDE PANEL SELECTION: ENSEMBLE APPROACH")
print("="*80)

# Load combined results with model labels
df = pd.read_csv('docking_results/combined_results_with_models.csv')
print(f"\nTotal docking results: {len(df)}")
print(f"Total proteases: {df['protease_name'].nunique()}")

# Get unique proteases
proteases = sorted(df['protease_name'].unique())
print(f"\nProteases identified: {len(proteases)}")

# Selection strategy: Best peptide per protease (regardless of model)
panel = []
model_counts = {'ConditionalGAN': 0, 'SupremeGAN': 0}

print("\n" + "="*80)
print("SELECTING BEST PEPTIDE PER PROTEASE")
print("="*80)
print(f"{'Rank':<5} {'Protease':<40} {'Model':<15} {'Affinity':>10} {'Sequence'}")
print("-"*120)

for rank, protease in enumerate(proteases, 1):
    # Get all peptides for this protease
    protease_data = df[df['protease_name'] == protease]

    # Find the best binder (most negative affinity)
    best_peptide = protease_data.loc[protease_data['binding_affinity'].idxmin()]

    panel.append({
        'rank': rank,
        'protease_name': best_peptide['protease_name'],
        'merops_id': best_peptide['merops_id'],
        'peptide_id': best_peptide['peptide_id'],
        'peptide_sequence': best_peptide['peptide_sequence'],
        'binding_affinity': best_peptide['binding_affinity'],
        'model': best_peptide['model'],
        'receptor_pdbqt': best_peptide['receptor_pdbqt'],
        'ligand_pdbqt': best_peptide['ligand_pdbqt'],
        'output_pdbqt': best_peptide['output_pdbqt']
    })

    model_counts[best_peptide['model']] += 1

    print(f"{rank:<5} {protease:<40} {best_peptide['model']:<15} {best_peptide['binding_affinity']:>10.3f} {best_peptide['peptide_sequence']}")

# Create DataFrame
panel_df = pd.DataFrame(panel)

print("\n" + "="*80)
print("PANEL STATISTICS")
print("="*80)
print(f"\nTotal peptides in panel: {len(panel_df)}")
print(f"ConditionalGAN contributions: {model_counts['ConditionalGAN']} ({100*model_counts['ConditionalGAN']/len(panel_df):.1f}%)")
print(f"SupremeGAN contributions: {model_counts['SupremeGAN']} ({100*model_counts['SupremeGAN']/len(panel_df):.1f}%)")

print(f"\nBinding Affinity Statistics:")
print(f"  Mean: {panel_df['binding_affinity'].mean():.3f} kcal/mol")
print(f"  Median: {panel_df['binding_affinity'].median():.3f} kcal/mol")
print(f"  Best: {panel_df['binding_affinity'].min():.3f} kcal/mol")
print(f"  Worst: {panel_df['binding_affinity'].max():.3f} kcal/mol")
print(f"  Std Dev: {panel_df['binding_affinity'].std():.3f} kcal/mol")

# Categorize binders
excellent = (panel_df['binding_affinity'] < -10).sum()
strong = ((panel_df['binding_affinity'] >= -10) & (panel_df['binding_affinity'] < -8)).sum()
good = ((panel_df['binding_affinity'] >= -8) & (panel_df['binding_affinity'] < -6)).sum()
moderate = (panel_df['binding_affinity'] >= -6).sum()

print(f"\nBinding Categories:")
print(f"  Excellent (<-10 kcal/mol): {excellent} ({100*excellent/len(panel_df):.1f}%)")
print(f"  Strong (-10 to -8): {strong} ({100*strong/len(panel_df):.1f}%)")
print(f"  Good (-8 to -6): {good} ({100*good/len(panel_df):.1f}%)")
print(f"  Moderate (>-6): {moderate} ({100*moderate/len(panel_df):.1f}%)")

# Save the panel
output_file = 'docking_results/27_peptide_panel.csv'
panel_df.to_csv(output_file, index=False)
print(f"\n✓ Saved panel to: {output_file}")

# Create a synthesis-ready format
synthesis_df = panel_df[['rank', 'peptide_sequence', 'protease_name', 'binding_affinity', 'model']].copy()
synthesis_df.columns = ['Panel_ID', 'Sequence', 'Target_Protease', 'Predicted_Affinity_kcal_mol', 'Source_Model']
synthesis_file = 'docking_results/27_peptide_panel_synthesis_ready.csv'
synthesis_df.to_csv(synthesis_file, index=False)
print(f"✓ Saved synthesis-ready format to: {synthesis_file}")

# Create detailed report
print("\n" + "="*80)
print("GENERATING DETAILED REPORT")
print("="*80)

report_lines = []
report_lines.append("="*80)
report_lines.append("27-PEPTIDE INHIBITOR PANEL: ENSEMBLE SELECTION")
report_lines.append("="*80)
report_lines.append("")
report_lines.append("SELECTION STRATEGY:")
report_lines.append("  - One peptide per protease (27 proteases total)")
report_lines.append("  - Best binder selected from either ConditionalGAN or SupremeGAN")
report_lines.append("  - Ensemble approach: leverage strengths of both models")
report_lines.append("")
report_lines.append("PANEL COMPOSITION:")
report_lines.append(f"  - ConditionalGAN: {model_counts['ConditionalGAN']} peptides ({100*model_counts['ConditionalGAN']/len(panel_df):.1f}%)")
report_lines.append(f"  - SupremeGAN: {model_counts['SupremeGAN']} peptides ({100*model_counts['SupremeGAN']/len(panel_df):.1f}%)")
report_lines.append("")
report_lines.append("BINDING AFFINITY DISTRIBUTION:")
report_lines.append(f"  - Mean: {panel_df['binding_affinity'].mean():.3f} kcal/mol")
report_lines.append(f"  - Median: {panel_df['binding_affinity'].median():.3f} kcal/mol")
report_lines.append(f"  - Range: {panel_df['binding_affinity'].min():.3f} to {panel_df['binding_affinity'].max():.3f} kcal/mol")
report_lines.append("")
report_lines.append("BINDING CATEGORIES:")
report_lines.append(f"  - Excellent (<-10): {excellent} peptides ({100*excellent/len(panel_df):.1f}%)")
report_lines.append(f"  - Strong (-10 to -8): {strong} peptides ({100*strong/len(panel_df):.1f}%)")
report_lines.append(f"  - Good (-8 to -6): {good} peptides ({100*good/len(panel_df):.1f}%)")
report_lines.append(f"  - Moderate (>-6): {moderate} peptides ({100*moderate/len(panel_df):.1f}%)")
report_lines.append("")
report_lines.append("="*80)
report_lines.append("DETAILED PANEL")
report_lines.append("="*80)
report_lines.append("")

for _, row in panel_df.iterrows():
    report_lines.append(f"Panel ID: {row['rank']}")
    report_lines.append(f"  Sequence: {row['peptide_sequence']}")
    report_lines.append(f"  Target: {row['protease_name']} ({row['merops_id']})")
    report_lines.append(f"  Binding Affinity: {row['binding_affinity']:.3f} kcal/mol")
    report_lines.append(f"  Source Model: {row['model']}")
    report_lines.append(f"  Original ID: {row['peptide_id']}")
    report_lines.append("")

report_lines.append("="*80)
report_lines.append("RECOMMENDED NEXT STEPS")
report_lines.append("="*80)
report_lines.append("")
report_lines.append("1. PRIORITIZATION:")
report_lines.append(f"   - Start with top {excellent} excellent binders (<-10 kcal/mol)")
report_lines.append("   - Consider clinical relevance of target proteases")
report_lines.append("   - Evaluate drug-likeness properties")
report_lines.append("")
report_lines.append("2. EXPERIMENTAL VALIDATION:")
report_lines.append("   - Synthesize peptides (consider N-/C-terminal modifications)")
report_lines.append("   - In vitro binding assays (SPR, ITC, fluorescence)")
report_lines.append("   - Enzymatic inhibition assays (IC50 determination)")
report_lines.append("   - Cell-based assays for most promising candidates")
report_lines.append("")
report_lines.append("3. OPTIMIZATION:")
report_lines.append("   - Structure-activity relationship (SAR) studies")
report_lines.append("   - Sequence modifications for improved stability")
report_lines.append("   - ADMET profiling")
report_lines.append("   - Consider cyclization or other modifications")
report_lines.append("")
report_lines.append("4. COMPUTATIONAL FOLLOW-UP:")
report_lines.append("   - Molecular dynamics simulations")
report_lines.append("   - Binding pose analysis")
report_lines.append("   - ADMET predictions")
report_lines.append("   - Generate additional variants using successful models")
report_lines.append("")

report_file = 'docking_results/27_peptide_panel_report.txt'
with open(report_file, 'w') as f:
    f.write('\n'.join(report_lines))

print(f"✓ Saved detailed report to: {report_file}")

# Create visualization
import matplotlib.pyplot as plt
import seaborn as sns

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Plot 1: Binding affinities ranked
colors = ['#FF6B6B' if m == 'ConditionalGAN' else '#4ECDC4' for m in panel_df['model']]
axes[0, 0].barh(range(len(panel_df)), panel_df['binding_affinity'], color=colors, edgecolor='black')
axes[0, 0].set_yticks(range(len(panel_df)))
axes[0, 0].set_yticklabels([f"{i+1}" for i in range(len(panel_df))], fontsize=8)
axes[0, 0].set_xlabel('Binding Affinity (kcal/mol)', fontsize=11)
axes[0, 0].set_ylabel('Panel ID', fontsize=11)
axes[0, 0].set_title('27-Peptide Panel: Binding Affinities', fontweight='bold', fontsize=12)
axes[0, 0].axvline(-8, color='red', linestyle='--', alpha=0.5, label='Strong')
axes[0, 0].axvline(-10, color='darkred', linestyle='--', alpha=0.5, label='Excellent')
axes[0, 0].invert_yaxis()
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3, axis='x')

# Plot 2: Model contribution pie chart
model_data = panel_df['model'].value_counts()
colors_pie = ['#FF6B6B' if idx == 'ConditionalGAN' else '#4ECDC4' for idx in model_data.index]
wedges, texts, autotexts = axes[0, 1].pie(
    model_data.values,
    labels=[f"{idx}\n({val} peptides)" for idx, val in model_data.items()],
    autopct='%1.1f%%',
    colors=colors_pie,
    startangle=90,
    textprops={'fontsize': 11, 'fontweight': 'bold'}
)
axes[0, 1].set_title('Model Contribution to Panel', fontweight='bold', fontsize=12)

# Plot 3: Binding category breakdown
categories = ['Excellent\n(<-10)', 'Strong\n(-10 to -8)', 'Good\n(-8 to -6)', 'Moderate\n(>-6)']
category_counts = [excellent, strong, good, moderate]
colors_bar = ['darkgreen', 'green', 'orange', 'red']
bars = axes[1, 0].bar(categories, category_counts, color=colors_bar, alpha=0.7, edgecolor='black')
axes[1, 0].set_ylabel('Number of Peptides', fontsize=11)
axes[1, 0].set_title('Binding Category Distribution', fontweight='bold', fontsize=12)
axes[1, 0].grid(True, alpha=0.3, axis='y')

# Add value labels
for bar in bars:
    height = bar.get_height()
    axes[1, 0].text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')

# Plot 4: Top 10 peptides
top10 = panel_df.nsmallest(10, 'binding_affinity')
colors_top = ['#FF6B6B' if m == 'ConditionalGAN' else '#4ECDC4' for m in top10['model']]
axes[1, 1].barh(range(len(top10)), top10['binding_affinity'], color=colors_top, edgecolor='black')
axes[1, 1].set_yticks(range(len(top10)))
axes[1, 1].set_yticklabels([f"#{row['rank']}: {row['peptide_sequence'][:15]}..."
                             for _, row in top10.iterrows()], fontsize=9)
axes[1, 1].set_xlabel('Binding Affinity (kcal/mol)', fontsize=11)
axes[1, 1].set_title('Top 10 Peptides in Panel', fontweight='bold', fontsize=12)
axes[1, 1].axvline(-10, color='darkred', linestyle='--', alpha=0.5)
axes[1, 1].invert_yaxis()
axes[1, 1].grid(True, alpha=0.3, axis='x')

plt.tight_layout()
viz_file = 'docking_results/plots/27_peptide_panel_visualization.png'
plt.savefig(viz_file, dpi=300, bbox_inches='tight')
print(f"✓ Saved visualization to: {viz_file}")
plt.close()

print("\n" + "="*80)
print("PANEL CREATION COMPLETE!")
print("="*80)
print("\nGenerated files:")
print("  1. 27_peptide_panel.csv - Full panel with all details")
print("  2. 27_peptide_panel_synthesis_ready.csv - Synthesis-ready format")
print("  3. 27_peptide_panel_report.txt - Detailed text report")
print("  4. plots/27_peptide_panel_visualization.png - Visual summary")
print("\nNext: Review the panel and proceed with experimental validation!")
