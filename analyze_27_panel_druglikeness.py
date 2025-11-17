#!/usr/bin/env python3
"""
Drug-Likeness Analysis for 27-Peptide Panel
Comprehensive ADMET and druglikeness assessment
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Amino acid properties
AA_PROPERTIES = {
    'Ala': {'MW': 89.1, 'charge': 0, 'hydrophobic': 1.8, 'polar': False, 'Hbond_donors': 0, 'Hbond_acceptors': 1},
    'Arg': {'MW': 174.2, 'charge': 1, 'hydrophobic': -4.5, 'polar': True, 'Hbond_donors': 4, 'Hbond_acceptors': 1},
    'Asn': {'MW': 132.1, 'charge': 0, 'hydrophobic': -3.5, 'polar': True, 'Hbond_donors': 2, 'Hbond_acceptors': 2},
    'Asp': {'MW': 133.1, 'charge': -1, 'hydrophobic': -3.5, 'polar': True, 'Hbond_donors': 1, 'Hbond_acceptors': 3},
    'Cys': {'MW': 121.2, 'charge': 0, 'hydrophobic': 2.5, 'polar': True, 'Hbond_donors': 1, 'Hbond_acceptors': 1},
    'Gln': {'MW': 146.1, 'charge': 0, 'hydrophobic': -3.5, 'polar': True, 'Hbond_donors': 2, 'Hbond_acceptors': 2},
    'Glu': {'MW': 147.1, 'charge': -1, 'hydrophobic': -3.5, 'polar': True, 'Hbond_donors': 1, 'Hbond_acceptors': 3},
    'Gly': {'MW': 75.1, 'charge': 0, 'hydrophobic': -0.4, 'polar': False, 'Hbond_donors': 0, 'Hbond_acceptors': 1},
    'His': {'MW': 155.2, 'charge': 0, 'hydrophobic': -3.2, 'polar': True, 'Hbond_donors': 1, 'Hbond_acceptors': 2},
    'Ile': {'MW': 131.2, 'charge': 0, 'hydrophobic': 4.5, 'polar': False, 'Hbond_donors': 0, 'Hbond_acceptors': 1},
    'Leu': {'MW': 131.2, 'charge': 0, 'hydrophobic': 3.8, 'polar': False, 'Hbond_donors': 0, 'Hbond_acceptors': 1},
    'Lys': {'MW': 146.2, 'charge': 1, 'hydrophobic': -3.9, 'polar': True, 'Hbond_donors': 2, 'Hbond_acceptors': 1},
    'Met': {'MW': 149.2, 'charge': 0, 'hydrophobic': 1.9, 'polar': False, 'Hbond_donors': 0, 'Hbond_acceptors': 1},
    'Phe': {'MW': 165.2, 'charge': 0, 'hydrophobic': 2.8, 'polar': False, 'Hbond_donors': 0, 'Hbond_acceptors': 1},
    'Pro': {'MW': 115.1, 'charge': 0, 'hydrophobic': -1.6, 'polar': False, 'Hbond_donors': 0, 'Hbond_acceptors': 1},
    'Ser': {'MW': 105.1, 'charge': 0, 'hydrophobic': -0.8, 'polar': True, 'Hbond_donors': 1, 'Hbond_acceptors': 2},
    'Thr': {'MW': 119.1, 'charge': 0, 'hydrophobic': -0.7, 'polar': True, 'Hbond_donors': 1, 'Hbond_acceptors': 2},
    'Trp': {'MW': 204.2, 'charge': 0, 'hydrophobic': -0.9, 'polar': True, 'Hbond_donors': 1, 'Hbond_acceptors': 1},
    'Tyr': {'MW': 181.2, 'charge': 0, 'hydrophobic': -1.3, 'polar': True, 'Hbond_donors': 1, 'Hbond_acceptors': 2},
    'Val': {'MW': 117.1, 'charge': 0, 'hydrophobic': 4.2, 'polar': False, 'Hbond_donors': 0, 'Hbond_acceptors': 1},
}


def parse_3letter_sequence(sequence):
    """Parse 3-letter amino acid sequence"""
    import re
    aa_codes = re.findall(r'[A-Z][a-z]{2}', sequence)
    return aa_codes


def calculate_properties(sequence):
    """Calculate comprehensive molecular properties for a peptide"""
    aa_list = parse_3letter_sequence(sequence)

    if not aa_list:
        return None

    # Molecular weight (subtract water for peptide bonds)
    total_mw = sum(AA_PROPERTIES.get(aa, {}).get('MW', 0) for aa in aa_list)
    total_mw -= 18 * (len(aa_list) - 1)

    # Net charge at pH 7
    total_charge = sum(AA_PROPERTIES.get(aa, {}).get('charge', 0) for aa in aa_list)

    # Hydrophobicity (GRAVY score)
    hydrophobicity = np.mean([AA_PROPERTIES.get(aa, {}).get('hydrophobic', 0) for aa in aa_list])

    # Polar ratio
    polar_count = sum(1 for aa in aa_list if AA_PROPERTIES.get(aa, {}).get('polar', False))
    polar_ratio = polar_count / len(aa_list) if aa_list else 0

    # H-bond donors and acceptors
    hbond_donors = sum(AA_PROPERTIES.get(aa, {}).get('Hbond_donors', 0) for aa in aa_list)
    hbond_acceptors = sum(AA_PROPERTIES.get(aa, {}).get('Hbond_acceptors', 0) for aa in aa_list)

    # Instability index (simplified)
    instability_score = 0
    for i in range(len(aa_list) - 1):
        if aa_list[i] in ['Asp', 'Glu'] and aa_list[i+1] == 'Pro':
            instability_score += 15
        if aa_list[i] == 'Cys':
            instability_score -= 5  # Cys can form disulfide bonds (stabilizing)

    # Aromatic residues (important for binding)
    aromatic_count = sum(1 for aa in aa_list if aa in ['Phe', 'Trp', 'Tyr'])
    aromatic_ratio = aromatic_count / len(aa_list) if aa_list else 0

    return {
        'length': len(aa_list),
        'molecular_weight': total_mw,
        'net_charge': total_charge,
        'hydrophobicity': hydrophobicity,
        'polar_ratio': polar_ratio,
        'hbond_donors': hbond_donors,
        'hbond_acceptors': hbond_acceptors,
        'aromatic_ratio': aromatic_ratio,
        'instability_score': instability_score,
        'amino_acids': aa_list
    }


def assess_druglikeness(properties):
    """Comprehensive drug-likeness assessment for peptides"""
    issues = []
    warnings = []
    score = 100

    # Molecular Weight Assessment
    mw = properties['molecular_weight']
    if mw > 1200:
        issues.append("MW > 1200 Da - Very poor oral bioavailability expected")
        score -= 30
    elif mw > 1000:
        warnings.append("MW > 1000 Da - Poor oral bioavailability likely")
        score -= 20
    elif mw > 800:
        warnings.append("MW > 800 Da - Consider IV/SC administration")
        score -= 10
    elif 600 <= mw <= 800:
        score += 10  # Good MW range for peptide therapeutics

    # Charge Assessment
    charge = abs(properties['net_charge'])
    if charge > 4:
        issues.append(f"Very high net charge ({properties['net_charge']}) - Major membrane permeability issues")
        score -= 25
    elif charge > 3:
        warnings.append(f"High net charge ({properties['net_charge']}) - Reduced membrane permeability")
        score -= 15
    elif charge == 0:
        score += 5  # Neutral peptides often have better permeability

    # Hydrophobicity Assessment (GRAVY score)
    hydro = properties['hydrophobicity']
    if hydro > 3:
        issues.append("Extremely hydrophobic - Major solubility issues expected")
        score -= 20
    elif hydro > 2:
        warnings.append("Very hydrophobic - Solubility concerns")
        score -= 10
    elif hydro < -3:
        warnings.append("Very hydrophilic - Poor membrane permeability likely")
        score -= 10
    elif -1 <= hydro <= 1:
        score += 10  # Balanced hydrophobicity

    # H-bond Assessment
    hbond_total = properties['hbond_donors'] + properties['hbond_acceptors']
    if hbond_total > 20:
        warnings.append(f"High H-bond count ({hbond_total}) - May affect permeability")
        score -= 10

    # Polar Ratio
    if properties['polar_ratio'] > 0.8:
        warnings.append("High polar content - Stability concerns")
        score -= 10

    # Instability Index
    if properties['instability_score'] > 40:
        warnings.append("High instability score - May degrade rapidly")
        score -= 15
    elif properties['instability_score'] < 10:
        score += 5

    # Aromatic Content (good for binding)
    if properties['aromatic_ratio'] > 0.5:
        score += 10  # High aromatic content often correlates with good binding
    elif properties['aromatic_ratio'] < 0.1:
        warnings.append("Low aromatic content - May affect binding")

    # Length Assessment
    length = properties['length']
    if 6 <= length <= 10:
        score += 15  # Ideal length for peptide drugs
    elif length > 15:
        warnings.append(f"Long peptide ({length} AA) - Synthesis and delivery challenges")
        score -= 10

    # Determine suitability
    suitable_for = []
    if score >= 80:
        suitable_for.append("Excellent drug candidate")
    if score >= 60:
        suitable_for.append("Parenteral administration")
    if mw < 800 and charge <= 2:
        suitable_for.append("Potential oral delivery (with modifications)")
    if properties['aromatic_ratio'] > 0.3:
        suitable_for.append("Good binding characteristics")

    return {
        'druglikeness_score': max(0, min(100, score)),
        'issues': issues,
        'warnings': warnings,
        'suitable_for': suitable_for
    }


print("="*80)
print("27-PEPTIDE PANEL: COMPREHENSIVE DRUG-LIKENESS ANALYSIS")
print("="*80)

# Load the panel
panel_df = pd.read_csv('docking_results/27_peptide_panel_synthesis_ready.csv')
print(f"\nAnalyzing {len(panel_df)} peptides...")

# Analyze each peptide
results = []
for idx, row in panel_df.iterrows():
    props = calculate_properties(row['Sequence'])

    if props is None:
        continue

    druglike = assess_druglikeness(props)

    results.append({
        'Panel_ID': row['Panel_ID'],
        'Sequence': row['Sequence'],
        'Target_Protease': row['Target_Protease'],
        'Binding_Affinity': row['Predicted_Affinity_kcal_mol'],
        'Source_Model': row['Source_Model'],
        'Length': props['length'],
        'MW_Da': round(props['molecular_weight'], 1),
        'Net_Charge': props['net_charge'],
        'Hydrophobicity_GRAVY': round(props['hydrophobicity'], 2),
        'Polar_Ratio': round(props['polar_ratio'], 2),
        'HBond_Donors': props['hbond_donors'],
        'HBond_Acceptors': props['hbond_acceptors'],
        'Aromatic_Ratio': round(props['aromatic_ratio'], 2),
        'Instability_Score': round(props['instability_score'], 1),
        'Druglikeness_Score': druglike['druglikeness_score'],
        'Issues': '; '.join(druglike['issues']) if druglike['issues'] else 'None',
        'Warnings': '; '.join(druglike['warnings']) if druglike['warnings'] else 'None',
        'Suitable_For': '; '.join(druglike['suitable_for']) if druglike['suitable_for'] else 'Needs optimization'
    })

results_df = pd.DataFrame(results)

# Calculate combined score (binding + druglikeness)
results_df['Combined_Score'] = (-results_df['Binding_Affinity'] * 10) + results_df['Druglikeness_Score']

# Save results
output_file = 'docking_results/27_panel_druglikeness_analysis.csv'
results_df.to_csv(output_file, index=False)
print(f"✓ Saved detailed results to: {output_file}")

# ============================================
# SUMMARY STATISTICS
# ============================================
print("\n" + "="*80)
print("PROPERTY RANGES")
print("="*80)
print(f"Molecular Weight: {results_df['MW_Da'].min():.1f} - {results_df['MW_Da'].max():.1f} Da")
print(f"Net Charge: {results_df['Net_Charge'].min()} to {results_df['Net_Charge'].max()}")
print(f"Hydrophobicity (GRAVY): {results_df['Hydrophobicity_GRAVY'].min():.2f} to {results_df['Hydrophobicity_GRAVY'].max():.2f}")
print(f"Druglikeness Score: {results_df['Druglikeness_Score'].min():.0f} - {results_df['Druglikeness_Score'].max():.0f}")
print(f"Mean Druglikeness: {results_df['Druglikeness_Score'].mean():.1f}/100")

# ============================================
# DRUGLIKENESS CATEGORIES
# ============================================
print("\n" + "="*80)
print("DRUGLIKENESS CATEGORIES")
print("="*80)

excellent = (results_df['Druglikeness_Score'] >= 80).sum()
good = ((results_df['Druglikeness_Score'] >= 60) & (results_df['Druglikeness_Score'] < 80)).sum()
moderate = ((results_df['Druglikeness_Score'] >= 40) & (results_df['Druglikeness_Score'] < 60)).sum()
poor = (results_df['Druglikeness_Score'] < 40).sum()

print(f"Excellent (≥80): {excellent} peptides ({100*excellent/len(results_df):.1f}%)")
print(f"Good (60-79): {good} peptides ({100*good/len(results_df):.1f}%)")
print(f"Moderate (40-59): {moderate} peptides ({100*moderate/len(results_df):.1f}%)")
print(f"Poor (<40): {poor} peptides ({100*poor/len(results_df):.1f}%)")

# ============================================
# TOP CANDIDATES
# ============================================
print("\n" + "="*80)
print("TOP 10 CANDIDATES (Combined: Binding Affinity + Druglikeness)")
print("="*80)

top10 = results_df.nlargest(10, 'Combined_Score')
print(f"\n{'ID':<4} {'Affinity':>9} {'Drug':>5} {'Comb':>6} {'MW':>7} {'Charge':>7} {'Target':<40}")
print("-"*90)
for _, row in top10.iterrows():
    print(f"{row['Panel_ID']:<4} {row['Binding_Affinity']:>9.3f} {row['Druglikeness_Score']:>5.0f} {row['Combined_Score']:>6.1f} {row['MW_Da']:>7.1f} {row['Net_Charge']:>7.0f} {row['Target_Protease']:<40}")

# ============================================
# BEST BINDERS WITH GOOD DRUGLIKENESS
# ============================================
print("\n" + "="*80)
print("BEST BINDERS WITH DRUGLIKENESS ≥60")
print("="*80)

best_viable = results_df[(results_df['Binding_Affinity'] < -8) & (results_df['Druglikeness_Score'] >= 60)].sort_values('Binding_Affinity')
print(f"\nFound {len(best_viable)} strong binders with good druglikeness:\n")
print(f"{'ID':<4} {'Sequence':<35} {'Target':<40} {'Affinity':>9} {'Drug':>5}")
print("-"*100)
for _, row in best_viable.iterrows():
    print(f"{row['Panel_ID']:<4} {row['Sequence']:<35} {row['Target_Protease']:<40} {row['Binding_Affinity']:>9.3f} {row['Druglikeness_Score']:>5.0f}")

# ============================================
# RECOMMENDED FOR SYNTHESIS
# ============================================
print("\n" + "="*80)
print("RECOMMENDED FOR SYNTHESIS (Top 7)")
print("="*80)

# Selection criteria: Combined score, prioritizing excellent binders
synthesis_candidates = results_df.nlargest(7, 'Combined_Score')

print(f"\n{'Priority':<9} {'ID':<4} {'Sequence':<35} {'Target':<25} {'Affinity':>9} {'Drug':>5}")
print("-"*95)
for priority, (_, row) in enumerate(synthesis_candidates.iterrows(), 1):
    print(f"{priority:<9} {row['Panel_ID']:<4} {row['Sequence']:<35} {row['Target_Protease'][:25]:<25} {row['Binding_Affinity']:>9.3f} {row['Druglikeness_Score']:>5.0f}")

synthesis_file = 'docking_results/recommended_for_synthesis.csv'
synthesis_candidates.to_csv(synthesis_file, index=False)
print(f"\n✓ Synthesis recommendations saved to: {synthesis_file}")

# ============================================
# VISUALIZATIONS
# ============================================
print("\n" + "="*80)
print("GENERATING VISUALIZATIONS")
print("="*80)

output_dir = Path('docking_results/plots')
output_dir.mkdir(exist_ok=True)

fig, axes = plt.subplots(2, 3, figsize=(20, 12))

# Plot 1: Druglikeness distribution
axes[0, 0].hist(results_df['Druglikeness_Score'], bins=15, color='steelblue', edgecolor='black', alpha=0.7)
axes[0, 0].axvline(results_df['Druglikeness_Score'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {results_df["Druglikeness_Score"].mean():.1f}')
axes[0, 0].set_xlabel('Druglikeness Score', fontsize=11)
axes[0, 0].set_ylabel('Frequency', fontsize=11)
axes[0, 0].set_title('Druglikeness Score Distribution', fontweight='bold', fontsize=12)
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# Plot 2: Binding affinity vs druglikeness
scatter = axes[0, 1].scatter(results_df['Binding_Affinity'], results_df['Druglikeness_Score'],
                              c=results_df['Combined_Score'], cmap='viridis', s=100, edgecolor='black', linewidth=1)
axes[0, 1].axhline(60, color='red', linestyle='--', alpha=0.5, label='Druglikeness threshold')
axes[0, 1].axvline(-8, color='orange', linestyle='--', alpha=0.5, label='Strong binding')
axes[0, 1].set_xlabel('Binding Affinity (kcal/mol)', fontsize=11)
axes[0, 1].set_ylabel('Druglikeness Score', fontsize=11)
axes[0, 1].set_title('Binding Affinity vs Druglikeness', fontweight='bold', fontsize=12)
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)
plt.colorbar(scatter, ax=axes[0, 1], label='Combined Score')

# Plot 3: Molecular weight distribution
axes[0, 2].hist(results_df['MW_Da'], bins=15, color='coral', edgecolor='black', alpha=0.7)
axes[0, 2].axvline(800, color='red', linestyle='--', alpha=0.5, label='800 Da threshold')
axes[0, 2].axvline(1000, color='darkred', linestyle='--', alpha=0.5, label='1000 Da threshold')
axes[0, 2].set_xlabel('Molecular Weight (Da)', fontsize=11)
axes[0, 2].set_ylabel('Frequency', fontsize=11)
axes[0, 2].set_title('Molecular Weight Distribution', fontweight='bold', fontsize=12)
axes[0, 2].legend()
axes[0, 2].grid(True, alpha=0.3)

# Plot 4: Hydrophobicity (GRAVY) distribution
axes[1, 0].hist(results_df['Hydrophobicity_GRAVY'], bins=15, color='lightgreen', edgecolor='black', alpha=0.7)
axes[1, 0].axvline(0, color='blue', linestyle='--', alpha=0.5, label='Neutral')
axes[1, 0].set_xlabel('Hydrophobicity (GRAVY score)', fontsize=11)
axes[1, 0].set_ylabel('Frequency', fontsize=11)
axes[1, 0].set_title('Hydrophobicity Distribution', fontweight='bold', fontsize=12)
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

# Plot 5: Net charge distribution
charge_counts = results_df['Net_Charge'].value_counts().sort_index()
axes[1, 1].bar(charge_counts.index, charge_counts.values, color='mediumpurple', edgecolor='black', alpha=0.7)
axes[1, 1].set_xlabel('Net Charge', fontsize=11)
axes[1, 1].set_ylabel('Count', fontsize=11)
axes[1, 1].set_title('Net Charge Distribution', fontweight='bold', fontsize=12)
axes[1, 1].grid(True, alpha=0.3, axis='y')

# Plot 6: Top candidates
top7 = results_df.nlargest(7, 'Combined_Score')
colors_top = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(top7)))
axes[1, 2].barh(range(len(top7)), top7['Combined_Score'], color=colors_top, edgecolor='black')
axes[1, 2].set_yticks(range(len(top7)))
axes[1, 2].set_yticklabels([f"#{int(row['Panel_ID'])}" for _, row in top7.iterrows()], fontsize=10)
axes[1, 2].set_xlabel('Combined Score', fontsize=11)
axes[1, 2].set_title('Top 7 Candidates (Combined Score)', fontweight='bold', fontsize=12)
axes[1, 2].invert_yaxis()
axes[1, 2].grid(True, alpha=0.3, axis='x')

plt.tight_layout()
viz_file = output_dir / '27_panel_druglikeness_analysis.png'
plt.savefig(viz_file, dpi=300, bbox_inches='tight')
print(f"✓ Saved visualization to: {viz_file}")
plt.close()

print("\n" + "="*80)
print("ANALYSIS COMPLETE!")
print("="*80)
print("\nGenerated files:")
print("  1. 27_panel_druglikeness_analysis.csv - Full analysis with all properties")
print("  2. recommended_for_synthesis.csv - Top 7 candidates for synthesis")
print("  3. plots/27_panel_druglikeness_analysis.png - Visual summary")
print("\nNext: Review top candidates and proceed with synthesis planning!")
