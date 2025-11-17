#!/usr/bin/env python3
"""
Design Peptide Inhibitor Modifications
Convert binding peptides into functional protease inhibitors
"""

import pandas as pd
import re
from pathlib import Path

# Protease-specific cleavage sites and inhibitor strategies
PROTEASE_INFO = {
    'Caspase': {
        'class': 'Cysteine protease',
        'cleavage_motif': ['Asp'],  # Cleaves after Asp
        'inhibitor_strategies': [
            'Replace P1 Asp with D-Asp',
            'Add aldehyde warhead at C-terminus',
            'N-terminal acetylation',
            'C-terminal aldehyde (CHO) or fluoromethyl ketone (FMK)',
            'Peptide backbone modification at scissile bond'
        ],
        'recommended_modifications': {
            'N-terminus': 'Acetyl (Ac-)',
            'C-terminus': 'Aldehyde (-CHO) or FMK',
            'backbone': 'Replace scissile bond with ketomethylene or reduced amide'
        }
    },
    'MMP': {
        'class': 'Metalloprotease',
        'cleavage_motif': ['Gly', 'Leu', 'Ala'],
        'inhibitor_strategies': [
            'Add hydroxamate group to chelate zinc',
            'Replace P1\' with non-hydrolyzable residue',
            'Add thiol or carboxylate zinc-binding group',
            'N-methylation to prevent backbone binding',
            'Cyclic peptide to restrict conformation'
        ],
        'recommended_modifications': {
            'N-terminus': 'Free or Acetyl',
            'C-terminus': 'Hydroxamate (-NHOH) or carboxylate',
            'backbone': 'N-methylation or phosphinic acid at scissile bond'
        }
    },
    'Serine protease': {
        'class': 'Serine protease',
        'cleavage_motif': ['Arg', 'Lys', 'Phe'],  # Trypsin-like or chymotrypsin-like
        'inhibitor_strategies': [
            'C-terminal boronic acid or aldehyde',
            'Replace scissile bond with non-cleavable linker',
            'N-terminal blocking (Ac, Boc, etc.)',
            'C-terminal chloromethyl ketone (CMK) or trifluoromethyl ketone',
            'Cyclic peptide'
        ],
        'recommended_modifications': {
            'N-terminus': 'Acetyl (Ac-)',
            'C-terminus': 'Boronic acid, aldehyde, or ketone warhead',
            'backbone': 'Replace P1-P1\' with reduced amide or ketomethylene'
        }
    }
}

# Map specific proteases to classes
PROTEASE_CLASS_MAP = {
    'Caspase-1': 'Caspase', 'Caspase-3': 'Caspase', 'Caspase-6': 'Caspase',
    'Caspase-7': 'Caspase', 'Caspase-8': 'Caspase', 'Caspase-9': 'Caspase',
    'MMP1': 'MMP', 'MMP2': 'MMP', 'MMP7': 'MMP', 'MMP8': 'MMP', 'MMP9': 'MMP', 'MMP12': 'MMP',
    'Neutrophil elastase': 'Serine protease', 'Thrombin': 'Serine protease',
    'Factor IXa': 'Serine protease', 'Factor VIIa': 'Serine protease', 'Factor Xa': 'Serine protease',
    'Plasmin': 'Serine protease', 'Kallikrein': 'Serine protease', 'tPA': 'Serine protease',
    'Urokinase': 'Serine protease', 'Granzyme B': 'Serine protease',
    'Proteinase 3': 'Serine protease', 'Cathepsin G': 'Serine protease',
    'NSP1': 'Cysteine protease', 'NSP2': 'Cysteine protease'
}


def parse_3letter_sequence(sequence):
    """Parse 3-letter amino acid sequence"""
    aa_codes = re.findall(r'[A-Z][a-z]{2}', sequence)
    return aa_codes


def identify_protease_class(protease_name):
    """Identify the protease class from name"""
    for key, pclass in PROTEASE_CLASS_MAP.items():
        if key in protease_name:
            return pclass
    # Default based on name patterns
    if 'Caspase' in protease_name:
        return 'Caspase'
    elif 'MMP' in protease_name:
        return 'MMP'
    else:
        return 'Serine protease'


def find_cleavage_sites(sequence, protease_class):
    """Identify potential cleavage sites in sequence"""
    aa_list = parse_3letter_sequence(sequence)
    cleavage_sites = []

    if protease_class in PROTEASE_INFO:
        motifs = PROTEASE_INFO[protease_class]['cleavage_motif']
        for i, aa in enumerate(aa_list):
            if aa in motifs:
                cleavage_sites.append({
                    'position': i + 1,
                    'residue': aa,
                    'context': f"...{aa_list[max(0,i-1)]}-{aa}↓{aa_list[min(len(aa_list)-1,i+1)]}..."
                })

    return cleavage_sites


def design_inhibitor(sequence, protease_name, protease_class):
    """Design inhibitor modifications for a peptide"""
    modifications = []

    if protease_class not in PROTEASE_INFO:
        protease_class = 'Serine protease'  # Default

    info = PROTEASE_INFO[protease_class]

    # General modifications for all peptides
    modifications.append({
        'type': 'N-terminal',
        'modification': info['recommended_modifications']['N-terminus'],
        'purpose': 'Prevent aminopeptidase degradation',
        'notation': f"{info['recommended_modifications']['N-terminus']}-{sequence}"
    })

    modifications.append({
        'type': 'C-terminal',
        'modification': info['recommended_modifications']['C-terminus'],
        'purpose': 'Act as warhead/prevent carboxypeptidase degradation',
        'notation': f"{sequence}-{info['recommended_modifications']['C-terminus']}"
    })

    # Find cleavage sites
    cleavage_sites = find_cleavage_sites(sequence, protease_class)

    if cleavage_sites:
        # Suggest backbone modification at most likely cleavage site
        primary_site = cleavage_sites[0]
        modifications.append({
            'type': 'Backbone',
            'modification': info['recommended_modifications']['backbone'],
            'purpose': f'Make scissile bond non-cleavable at position {primary_site["position"]}',
            'notation': f'Modified backbone at {primary_site["context"]}'
        })

    # Additional stability modifications
    modifications.append({
        'type': 'Stability',
        'modification': 'Consider D-amino acids at non-critical positions',
        'purpose': 'Increase protease resistance',
        'notation': 'Replace 1-2 L-amino acids with D-forms'
    })

    # Cyclization for conformational constraint
    aa_list = parse_3letter_sequence(sequence)
    if 'Cys' in aa_list or 'Lys' in aa_list or 'Glu' in aa_list:
        modifications.append({
            'type': 'Cyclization',
            'modification': 'Disulfide bridge (Cys-Cys) or lactam bridge (Lys-Glu/Asp)',
            'purpose': 'Conformational constraint & stability',
            'notation': 'Cyclic version via side-chain bridge'
        })

    return modifications, cleavage_sites


def format_inhibitor_notation(sequence, modifications):
    """Create standard inhibitor notation"""
    notations = []

    # Version 1: Full terminal modifications
    n_term = next((m['modification'] for m in modifications if m['type'] == 'N-terminal'), 'Ac')
    c_term = next((m['modification'] for m in modifications if m['type'] == 'C-terminal'), 'NH2')
    notations.append(f"{n_term}-{sequence}-{c_term}")

    # Version 2: With backbone modification
    notations.append(f"{n_term}-{sequence}[ψ]-{c_term}")  # ψ indicates modified backbone

    # Version 3: Cyclic version
    notations.append(f"cyclo({sequence})")

    return notations


print("="*80)
print("PEPTIDE INHIBITOR DESIGN")
print("Converting binding peptides to functional protease inhibitors")
print("="*80)

# Load the 27-peptide panel
panel_df = pd.read_csv('docking_results/27_peptide_panel_synthesis_ready.csv')
print(f"\nDesigning inhibitor modifications for {len(panel_df)} peptides...")

# Design inhibitors
inhibitor_designs = []

for idx, row in panel_df.iterrows():
    sequence = row['Sequence']
    protease_name = row['Target_Protease']

    # Identify protease class
    protease_class = identify_protease_class(protease_name)

    # Design modifications
    modifications, cleavage_sites = design_inhibitor(sequence, protease_name, protease_class)

    # Create notation
    notations = format_inhibitor_notation(sequence, modifications)

    inhibitor_designs.append({
        'Panel_ID': row['Panel_ID'],
        'Original_Sequence': sequence,
        'Target_Protease': protease_name,
        'Protease_Class': protease_class,
        'Binding_Affinity': row['Predicted_Affinity_kcal_mol'],
        'Cleavage_Risk': 'Yes' if cleavage_sites else 'Low',
        'Num_Cleavage_Sites': len(cleavage_sites),
        'Inhibitor_Design_1': notations[0],  # Terminal modifications
        'Inhibitor_Design_2': notations[1],  # + backbone modification
        'Inhibitor_Design_3': notations[2],  # Cyclic
        'N_Terminal_Mod': next((m['modification'] for m in modifications if m['type'] == 'N-terminal'), ''),
        'C_Terminal_Mod': next((m['modification'] for m in modifications if m['type'] == 'C-terminal'), ''),
        'Backbone_Mod': next((m['modification'] for m in modifications if m['type'] == 'Backbone'), 'None'),
        'Additional_Suggestions': '; '.join([m['modification'] for m in modifications if m['type'] in ['Stability', 'Cyclization']])
    })

inhibitor_df = pd.DataFrame(inhibitor_designs)

# Save results
output_file = 'docking_results/27_panel_inhibitor_designs.csv'
inhibitor_df.to_csv(output_file, index=False)
print(f"✓ Saved inhibitor designs to: {output_file}")

# ============================================
# SUMMARY BY PROTEASE CLASS
# ============================================
print("\n" + "="*80)
print("INHIBITOR DESIGN SUMMARY BY PROTEASE CLASS")
print("="*80)

for pclass in inhibitor_df['Protease_Class'].unique():
    class_data = inhibitor_df[inhibitor_df['Protease_Class'] == pclass]
    print(f"\n{pclass} ({len(class_data)} peptides):")
    print(f"  Strategy: {PROTEASE_INFO.get(pclass, {}).get('inhibitor_strategies', ['General'])[0]}")
    print(f"  Peptides at risk of cleavage: {(class_data['Cleavage_Risk'] == 'Yes').sum()}")
    print(f"  Example design: {class_data.iloc[0]['Inhibitor_Design_1']}")

# ============================================
# DETAILED DESIGNS FOR TOP CANDIDATES
# ============================================
print("\n" + "="*80)
print("DETAILED INHIBITOR DESIGNS - TOP 10 BINDERS")
print("="*80)

top10 = inhibitor_df.nsmallest(10, 'Binding_Affinity')

for _, row in top10.iterrows():
    print(f"\n{'─'*80}")
    print(f"Panel #{row['Panel_ID']}: {row['Target_Protease']}")
    print(f"{'─'*80}")
    print(f"Original Sequence: {row['Original_Sequence']}")
    print(f"Binding Affinity: {row['Binding_Affinity']:.3f} kcal/mol")
    print(f"Protease Class: {row['Protease_Class']}")
    print(f"Cleavage Risk: {row['Cleavage_Risk']} ({row['Num_Cleavage_Sites']} potential sites)")
    print(f"\nRecommended Inhibitor Designs:")
    print(f"  Version 1 (Basic):     {row['Inhibitor_Design_1']}")
    print(f"  Version 2 (Enhanced):  {row['Inhibitor_Design_2']}")
    print(f"  Version 3 (Cyclic):    {row['Inhibitor_Design_3']}")
    print(f"\nKey Modifications:")
    print(f"  N-terminus: {row['N_Terminal_Mod']}")
    print(f"  C-terminus: {row['C_Terminal_Mod']}")
    print(f"  Backbone: {row['Backbone_Mod']}")
    if row['Additional_Suggestions']:
        print(f"  Additional: {row['Additional_Suggestions']}")

# ============================================
# SYNTHESIS RECOMMENDATIONS
# ============================================
print("\n" + "="*80)
print("SYNTHESIS RECOMMENDATIONS")
print("="*80)

print("\nFor each peptide, synthesize in this order:")
print("  1. Unmodified peptide (baseline control)")
print("  2. N-Ac + C-NH2 version (basic inhibitor)")
print("  3. Version with warhead (class-specific)")
print("  4. Cyclic version (if feasible)")
print("\nExpected costs per peptide:")
print("  - Unmodified: $100-200")
print("  - N-Ac/C-NH2: $150-250")
print("  - With warhead: $300-500")
print("  - Cyclic: $500-800")

# Create synthesis-ready table
synthesis_df = inhibitor_df[['Panel_ID', 'Original_Sequence', 'Target_Protease',
                               'Binding_Affinity', 'Inhibitor_Design_1',
                               'Inhibitor_Design_2', 'Protease_Class']].copy()
synthesis_df.columns = ['ID', 'Sequence', 'Target', 'Affinity_kcal_mol',
                        'Basic_Inhibitor', 'Enhanced_Inhibitor', 'Class']

# Prioritize top candidates
synthesis_df = synthesis_df.nsmallest(10, 'Affinity_kcal_mol')
synthesis_file = 'docking_results/inhibitor_synthesis_recommendations.csv'
synthesis_df.to_csv(synthesis_file, index=False)
print(f"\n✓ Synthesis recommendations saved to: {synthesis_file}")

# ============================================
# PROTEASE-SPECIFIC GUIDANCE
# ============================================
print("\n" + "="*80)
print("PROTEASE CLASS-SPECIFIC INHIBITOR STRATEGIES")
print("="*80)

for pclass, info in PROTEASE_INFO.items():
    print(f"\n{pclass}:")
    print(f"  Class: {info['class']}")
    print(f"  Key strategies:")
    for i, strategy in enumerate(info['inhibitor_strategies'][:3], 1):
        print(f"    {i}. {strategy}")

print("\n" + "="*80)
print("NEXT STEPS")
print("="*80)
print("\n1. Review inhibitor designs above")
print("2. Select 5-7 top candidates for synthesis")
print("3. For each candidate, order:")
print("   - Unmodified version (control)")
print("   - Basic inhibitor (Ac-peptide-NH2)")
print("   - Enhanced inhibitor (with warhead)")
print("4. Test inhibitory activity (IC50 determination)")
print("5. Compare to unmodified peptide (should be much better)")
print("\n✓ INHIBITOR DESIGNS COMPLETE!")
