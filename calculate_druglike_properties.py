"""
Calculate drug-like properties for peptide biomarkers
Assesses molecular weight, charge, hydrophobicity, etc.
"""
import pandas as pd
import numpy as np
from pathlib import Path

# Amino acid properties
AA_PROPERTIES = {
    'Ala': {'MW': 89.1, 'charge': 0, 'hydrophobic': 1.8, 'polar': False},
    'Arg': {'MW': 174.2, 'charge': 1, 'hydrophobic': -4.5, 'polar': True},
    'Asn': {'MW': 132.1, 'charge': 0, 'hydrophobic': -3.5, 'polar': True},
    'Asp': {'MW': 133.1, 'charge': -1, 'hydrophobic': -3.5, 'polar': True},
    'Cys': {'MW': 121.2, 'charge': 0, 'hydrophobic': 2.5, 'polar': True},
    'Gln': {'MW': 146.1, 'charge': 0, 'hydrophobic': -3.5, 'polar': True},
    'Glu': {'MW': 147.1, 'charge': -1, 'hydrophobic': -3.5, 'polar': True},
    'Gly': {'MW': 75.1, 'charge': 0, 'hydrophobic': -0.4, 'polar': False},
    'His': {'MW': 155.2, 'charge': 0, 'hydrophobic': -3.2, 'polar': True},
    'Ile': {'MW': 131.2, 'charge': 0, 'hydrophobic': 4.5, 'polar': False},
    'Leu': {'MW': 131.2, 'charge': 0, 'hydrophobic': 3.8, 'polar': False},
    'Lys': {'MW': 146.2, 'charge': 1, 'hydrophobic': -3.9, 'polar': True},
    'Met': {'MW': 149.2, 'charge': 0, 'hydrophobic': 1.9, 'polar': False},
    'Phe': {'MW': 165.2, 'charge': 0, 'hydrophobic': 2.8, 'polar': False},
    'Pro': {'MW': 115.1, 'charge': 0, 'hydrophobic': -1.6, 'polar': False},
    'Ser': {'MW': 105.1, 'charge': 0, 'hydrophobic': -0.8, 'polar': True},
    'Thr': {'MW': 119.1, 'charge': 0, 'hydrophobic': -0.7, 'polar': True},
    'Trp': {'MW': 204.2, 'charge': 0, 'hydrophobic': -0.9, 'polar': True},
    'Tyr': {'MW': 181.2, 'charge': 0, 'hydrophobic': -1.3, 'polar': True},
    'Val': {'MW': 117.1, 'charge': 0, 'hydrophobic': 4.2, 'polar': False},
}


def parse_3letter_sequence(sequence):
    """Parse 3-letter amino acid sequence"""
    import re
    aa_codes = re.findall(r'[A-Z][a-z]{2}', sequence)
    return aa_codes


def calculate_properties(sequence):
    """Calculate molecular properties for a peptide"""
    aa_list = parse_3letter_sequence(sequence)

    if not aa_list:
        return None

    total_mw = sum(AA_PROPERTIES.get(aa, {}).get('MW', 0) for aa in aa_list)
    # Subtract water for peptide bonds
    total_mw -= 18 * (len(aa_list) - 1)

    total_charge = sum(AA_PROPERTIES.get(aa, {}).get('charge', 0) for aa in aa_list)

    hydrophobicity = np.mean([AA_PROPERTIES.get(aa, {}).get('hydrophobic', 0) for aa in aa_list])

    polar_count = sum(1 for aa in aa_list if AA_PROPERTIES.get(aa, {}).get('polar', False))
    polar_ratio = polar_count / len(aa_list) if aa_list else 0

    return {
        'length': len(aa_list),
        'molecular_weight': total_mw,
        'net_charge': total_charge,
        'hydrophobicity': hydrophobicity,
        'polar_ratio': polar_ratio,
        'amino_acids': aa_list
    }


def assess_druglikeness(properties):
    """Assess if peptide meets drug-like criteria"""
    issues = []
    score = 100

    # Peptide drug guidelines (more lenient than Lipinski's Rule of 5)
    if properties['molecular_weight'] > 1000:
        issues.append("MW > 1000 Da (may have poor oral bioavailability)")
        score -= 20
    elif properties['molecular_weight'] > 800:
        issues.append("MW > 800 Da (borderline for oral delivery)")
        score -= 10

    if abs(properties['net_charge']) > 3:
        issues.append(f"High net charge ({properties['net_charge']}) - may affect membrane permeability")
        score -= 15

    if properties['hydrophobicity'] > 3:
        issues.append("Very hydrophobic - may have solubility issues")
        score -= 15
    elif properties['hydrophobicity'] < -3:
        issues.append("Very hydrophilic - may have poor membrane permeability")
        score -= 10

    if properties['polar_ratio'] > 0.8:
        issues.append("High polar residue content - may affect stability")
        score -= 10

    # Positive attributes
    if 6 <= properties['length'] <= 12:
        score += 10  # Ideal length for peptide drugs

    if 400 <= properties['molecular_weight'] <= 800:
        score += 10  # Good MW range

    return {
        'druglikeness_score': max(0, score),
        'issues': issues,
        'suitable_for': []
    }


def analyze_results(results_file, output_file="peptide_properties.csv"):
    """Analyze drug-like properties for all peptides"""
    print("=" * 80)
    print("DRUG-LIKE PROPERTIES ANALYSIS")
    print("=" * 80)

    df = pd.read_csv(results_file)
    df = df[df['status'] == 'success']

    results = []
    for idx, row in df.iterrows():
        props = calculate_properties(row['peptide_sequence'])

        if props is None:
            continue

        druglike = assess_druglikeness(props)

        results.append({
            'peptide_id': row['peptide_id'],
            'protease_name': row['protease_name'],
            'sequence': row['peptide_sequence'],
            'binding_affinity': row['binding_affinity'],
            'length': props['length'],
            'molecular_weight': props['molecular_weight'],
            'net_charge': props['net_charge'],
            'hydrophobicity': props['hydrophobicity'],
            'polar_ratio': props['polar_ratio'],
            'druglikeness_score': druglike['druglikeness_score'],
            'issues': '; '.join(druglike['issues']) if druglike['issues'] else 'None'
        })

    results_df = pd.DataFrame(results)
    results_df.to_csv(output_file, index=False)

    # Summary statistics
    print(f"\nAnalyzed {len(results_df)} peptides")
    print(f"\nProperty Ranges:")
    print(f"  Molecular Weight: {results_df['molecular_weight'].min():.1f} - {results_df['molecular_weight'].max():.1f} Da")
    print(f"  Net Charge: {results_df['net_charge'].min():.1f} to {results_df['net_charge'].max():.1f}")
    print(f"  Hydrophobicity: {results_df['hydrophobicity'].min():.2f} to {results_df['hydrophobicity'].max():.2f}")
    print(f"  Mean Druglikeness Score: {results_df['druglikeness_score'].mean():.1f}/100")

    # Top candidates (best binding + good druglikeness)
    results_df['combined_score'] = -results_df['binding_affinity'] + results_df['druglikeness_score']/10

    print(f"\n{'=' * 80}")
    print("TOP 10 CANDIDATES (Binding Affinity + Druglikeness)")
    print("=" * 80)
    top10 = results_df.nsmallest(10, 'binding_affinity')
    print(top10[['peptide_id', 'protease_name', 'binding_affinity', 'druglikeness_score', 'molecular_weight', 'issues']].to_string(index=False))

    print(f"\n✓ Results saved to {output_file}")

    return results_df


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Calculate drug-like properties')
    parser.add_argument('--results', type=str, required=True, help='Docking results CSV')
    parser.add_argument('--output', type=str, default='peptide_properties.csv', help='Output file')

    args = parser.parse_args()

    analyze_results(args.results, args.output)


if __name__ == "__main__":
    main()
