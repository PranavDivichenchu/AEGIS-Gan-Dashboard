"""
Compare binding affinities across different GAN models
Shows which model generates the best potential biomarkers
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

class GANModelComparison:
    def __init__(self, results_dir="docking_results"):
        self.results_dir = Path(results_dir)
        self.models = {}

    def load_results(self, model_name, results_file):
        """Load docking results for a specific model"""
        df = pd.read_csv(results_file)
        df = df[df['status'] == 'success']  # Only successful dockings
        df['model'] = model_name
        self.models[model_name] = df
        print(f"Loaded {len(df)} successful dockings from {model_name}")

    def load_all_results(self):
        """Auto-load all model results from standard naming"""
        for model in ['supreme', 'conditional', 'wgan']:
            file_path = self.results_dir / f"docking_results_{model}.csv"
            if file_path.exists():
                self.load_results(model.upper(), file_path)
            else:
                print(f"Warning: {file_path} not found, skipping {model}")

    def compare_overall_performance(self):
        """Compare overall binding affinity statistics across models"""
        print("\n" + "=" * 80)
        print("OVERALL MODEL COMPARISON")
        print("=" * 80)

        results = []
        for model_name, df in self.models.items():
            stats = {
                'Model': model_name,
                'Total Peptides': len(df),
                'Mean Affinity': df['binding_affinity'].mean(),
                'Median Affinity': df['binding_affinity'].median(),
                'Best Affinity': df['binding_affinity'].min(),  # More negative = better
                'Std Dev': df['binding_affinity'].std(),
                'Strong Binders (<-8)': len(df[df['binding_affinity'] < -8]),
                'Moderate Binders (<-7)': len(df[df['binding_affinity'] < -7])
            }
            results.append(stats)

        comparison_df = pd.DataFrame(results)
        print(comparison_df.to_string(index=False))

        # Determine best model
        best_mean = comparison_df.loc[comparison_df['Mean Affinity'].idxmin(), 'Model']
        best_top = comparison_df.loc[comparison_df['Best Affinity'].idxmin(), 'Model']
        best_strong = comparison_df.loc[comparison_df['Strong Binders (<-8)'].idxmax(), 'Model']

        print(f"\n🏆 Best Mean Affinity: {best_mean}")
        print(f"🏆 Best Single Candidate: {best_top}")
        print(f"🏆 Most Strong Binders: {best_strong}")

        return comparison_df

    def compare_by_protease(self):
        """Compare which model performs best for each protease"""
        print("\n" + "=" * 80)
        print("PERFORMANCE BY PROTEASE")
        print("=" * 80)

        all_data = pd.concat(self.models.values(), ignore_index=True)

        # Group by protease and model
        grouped = all_data.groupby(['protease_name', 'model'])['binding_affinity'].agg(['mean', 'min', 'count'])
        grouped = grouped.reset_index()

        # Find best model for each protease
        best_by_protease = grouped.loc[grouped.groupby('protease_name')['mean'].idxmin()]

        print("\nBest Model for Each Protease (by mean affinity):")
        print(best_by_protease[['protease_name', 'model', 'mean']].to_string(index=False))

        # Count wins per model
        model_wins = best_by_protease['model'].value_counts()
        print("\n📊 Model Performance Summary:")
        for model, wins in model_wins.items():
            print(f"   {model}: Best for {wins} proteases")

        return best_by_protease

    def get_top_candidates(self, n=20):
        """Get top N candidates across all models"""
        print("\n" + "=" * 80)
        print(f"TOP {n} BIOMARKER CANDIDATES (ALL MODELS)")
        print("=" * 80)

        all_data = pd.concat(self.models.values(), ignore_index=True)
        top_candidates = all_data.nsmallest(n, 'binding_affinity')

        print(top_candidates[['model', 'peptide_id', 'protease_name', 'binding_affinity', 'peptide_sequence']].to_string(index=False))

        # Show model distribution in top candidates
        print(f"\n📊 Model Distribution in Top {n}:")
        model_dist = top_candidates['model'].value_counts()
        for model, count in model_dist.items():
            print(f"   {model}: {count} candidates ({count/n*100:.1f}%)")

        return top_candidates

    def visualize_comparison(self, output_dir="model_comparison"):
        """Create visualization comparing models"""
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)

        all_data = pd.concat(self.models.values(), ignore_index=True)

        # 1. Distribution plot
        plt.figure(figsize=(12, 6))
        for model_name, df in self.models.items():
            plt.hist(df['binding_affinity'], bins=30, alpha=0.5, label=model_name)
        plt.xlabel('Binding Affinity (kcal/mol)')
        plt.ylabel('Frequency')
        plt.title('Binding Affinity Distribution by GAN Model')
        plt.legend()
        plt.axvline(-7, color='red', linestyle='--', label='Strong binder threshold')
        plt.savefig(output_dir / 'affinity_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()

        # 2. Box plot comparison
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=all_data, x='model', y='binding_affinity')
        plt.ylabel('Binding Affinity (kcal/mol)')
        plt.xlabel('GAN Model')
        plt.title('Binding Affinity Comparison Across Models')
        plt.axhline(-7, color='red', linestyle='--', alpha=0.5)
        plt.savefig(output_dir / 'model_boxplot.png', dpi=300, bbox_inches='tight')
        plt.close()

        # 3. Top candidates by model
        top_by_model = all_data.groupby('model').apply(
            lambda x: x.nsmallest(10, 'binding_affinity')['binding_affinity'].mean()
        )

        plt.figure(figsize=(8, 6))
        top_by_model.plot(kind='bar', color=['#1f77b4', '#ff7f0e', '#2ca02c'])
        plt.ylabel('Mean Affinity of Top 10 (kcal/mol)')
        plt.xlabel('GAN Model')
        plt.title('Mean Binding Affinity of Top 10 Candidates')
        plt.xticks(rotation=0)
        plt.tight_layout()
        plt.savefig(output_dir / 'top10_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()

        # 4. Success rate by protease
        protease_stats = all_data.groupby(['protease_name', 'model'])['binding_affinity'].mean().reset_index()
        protease_pivot = protease_stats.pivot(index='protease_name', columns='model', values='binding_affinity')

        plt.figure(figsize=(12, 10))
        sns.heatmap(protease_pivot, annot=True, fmt='.2f', cmap='RdYlGn_r', center=-6)
        plt.title('Mean Binding Affinity by Protease and Model')
        plt.tight_layout()
        plt.savefig(output_dir / 'protease_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()

        print(f"\n✓ Visualizations saved to {output_dir}/")

    def generate_report(self, output_file="model_comparison_report.txt"):
        """Generate comprehensive comparison report"""
        with open(output_file, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("GAN MODEL COMPARISON REPORT\n")
            f.write("=" * 80 + "\n\n")

            # Overall comparison
            comparison_df = self.compare_overall_performance()
            f.write("\nOVERALL PERFORMANCE:\n")
            f.write(comparison_df.to_string(index=False) + "\n\n")

            # Best by protease
            best_by_protease = self.compare_by_protease()
            f.write("\nBEST MODEL BY PROTEASE:\n")
            f.write(best_by_protease[['protease_name', 'model', 'mean']].to_string(index=False) + "\n\n")

            # Top candidates
            top_candidates = self.get_top_candidates(n=20)
            f.write("\nTOP 20 BIOMARKER CANDIDATES:\n")
            f.write(top_candidates[['model', 'peptide_id', 'protease_name', 'binding_affinity']].to_string(index=False) + "\n\n")

        print(f"\n✓ Report saved to {output_file}")


def main():
    """Main execution"""
    import argparse

    parser = argparse.ArgumentParser(description='Compare GAN model performance for biomarker generation')
    parser.add_argument('--results-dir', type=str, default='docking_results',
                        help='Directory containing docking results')
    parser.add_argument('--top-n', type=int, default=20,
                        help='Number of top candidates to show')

    args = parser.parse_args()

    print("=" * 80)
    print("GAN MODEL COMPARISON FOR BIOMARKER DISCOVERY")
    print("=" * 80)

    comparator = GANModelComparison(results_dir=args.results_dir)
    comparator.load_all_results()

    if not comparator.models:
        print("\nError: No model results found!")
        print("Expected files like: docking_results_supreme.csv, docking_results_conditional.csv, etc.")
        return

    # Run all comparisons
    comparator.compare_overall_performance()
    comparator.compare_by_protease()
    comparator.get_top_candidates(n=args.top_n)
    comparator.visualize_comparison()
    comparator.generate_report()

    print("\n" + "=" * 80)
    print("COMPARISON COMPLETE!")
    print("=" * 80)


if __name__ == "__main__":
    main()
