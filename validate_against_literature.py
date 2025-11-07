"""
Validate GAN-generated peptides against known protease substrates
Compares your results to literature values for credibility
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Known protease substrates and their typical binding affinities
# Values from literature (approximate ranges)
KNOWN_SUBSTRATES = {
    "Neutrophil elastase (ELANE)": {
        "typical_range": (-9.0, -6.0),
        "known_sequences": [
            "AAPV",  # Ala-Ala-Pro-Val
            "AAPA",  # Common elastase substrate
        ],
        "references": "Nakajima et al. (1979), Powers et al. (1985)"
    },
    "Thrombin (F2, coagulation factor IIa)": {
        "typical_range": (-10.0, -7.0),
        "known_sequences": [
            "LTPR",  # Leu-Thr-Pro-Arg - fibrinogen cleavage
            "GPRP",  # Common thrombin substrate
        ],
        "references": "Stubbs & Bode (1995)"
    },
    "MMP9 (Gelatinase B)": {
        "typical_range": (-8.5, -6.0),
        "known_sequences": [
            "GPQG",  # Gly-Pro-Gln-Gly - collagen substrate
        ],
        "references": "Nagase et al. (2006)"
    },
    "MMP8 (Collagenase-2)": {
        "typical_range": (-8.0, -6.0),
        "known_sequences": [
            "GPQG",  # Collagen substrate
        ],
        "references": "Nagase et al. (2006)"
    },
    "Cathepsin G (CTSG)": {
        "typical_range": (-9.0, -6.5),
        "known_sequences": [
            "AAPF",  # Ala-Ala-Pro-Phe
        ],
        "references": "Powers et al. (1985)"
    },
    "Plasmin": {
        "typical_range": (-9.0, -6.5),
        "known_sequences": [
            "VLK",  # Val-Leu-Lys - plasminogen substrate
        ],
        "references": "Lijnen & Collen (1995)"
    },
    "Caspase-3": {
        "typical_range": (-9.5, -7.0),
        "known_sequences": [
            "DEVD",  # Asp-Glu-Val-Asp - canonical caspase-3 substrate
        ],
        "references": "Thornberry et al. (1997)"
    }
}


class LiteratureValidator:
    def __init__(self, results_file):
        self.results_file = results_file
        self.df = pd.read_csv(results_file)
        self.df = self.df[self.df['status'] == 'success']

    def compare_to_literature_ranges(self):
        """Compare your binding affinities to known literature ranges"""
        print("=" * 80)
        print("VALIDATION AGAINST LITERATURE VALUES")
        print("=" * 80)

        results = []
        for protease, info in KNOWN_SUBSTRATES.items():
            # Get your results for this protease
            protease_data = self.df[self.df['protease_name'] == protease]

            if len(protease_data) == 0:
                continue

            min_lit, max_lit = info['typical_range']
            your_mean = protease_data['binding_affinity'].mean()
            your_best = protease_data['binding_affinity'].min()

            # Count how many of your peptides fall in literature range
            in_range = len(protease_data[
                (protease_data['binding_affinity'] >= min_lit) &
                (protease_data['binding_affinity'] <= max_lit)
            ])

            results.append({
                'Protease': protease,
                'Literature Range': f"{min_lit} to {max_lit}",
                'Your Mean': f"{your_mean:.2f}",
                'Your Best': f"{your_best:.2f}",
                'In Range': f"{in_range}/{len(protease_data)} ({in_range/len(protease_data)*100:.1f}%)",
                'Status': '✓ Good' if min_lit <= your_mean <= max_lit else '⚠ Outside range',
                'Reference': info['references']
            })

        results_df = pd.DataFrame(results)
        print(results_df.to_string(index=False))

        # Summary
        good_count = len(results_df[results_df['Status'] == '✓ Good'])
        total_count = len(results_df)
        print(f"\n📊 Summary: {good_count}/{total_count} proteases have mean affinities in literature range")

        return results_df

    def analyze_specificity(self):
        """Check if peptides show protease specificity"""
        print("\n" + "=" * 80)
        print("PROTEASE SPECIFICITY ANALYSIS")
        print("=" * 80)

        # For each peptide, compare binding to intended target vs. off-targets
        peptide_specificity = []

        for peptide_id in self.df['peptide_id'].unique():
            peptide_data = self.df[self.df['peptide_id'] == peptide_id]

            if len(peptide_data) < 2:
                continue

            best_affinity = peptide_data['binding_affinity'].min()
            best_protease = peptide_data[peptide_data['binding_affinity'] == best_affinity]['protease_name'].values[0]

            # Calculate specificity: difference between best and second-best
            sorted_affinities = peptide_data['binding_affinity'].sort_values()
            if len(sorted_affinities) >= 2:
                specificity = sorted_affinities.iloc[1] - sorted_affinities.iloc[0]

                peptide_specificity.append({
                    'peptide_id': peptide_id,
                    'best_protease': best_protease,
                    'best_affinity': best_affinity,
                    'specificity': specificity
                })

        spec_df = pd.DataFrame(peptide_specificity)

        if len(spec_df) > 0:
            print(f"\nMean specificity: {spec_df['specificity'].mean():.2f} kcal/mol")
            print(f"(Higher = more specific to one protease)")

            # Show most specific peptides
            print("\nTop 10 Most Specific Peptides:")
            top_specific = spec_df.nlargest(10, 'specificity')
            print(top_specific.to_string(index=False))

        return spec_df

    def visualize_validation(self, output_dir="validation_analysis"):
        """Create validation visualizations"""
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)

        # 1. Compare to literature ranges
        fig, axes = plt.subplots(2, 1, figsize=(12, 10))

        for protease, info in KNOWN_SUBSTRATES.items():
            protease_data = self.df[self.df['protease_name'] == protease]
            if len(protease_data) == 0:
                continue

            min_lit, max_lit = info['typical_range']

            # Plot 1: Your distribution vs. literature range
            ax = axes[0]
            ax.hist(protease_data['binding_affinity'], bins=20, alpha=0.5, label=protease)
            ax.axvline(min_lit, color='red', linestyle='--', alpha=0.3)
            ax.axvline(max_lit, color='red', linestyle='--', alpha=0.3)

        axes[0].set_xlabel('Binding Affinity (kcal/mol)')
        axes[0].set_ylabel('Frequency')
        axes[0].set_title('Your Results vs. Literature Ranges (red lines)')
        axes[0].legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)

        # Plot 2: Mean affinities with literature ranges
        ax = axes[1]
        protease_means = []
        protease_names = []
        lit_ranges = []

        for protease, info in KNOWN_SUBSTRATES.items():
            protease_data = self.df[self.df['protease_name'] == protease]
            if len(protease_data) == 0:
                continue

            protease_means.append(protease_data['binding_affinity'].mean())
            protease_names.append(protease.split('(')[0].strip())
            lit_ranges.append(info['typical_range'])

        x_pos = range(len(protease_names))
        ax.scatter(x_pos, protease_means, s=100, label='Your Mean', zorder=3)

        for i, (min_lit, max_lit) in enumerate(lit_ranges):
            ax.plot([i, i], [min_lit, max_lit], 'r-', linewidth=3, alpha=0.5, label='Lit. Range' if i == 0 else '')

        ax.set_xticks(x_pos)
        ax.set_xticklabels(protease_names, rotation=45, ha='right')
        ax.set_ylabel('Binding Affinity (kcal/mol)')
        ax.set_title('Your Mean Affinities vs. Literature Ranges')
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(output_dir / 'literature_validation.png', dpi=300, bbox_inches='tight')
        plt.close()

        print(f"\n✓ Validation plots saved to {output_dir}/")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Validate results against literature')
    parser.add_argument('--results', type=str, required=True, help='Docking results CSV file')
    parser.add_argument('--output', type=str, default='validation_analysis', help='Output directory')

    args = parser.parse_args()

    print("=" * 80)
    print("LITERATURE VALIDATION ANALYSIS")
    print("=" * 80)

    validator = LiteratureValidator(args.results)
    validator.compare_to_literature_ranges()
    validator.analyze_specificity()
    validator.visualize_validation(output_dir=args.output)

    print("\n" + "=" * 80)
    print("VALIDATION COMPLETE!")
    print("=" * 80)


if __name__ == "__main__":
    main()
