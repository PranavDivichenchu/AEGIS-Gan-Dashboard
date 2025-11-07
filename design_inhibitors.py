"""
Convert top peptide substrates into peptidomimetic inhibitors
Modifies the P1-P1' scissile bond to make them uncleavable
"""
import pandas as pd
import numpy as np
from pathlib import Path
import re


class InhibitorDesigner:
    """Design peptidomimetic inhibitors from substrate sequences"""

    MODIFICATIONS = {
        'reduced_amide': {
            'name': 'Reduced Amide (ψ[CH₂NH])',
            'notation': 'ψ[CH2NH]',
            'description': 'Replace C=O with CH₂, most common modification',
            'synthesizable': 'Yes',
            'cost': '$',
            'binding_change': 0.5  # Expected change in binding affinity (kcal/mol)
        },
        'ketomethylene': {
            'name': 'Ketomethylene (ψ[COCH₂])',
            'notation': 'ψ[COCH2]',
            'description': 'Replace NH with O, transition-state analog',
            'synthesizable': 'Yes',
            'cost': '$$',
            'binding_change': -1.0  # Stronger binding expected
        },
        'phosphonate': {
            'name': 'Phosphonate (ψ[P(O)(OH)CH₂])',
            'notation': 'ψ[PO3H2]',
            'description': 'Tetrahedral intermediate analog, very strong binding',
            'synthesizable': 'Yes',
            'cost': '$$$',
            'binding_change': -2.0  # Much stronger binding
        },
        'hydroxyethylene': {
            'name': 'Hydroxyethylene (ψ[CH(OH)CH₂])',
            'notation': 'ψ[CHOHCH2]',
            'description': 'Used in HIV inhibitors, good stability',
            'synthesizable': 'Yes',
            'cost': '$$',
            'binding_change': -1.5
        }
    }

    def __init__(self, docking_results_file):
        self.df = pd.read_csv(docking_results_file)
        self.df = self.df[self.df['status'] == 'success']

    def parse_sequence(self, sequence):
        """Parse 3-letter amino acid sequence into list"""
        aa_codes = re.findall(r'[A-Z][a-z]{2}', sequence)
        return aa_codes

    def design_inhibitor(self, sequence, modification='reduced_amide'):
        """
        Design inhibitor by modifying P1-P1' bond

        Args:
            sequence: 8-mer peptide sequence (3-letter codes)
            modification: Type of peptidomimetic modification

        Returns:
            Dictionary with inhibitor design
        """
        aa_list = self.parse_sequence(sequence)

        if len(aa_list) != 8:
            return None

        # P1 is position 3 (index 3), P1' is position 4 (index 4)
        # Cleavage happens between positions 3 and 4
        P4, P3, P2, P1, P1p, P2p, P3p, P4p = aa_list

        mod_info = self.MODIFICATIONS[modification]

        # Create inhibitor notation
        inhibitor_sequence = f"{P4}-{P3}-{P2}-{P1}{mod_info['notation']}{P1p}-{P2p}-{P3p}-{P4p}"

        # Simplified notation for display
        inhibitor_simple = f"{P4}{P3}{P2}{P1}[*]{P1p}{P2p}{P3p}{P4p}"

        return {
            'original_sequence': sequence,
            'P1': P1,
            'P1_prime': P1p,
            'modification_type': mod_info['name'],
            'modification_notation': mod_info['notation'],
            'inhibitor_sequence': inhibitor_sequence,
            'inhibitor_simple': inhibitor_simple,
            'description': mod_info['description'],
            'synthesizable': mod_info['synthesizable'],
            'estimated_cost': mod_info['cost'],
            'expected_affinity_change': mod_info['binding_change']
        }

    def design_top_inhibitors(self, n=20, output_file="designed_inhibitors.csv"):
        """
        Design inhibitors from top N substrate candidates

        Args:
            n: Number of top substrates to convert
            output_file: Output CSV file
        """
        print("=" * 80)
        print("PEPTIDOMIMETIC INHIBITOR DESIGN")
        print("=" * 80)

        # Get top N candidates by binding affinity
        top_peptides = self.df.nsmallest(n, 'binding_affinity')

        inhibitor_designs = []

        for idx, row in top_peptides.iterrows():
            # Design multiple versions with different modifications
            for mod_type in ['reduced_amide', 'ketomethylene', 'phosphonate', 'hydroxyethylene']:
                design = self.design_inhibitor(row['peptide_sequence'], modification=mod_type)

                if design:
                    # Calculate predicted inhibitor affinity
                    predicted_affinity = row['binding_affinity'] + design['expected_affinity_change']

                    inhibitor_designs.append({
                        'peptide_id': row['peptide_id'],
                        'protease_name': row['protease_name'],
                        'original_substrate': row['peptide_sequence'],
                        'substrate_affinity': row['binding_affinity'],
                        'P1_residue': design['P1'],
                        'P1_prime_residue': design['P1_prime'],
                        'modification_type': design['modification_type'],
                        'modification_notation': design['modification_notation'],
                        'inhibitor_sequence': design['inhibitor_sequence'],
                        'inhibitor_simple': design['inhibitor_simple'],
                        'predicted_affinity': predicted_affinity,
                        'affinity_improvement': design['expected_affinity_change'],
                        'synthesizable': design['synthesizable'],
                        'estimated_cost': design['estimated_cost'],
                        'description': design['description']
                    })

        inhibitor_df = pd.DataFrame(inhibitor_designs)
        inhibitor_df = inhibitor_df.sort_values('predicted_affinity')
        inhibitor_df.to_csv(output_file, index=False)

        print(f"\nDesigned {len(inhibitor_df)} inhibitor variants from {n} top substrates")
        print(f"\nModification types:")
        for mod_type, count in inhibitor_df['modification_type'].value_counts().items():
            print(f"  {mod_type}: {count} designs")

        print(f"\n{'=' * 80}")
        print("TOP 10 INHIBITOR DESIGNS")
        print("=" * 80)
        print(inhibitor_df.head(10)[['inhibitor_simple', 'protease_name', 'predicted_affinity', 'modification_type']].to_string(index=False))

        print(f"\n✓ Inhibitor designs saved to {output_file}")

        return inhibitor_df

    def generate_synthesis_protocol(self, inhibitor_df, output_file="synthesis_protocols.txt"):
        """Generate synthesis recommendations for top inhibitors"""

        with open(output_file, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("INHIBITOR SYNTHESIS RECOMMENDATIONS\n")
            f.write("=" * 80 + "\n\n")

            # Group by protease
            for protease in inhibitor_df['protease_name'].unique():
                f.write(f"\n{'=' * 80}\n")
                f.write(f"PROTEASE: {protease}\n")
                f.write("=" * 80 + "\n\n")

                protease_inhibitors = inhibitor_df[inhibitor_df['protease_name'] == protease].head(3)

                for idx, row in protease_inhibitors.iterrows():
                    f.write(f"Inhibitor {idx+1}:\n")
                    f.write(f"  Sequence: {row['inhibitor_sequence']}\n")
                    f.write(f"  Modification: {row['modification_type']}\n")
                    f.write(f"  Predicted Ki: ~{abs(row['predicted_affinity']):.2f} kcal/mol\n")
                    f.write(f"  Synthesizable: {row['synthesizable']}\n")
                    f.write(f"  Est. Cost: {row['estimated_cost']}\n\n")

                    f.write(f"  Synthesis Strategy:\n")
                    if 'Reduced Amide' in row['modification_type']:
                        f.write(f"    - Use solid-phase peptide synthesis (SPPS)\n")
                        f.write(f"    - Replace Fmoc-P1'-OH with Fmoc-P1'-ψ[CH2NH]-P1-OH building block\n")
                        f.write(f"    - Available from: PolyPeptide Group, Bachem, GenScript\n")
                        f.write(f"    - Estimated cost: $200-500 for 5mg\n")
                    elif 'Ketomethylene' in row['modification_type']:
                        f.write(f"    - SPPS with ketomethylene building block\n")
                        f.write(f"    - Custom synthesis may be required\n")
                        f.write(f"    - Estimated cost: $500-1000 for 5mg\n")
                    elif 'Phosphonate' in row['modification_type']:
                        f.write(f"    - Solution-phase synthesis of phosphonate linkage\n")
                        f.write(f"    - Couple to SPPS-synthesized fragments\n")
                        f.write(f"    - Estimated cost: $1000-2000 for 5mg\n")
                    elif 'Hydroxyethylene' in row['modification_type']:
                        f.write(f"    - Similar to HIV protease inhibitors\n")
                        f.write(f"    - SPPS with hydroxyethylene building block\n")
                        f.write(f"    - Estimated cost: $500-1000 for 5mg\n")

                    f.write(f"\n  In Vitro Testing:\n")
                    f.write(f"    - Fluorogenic substrate assay\n")
                    f.write(f"    - Test IC50 against {protease}\n")
                    f.write(f"    - Test specificity panel (10 related proteases)\n")
                    f.write(f"    - Estimated cost: $2000-5000 per inhibitor\n")
                    f.write(f"\n")

            f.write("\n" + "=" * 80 + "\n")
            f.write("RECOMMENDED VENDORS\n")
            f.write("=" * 80 + "\n")
            f.write("Peptide Synthesis:\n")
            f.write("  - GenScript (USA): https://www.genscript.com/peptide-synthesis.html\n")
            f.write("  - Bachem (Switzerland): https://www.bachem.com\n")
            f.write("  - PolyPeptide Group: https://www.polypeptide.com\n")
            f.write("  - Custom Building Blocks: ChemPep, AAPPTec\n\n")

            f.write("In Vitro Testing:\n")
            f.write("  - BPS Bioscience (protease assay kits)\n")
            f.write("  - Reaction Biology (custom inhibitor profiling)\n")
            f.write("  - Your local university biochemistry core facility\n")

        print(f"✓ Synthesis protocols saved to {output_file}")

    def visualize_modifications(self, output_dir="inhibitor_designs"):
        """Create visualizations of inhibitor designs"""
        import matplotlib.pyplot as plt
        import seaborn as sns

        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)

        # Load inhibitor designs
        inhibitor_df = pd.read_csv("designed_inhibitors.csv")

        # 1. Predicted affinity improvement
        fig, ax = plt.subplots(figsize=(10, 6))

        mod_order = ['Reduced Amide (ψ[CH₂NH])', 'Ketomethylene (ψ[COCH₂])',
                     'Hydroxyethylene (ψ[CH(OH)CH₂])', 'Phosphonate (ψ[P(O)(OH)CH₂])']

        sns.boxplot(data=inhibitor_df, x='modification_type', y='predicted_affinity',
                    order=mod_order, ax=ax)
        ax.set_xlabel('Modification Type')
        ax.set_ylabel('Predicted Binding Affinity (kcal/mol)')
        ax.set_title('Predicted Inhibitor Binding by Modification Type')
        ax.axhline(-8, color='red', linestyle='--', label='Strong binder threshold', alpha=0.5)
        plt.xticks(rotation=45, ha='right')
        plt.legend()
        plt.tight_layout()
        plt.savefig(output_dir / 'modification_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()

        # 2. Substrate vs Inhibitor affinity
        fig, ax = plt.subplots(figsize=(10, 8))

        for mod_type in inhibitor_df['modification_type'].unique():
            mod_data = inhibitor_df[inhibitor_df['modification_type'] == mod_type]
            ax.scatter(mod_data['substrate_affinity'], mod_data['predicted_affinity'],
                      label=mod_type, alpha=0.6, s=50)

        # Diagonal line (no change)
        lim = [min(ax.get_xlim()[0], ax.get_ylim()[0]),
               max(ax.get_xlim()[1], ax.get_ylim()[1])]
        ax.plot(lim, lim, 'k--', alpha=0.3, label='No change')

        ax.set_xlabel('Substrate Binding Affinity (kcal/mol)')
        ax.set_ylabel('Predicted Inhibitor Binding Affinity (kcal/mol)')
        ax.set_title('Substrate → Inhibitor Affinity Change')
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_dir / 'substrate_to_inhibitor.png', dpi=300, bbox_inches='tight')
        plt.close()

        # 3. Best inhibitor per protease
        best_per_protease = inhibitor_df.loc[inhibitor_df.groupby('protease_name')['predicted_affinity'].idxmin()]

        fig, ax = plt.subplots(figsize=(12, 8))

        proteases = best_per_protease['protease_name'].str.split('(').str[0].str.strip()
        affinities = best_per_protease['predicted_affinity']
        modifications = best_per_protease['modification_type']

        colors = {'Reduced Amide (ψ[CH₂NH])': 'blue',
                 'Ketomethylene (ψ[COCH₂])': 'green',
                 'Hydroxyethylene (ψ[CH(OH)CH₂])': 'orange',
                 'Phosphonate (ψ[P(O)(OH)CH₂])': 'red'}

        bar_colors = [colors.get(m, 'gray') for m in modifications]

        ax.barh(range(len(proteases)), affinities, color=bar_colors)
        ax.set_yticks(range(len(proteases)))
        ax.set_yticklabels(proteases, fontsize=8)
        ax.set_xlabel('Predicted Binding Affinity (kcal/mol)')
        ax.set_title('Best Inhibitor Design per Protease')
        ax.axvline(-8, color='red', linestyle='--', alpha=0.5)

        # Legend
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor=color, label=mod) for mod, color in colors.items()]
        ax.legend(handles=legend_elements, bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=7)

        plt.tight_layout()
        plt.savefig(output_dir / 'best_inhibitors_per_protease.png', dpi=300, bbox_inches='tight')
        plt.close()

        print(f"✓ Visualizations saved to {output_dir}/")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Design peptidomimetic inhibitors from substrates')
    parser.add_argument('--results', type=str, required=True, help='Docking results CSV')
    parser.add_argument('--top-n', type=int, default=20, help='Number of top substrates to convert')
    parser.add_argument('--output', type=str, default='designed_inhibitors.csv', help='Output file')

    args = parser.parse_args()

    print("=" * 80)
    print("THERAPEUTIC INHIBITOR DESIGN")
    print("=" * 80)
    print("\nConverting top substrate candidates into peptidomimetic inhibitors...")

    designer = InhibitorDesigner(args.results)
    inhibitor_df = designer.design_top_inhibitors(n=args.top_n, output_file=args.output)
    designer.generate_synthesis_protocol(inhibitor_df)
    designer.visualize_modifications()

    print("\n" + "=" * 80)
    print("INHIBITOR DESIGN COMPLETE!")
    print("=" * 80)
    print("\nOutput files:")
    print("  1. designed_inhibitors.csv - All inhibitor designs")
    print("  2. synthesis_protocols.txt - Synthesis recommendations")
    print("  3. inhibitor_designs/ - Visualization plots")


if __name__ == "__main__":
    main()
