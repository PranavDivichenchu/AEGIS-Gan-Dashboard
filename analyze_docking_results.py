"""
Analyze and visualize molecular docking results
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Dict, List
import json


class DockingAnalyzer:
    """Analyze and rank docking results"""

    def __init__(self, results_csv: str, output_dir: str = "docking_analysis"):
        self.results_csv = results_csv
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Load results
        self.df = pd.read_csv(results_csv)
        self.df = self.df[self.df['status'] == 'success']  # Only successful dockings

        print(f"Loaded {len(self.df)} successful docking results")

    def rank_by_affinity(self, ascending: bool = True) -> pd.DataFrame:
        """
        Rank peptides by binding affinity

        Args:
            ascending: True for most negative (strongest binding) first

        Returns:
            Ranked DataFrame
        """
        ranked = self.df.sort_values('binding_affinity', ascending=ascending)
        ranked['rank'] = range(1, len(ranked) + 1)
        return ranked

    def get_top_binders(self, n: int = 10, per_protease: bool = False) -> pd.DataFrame:
        """
        Get top binding peptides

        Args:
            n: Number of top binders to return
            per_protease: If True, return top n per protease

        Returns:
            DataFrame with top binders
        """
        if per_protease:
            top_binders = []
            for protease in self.df['protease_name'].unique():
                protease_df = self.df[self.df['protease_name'] == protease]
                top = protease_df.nsmallest(n, 'binding_affinity')
                top_binders.append(top)
            return pd.concat(top_binders, ignore_index=True)
        else:
            return self.df.nsmallest(n, 'binding_affinity')

    def calculate_statistics(self) -> Dict:
        """Calculate summary statistics"""
        stats = {
            'total_dockings': len(self.df),
            'unique_proteases': self.df['protease_name'].nunique(),
            'unique_peptides': self.df['peptide_id'].nunique(),
            'mean_affinity': self.df['binding_affinity'].mean(),
            'median_affinity': self.df['binding_affinity'].median(),
            'std_affinity': self.df['binding_affinity'].std(),
            'min_affinity': self.df['binding_affinity'].min(),
            'max_affinity': self.df['binding_affinity'].max(),
            'best_binder': self.df.loc[self.df['binding_affinity'].idxmin()].to_dict()
        }

        # Per-protease statistics
        protease_stats = self.df.groupby('protease_name')['binding_affinity'].agg([
            'count', 'mean', 'median', 'std', 'min', 'max'
        ]).reset_index()

        stats['per_protease'] = protease_stats.to_dict('records')

        return stats

    def plot_affinity_distribution(self):
        """Plot binding affinity distribution"""
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        # Overall distribution
        axes[0].hist(self.df['binding_affinity'], bins=30, edgecolor='black', alpha=0.7)
        axes[0].axvline(self.df['binding_affinity'].mean(), color='red', linestyle='--', label='Mean')
        axes[0].axvline(self.df['binding_affinity'].median(), color='green', linestyle='--', label='Median')
        axes[0].set_xlabel('Binding Affinity (kcal/mol)')
        axes[0].set_ylabel('Frequency')
        axes[0].set_title('Binding Affinity Distribution')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)

        # Box plot
        axes[1].boxplot(self.df['binding_affinity'], vert=True)
        axes[1].set_ylabel('Binding Affinity (kcal/mol)')
        axes[1].set_title('Binding Affinity Box Plot')
        axes[1].grid(True, alpha=0.3)

        plt.tight_layout()
        output_file = self.output_dir / 'affinity_distribution.png'
        plt.savefig(output_file, dpi=300)
        print(f"Saved: {output_file}")
        plt.close()

    def plot_per_protease_comparison(self):
        """Plot binding affinity comparison across proteases"""
        # Calculate mean affinity per protease
        protease_means = self.df.groupby('protease_name')['binding_affinity'].mean().sort_values()

        fig, axes = plt.subplots(2, 1, figsize=(14, 10))

        # Bar plot of means
        axes[0].barh(range(len(protease_means)), protease_means.values, alpha=0.7)
        axes[0].set_yticks(range(len(protease_means)))
        axes[0].set_yticklabels(protease_means.index, fontsize=8)
        axes[0].set_xlabel('Mean Binding Affinity (kcal/mol)')
        axes[0].set_title('Mean Binding Affinity by Protease')
        axes[0].axvline(0, color='black', linestyle='-', linewidth=0.5)
        axes[0].grid(True, alpha=0.3, axis='x')

        # Box plot per protease
        protease_data = [self.df[self.df['protease_name'] == p]['binding_affinity'].values
                         for p in protease_means.index]

        bp = axes[1].boxplot(protease_data, vert=False, labels=protease_means.index, patch_artist=True)
        for patch in bp['boxes']:
            patch.set_facecolor('lightblue')
        axes[1].set_xlabel('Binding Affinity (kcal/mol)')
        axes[1].tick_params(axis='y', labelsize=8)
        axes[1].set_title('Binding Affinity Distribution by Protease')
        axes[1].grid(True, alpha=0.3, axis='x')

        plt.tight_layout()
        output_file = self.output_dir / 'per_protease_comparison.png'
        plt.savefig(output_file, dpi=300)
        print(f"Saved: {output_file}")
        plt.close()

    def plot_top_binders_heatmap(self, top_n: int = 20):
        """Create heatmap of top binders"""
        # Get top binders per protease
        top_binders_list = []
        for protease in self.df['protease_name'].unique():
            protease_df = self.df[self.df['protease_name'] == protease]
            top = protease_df.nsmallest(min(top_n, len(protease_df)), 'binding_affinity')
            top_binders_list.append(top)

        top_binders = pd.concat(top_binders_list, ignore_index=True)

        # Create pivot table for heatmap
        pivot_data = top_binders.pivot_table(
            values='binding_affinity',
            index='protease_name',
            columns='peptide_id',
            aggfunc='min'
        )

        # Plot heatmap
        fig, ax = plt.subplots(figsize=(20, 10))
        sns.heatmap(pivot_data, cmap='RdYlGn_r', center=0,
                    annot=False, fmt='.2f', cbar_kws={'label': 'Binding Affinity (kcal/mol)'},
                    ax=ax)
        ax.set_title(f'Top {top_n} Binders per Protease Heatmap')
        ax.set_xlabel('Peptide ID')
        ax.set_ylabel('Protease')
        plt.xticks(rotation=90, fontsize=6)
        plt.yticks(rotation=0, fontsize=8)
        plt.tight_layout()

        output_file = self.output_dir / 'top_binders_heatmap.png'
        plt.savefig(output_file, dpi=300)
        print(f"Saved: {output_file}")
        plt.close()

    def plot_sequence_analysis(self):
        """Analyze sequence features vs binding affinity"""
        # Add sequence features
        self.df['sequence_length'] = self.df['peptide_sequence'].str.len()

        # Count amino acid composition
        amino_acids = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L',
                       'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']

        for aa in amino_acids:
            self.df[f'count_{aa}'] = self.df['peptide_sequence'].str.count(aa)

        # Plot
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        # Sequence length vs affinity
        axes[0].scatter(self.df['sequence_length'], self.df['binding_affinity'], alpha=0.5)
        axes[0].set_xlabel('Sequence Length')
        axes[0].set_ylabel('Binding Affinity (kcal/mol)')
        axes[0].set_title('Sequence Length vs Binding Affinity')
        axes[0].grid(True, alpha=0.3)

        # Top 5 amino acids correlation
        correlations = []
        for aa in amino_acids:
            corr = self.df[[f'count_{aa}', 'binding_affinity']].corr().iloc[0, 1]
            correlations.append((aa, corr))

        correlations.sort(key=lambda x: abs(x[1]), reverse=True)
        top_aas = correlations[:10]

        aa_names = [x[0] for x in top_aas]
        aa_corrs = [x[1] for x in top_aas]

        colors = ['green' if x < 0 else 'red' for x in aa_corrs]
        axes[1].barh(aa_names, aa_corrs, color=colors, alpha=0.7)
        axes[1].set_xlabel('Correlation with Binding Affinity')
        axes[1].set_ylabel('Amino Acid')
        axes[1].set_title('Top 10 Amino Acids by Correlation\n(Negative = Stronger Binding)')
        axes[1].axvline(0, color='black', linestyle='-', linewidth=0.5)
        axes[1].grid(True, alpha=0.3, axis='x')

        plt.tight_layout()
        output_file = self.output_dir / 'sequence_analysis.png'
        plt.savefig(output_file, dpi=300)
        print(f"Saved: {output_file}")
        plt.close()

    def generate_report(self):
        """Generate comprehensive analysis report"""
        print("\n" + "=" * 80)
        print("DOCKING RESULTS ANALYSIS REPORT")
        print("=" * 80)

        # Calculate statistics
        stats = self.calculate_statistics()

        print(f"\nOVERALL STATISTICS:")
        print(f"  Total successful dockings: {stats['total_dockings']}")
        print(f"  Unique proteases: {stats['unique_proteases']}")
        print(f"  Unique peptides: {stats['unique_peptides']}")
        print(f"\nBINDING AFFINITY:")
        print(f"  Mean: {stats['mean_affinity']:.2f} kcal/mol")
        print(f"  Median: {stats['median_affinity']:.2f} kcal/mol")
        print(f"  Std Dev: {stats['std_affinity']:.2f} kcal/mol")
        print(f"  Range: [{stats['min_affinity']:.2f}, {stats['max_affinity']:.2f}] kcal/mol")

        print(f"\nBEST BINDER:")
        best = stats['best_binder']
        print(f"  Peptide: {best['peptide_id']}")
        print(f"  Sequence: {best['peptide_sequence']}")
        print(f"  Protease: {best['protease_name']}")
        print(f"  Binding Affinity: {best['binding_affinity']:.2f} kcal/mol")

        # Top 10 overall
        print(f"\nTOP 10 OVERALL BINDERS:")
        top10 = self.get_top_binders(n=10)
        for idx, row in top10.iterrows():
            print(f"  {row['peptide_sequence']:10s} -> {row['protease_name']:30s} : {row['binding_affinity']:7.2f} kcal/mol")

        # Top 3 per protease
        print(f"\nTOP 3 BINDERS PER PROTEASE:")
        top_per_protease = self.get_top_binders(n=3, per_protease=True)
        for protease in sorted(top_per_protease['protease_name'].unique()):
            print(f"\n  {protease}:")
            protease_tops = top_per_protease[top_per_protease['protease_name'] == protease]
            for idx, row in protease_tops.iterrows():
                print(f"    {row['peptide_sequence']:10s} : {row['binding_affinity']:7.2f} kcal/mol")

        # Save statistics to JSON
        stats_file = self.output_dir / 'statistics.json'
        with open(stats_file, 'w') as f:
            json.dump(stats, f, indent=2, default=str)
        print(f"\nStatistics saved to: {stats_file}")

        # Save ranked results
        ranked = self.rank_by_affinity()
        ranked_file = self.output_dir / 'ranked_results.csv'
        ranked.to_csv(ranked_file, index=False)
        print(f"Ranked results saved to: {ranked_file}")

        # Save top binders
        top_binders_file = self.output_dir / 'top_binders.csv'
        top_per_protease.to_csv(top_binders_file, index=False)
        print(f"Top binders saved to: {top_binders_file}")

        print("=" * 80)

    def run_full_analysis(self):
        """Run complete analysis pipeline"""
        print("\n" + "=" * 80)
        print("RUNNING FULL DOCKING ANALYSIS")
        print("=" * 80)

        # Generate plots
        print("\nGenerating visualizations...")
        self.plot_affinity_distribution()
        self.plot_per_protease_comparison()
        self.plot_top_binders_heatmap()
        self.plot_sequence_analysis()

        # Generate report
        self.generate_report()

        print("\n" + "=" * 80)
        print("ANALYSIS COMPLETE!")
        print(f"Results saved to: {self.output_dir}")
        print("=" * 80)


def main():
    """Main execution"""
    import argparse

    parser = argparse.ArgumentParser(description='Analyze docking results')
    parser.add_argument('--results', type=str, required=True, help='CSV file with docking results')
    parser.add_argument('--output', type=str, default='docking_analysis', help='Output directory')

    args = parser.parse_args()

    analyzer = DockingAnalyzer(args.results, args.output)
    analyzer.run_full_analysis()


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1:
        print("=" * 80)
        print("EXAMPLE USAGE:")
        print("=" * 80)
        print("python analyze_docking_results.py --results docking_results/docking_results.csv")
        print("\nCustom output directory:")
        print("python analyze_docking_results.py --results results.csv --output my_analysis")
        print("=" * 80)
    else:
        main()
