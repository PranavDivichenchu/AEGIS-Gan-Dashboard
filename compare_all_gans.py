import torch
import torch.nn as nn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score
from scipy.spatial.distance import pdist, squareform
import seaborn as sns
from collections import Counter
import os

df = pd.read_csv("/Users/pranavdivichenchu/Documents/AET Senior Research/MEROPS_sepsis_expanded_dataset.csv")
sequence_cols = ['P4','P3','P2','P1',"P1'","P2'","P3'","P4'"]
label_col = 'Label'
protease_col = 'Protease_Name'

df_pos = df[df[label_col] == 1].copy()


encoders = {}
for col in sequence_cols:
    le = LabelEncoder()
    df_pos[col] = le.fit_transform(df_pos[col])
    encoders[col] = le


protease_encoder = LabelEncoder()
df_pos['Protease_Encoded'] = protease_encoder.fit_transform(df_pos[protease_col])
num_proteases = len(protease_encoder.classes_)

data = df_pos[sequence_cols].values.astype(float)
protease_labels = df_pos['Protease_Encoded'].values

scaler = StandardScaler()
data = scaler.fit_transform(data)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def calculate_diversity_score(sequences):
    """
    Calculate diversity within generated sequences.
    Higher is better (more diverse).
    """
    if len(sequences) < 2:
        return 0.0
    
    numeric_seqs = []
    for seq in sequences:
        numeric = []
        for i, aa in enumerate(seq):
            col = sequence_cols[i]
            try:
                idx = np.where(encoders[col].classes_ == aa)[0][0]
                numeric.append(idx)
            except:
                numeric.append(0)
        numeric_seqs.append(numeric)

    numeric_seqs = np.array(numeric_seqs)

    
    distances = pdist(numeric_seqs, metric='euclidean')
    avg_distance = np.mean(distances)

    return avg_distance

def calculate_biological_validity(sequences):
    """
    Check if generated sequences use valid amino acids.
    Returns percentage of valid amino acids.
    """
    total_positions = 0
    valid_positions = 0

    for seq in sequences:
        for i, aa in enumerate(seq):
            total_positions += 1
            col = sequence_cols[i]
            if aa in encoders[col].classes_:
                valid_positions += 1

    return valid_positions / total_positions if total_positions > 0 else 0.0

def calculate_amino_acid_distribution(sequences, position):
    aa_counts = Counter()
    for seq in sequences:
        if position < len(seq):
            aa_counts[seq[position]] += 1

    return dict(aa_counts)

def evaluate_mode_coverage(generator, generator_func, num_samples=100):
    mode_coverage = {}

    for protease_idx in range(num_proteases):
        sequences, protease_name = generator_func(generator, protease_idx=protease_idx, num_samples=num_samples)
        diversity = calculate_diversity_score(sequences)
        validity = calculate_biological_validity(sequences)

        mode_coverage[protease_name] = {
            'diversity': diversity,
            'validity': validity,
            'sample_count': len(sequences)
        }

    return mode_coverage

def generate_sequences_vanilla(G, protease_idx=0, num_samples=10):
    latent_dim = 16
    z = torch.randn(num_samples, latent_dim).to(device)
    synthetic_data = G(z).detach().cpu().numpy()
    synthetic_data = scaler.inverse_transform(synthetic_data)

    sequences = decode_sequences(synthetic_data)
    return sequences, f"Protease_{protease_idx}"

def generate_sequences_conditional(G, protease_idx=0, num_samples=10):
    latent_dim = 16
    z = torch.randn(num_samples, latent_dim).to(device)
    labels = torch.full((num_samples,), protease_idx, dtype=torch.long).to(device)

    synthetic_data = G(z, labels).detach().cpu().numpy()
    synthetic_data = scaler.inverse_transform(synthetic_data)

    sequences = decode_sequences(synthetic_data)
    return sequences, protease_encoder.classes_[protease_idx]

def generate_sequences_wgan(G, protease_idx=0, num_samples=10):
    latent_dim = 16
    z = torch.randn(num_samples, latent_dim).to(device)
    labels = torch.full((num_samples,), protease_idx, dtype=torch.long).to(device)

    synthetic_data = G(z, labels).detach().cpu().numpy()
    synthetic_data = scaler.inverse_transform(synthetic_data)

    sequences = decode_sequences(synthetic_data)
    return sequences, protease_encoder.classes_[protease_idx]

def generate_sequences_supreme(G, protease_idx=0, num_samples=10):
    latent_dim = 128
    z = torch.randn(num_samples, latent_dim).to(device)
    labels = torch.full((num_samples,), protease_idx, dtype=torch.long).to(device)

    synthetic_data = G(z, labels).detach().cpu().numpy()
    synthetic_data = scaler.inverse_transform(synthetic_data)

    sequences = decode_sequences(synthetic_data)
    return sequences, protease_encoder.classes_[protease_idx]

def decode_sequences(synthetic_data):
    sequences = []
    for row in synthetic_data:
        aa_row = []
        for i, col in enumerate(sequence_cols):
            value = row[i]
            valid_min, valid_max = 0, len(encoders[col].classes_) - 1
            if np.isnan(value):
                idx = valid_min
            else:
                idx = int(round(value))
                idx = max(valid_min, min(valid_max, idx))
            aa = encoders[col].inverse_transform([idx])[0]
            aa_row.append(aa)
        sequences.append(aa_row)
    return sequences

def compare_all_models():
    results = {}

    # Check which models exist
    model_files = {
        'Vanilla GAN': ('generator.pth', 'discriminator.pth'),
        'Conditional GAN': ('cgan_generator.pth', 'cgan_discriminator.pth'),
        'WGAN-GP': ('wgan_generator.pth', 'wgan_critic.pth'),
        'Supreme GAN': ('supreme_generator.pth', 'supreme_critic.pth')
    }

    print("=" * 80)
    print("GAN MODEL COMPARISON")
    print("=" * 80)
    print("\nChecking for trained models...")

    available_models = []
    for model_name, (gen_file, disc_file) in model_files.items():
        if os.path.exists(gen_file) and os.path.exists(disc_file):
            print(f"  ✓ {model_name} found")
            available_models.append(model_name)
        else:
            print(f"  ✗ {model_name} not found (train it first!)")

    if not available_models:
        print("\nNo trained models found! Train some models first.")
        return

    print("\n" + "=" * 80)
    print("GENERATING SAMPLES FOR EVALUATION (100 samples per protease per model)")
    print("=" * 80)

    for model_name in available_models:
        print(f"\nEvaluating {model_name}...")

        model_results = {
            'diversity_scores': [],
            'validity_scores': [],
            'sequences': []
        }

        
        for protease_idx in range(num_proteases):
            sequences = []
            # sequences = generate_sequences_X(model, protease_idx, num_samples=100)

            diversity = calculate_diversity_score(sequences)
            validity = calculate_biological_validity(sequences)

            model_results['diversity_scores'].append(diversity)
            model_results['validity_scores'].append(validity)
            model_results['sequences'].extend(sequences[:5])  # Save a few examples

        results[model_name] = model_results

    print("\n" + "=" * 80)
    print("GENERATING COMPARISON PLOTS")
    print("=" * 80)

    fig, axes = plt.subplots(2, 2, figsize=(15, 12))

    ax = axes[0, 0]
    diversity_data = {name: res['diversity_scores'] for name, res in results.items()}
    ax.boxplot(diversity_data.values(), labels=diversity_data.keys())
    ax.set_ylabel('Diversity Score')
    ax.set_title('Sample Diversity by Model')
    ax.grid(True, alpha=0.3)
    ax.tick_params(axis='x', rotation=45)

    ax = axes[0, 1]
    validity_data = {name: res['validity_scores'] for name, res in results.items()}
    ax.boxplot(validity_data.values(), labels=validity_data.keys())
    ax.set_ylabel('Validity Score')
    ax.set_title('Biological Validity by Model')
    ax.grid(True, alpha=0.3)
    ax.tick_params(axis='x', rotation=45)

    ax = axes[1, 0]
    model_names = list(results.keys())
    avg_diversity = [np.mean(results[name]['diversity_scores']) for name in model_names]
    avg_validity = [np.mean(results[name]['validity_scores']) for name in model_names]

    x = np.arange(len(model_names))
    width = 0.35

    ax.bar(x - width/2, avg_diversity, width, label='Diversity', alpha=0.8)
    ax.bar(x + width/2, avg_validity, width, label='Validity', alpha=0.8)
    ax.set_ylabel('Score')
    ax.set_title('Average Performance Comparison')
    ax.set_xticks(x)
    ax.set_xticklabels(model_names, rotation=45, ha='right')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')

    ax = axes[1, 1]
    quality_scores = [np.mean(results[name]['diversity_scores']) * np.mean(results[name]['validity_scores'])
                      for name in model_names]
    colors = plt.cm.viridis(np.linspace(0, 1, len(model_names)))
    ax.bar(model_names, quality_scores, color=colors, alpha=0.8)
    ax.set_ylabel('Quality Score')
    ax.set_title('Overall Quality (Diversity × Validity)')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('gan_comparison_results.png', dpi=150)
    print("Comparison plots saved as 'gan_comparison_results.png'")
    plt.show()

    print("\n" + "=" * 80)
    print("SUMMARY TABLE")
    print("=" * 80)
    print(f"{'Model':<20} {'Avg Diversity':<15} {'Avg Validity':<15} {'Quality Score':<15}")
    print("-" * 80)

    for name in model_names:
        avg_div = np.mean(results[name]['diversity_scores'])
        avg_val = np.mean(results[name]['validity_scores'])
        quality = avg_div * avg_val

        print(f"{name:<20} {avg_div:<15.4f} {avg_val:<15.4f} {quality:<15.4f}")

    print("=" * 80)

    # Determine winner
    best_model = max(model_names, key=lambda name:
                    np.mean(results[name]['diversity_scores']) * np.mean(results[name]['validity_scores']))

    print(f"\n🏆 BEST PERFORMING MODEL: {best_model}")
    print("=" * 80)

    return results

if __name__ == "__main__":
    print("\n🔬 Starting comprehensive GAN comparison...")
    print("This will evaluate all trained models on multiple metrics.\n")

    results = compare_all_models()

    print("\n✅ Comparison complete!")
    print("\nInterpretation Guide:")
    print("  • Diversity: Higher = more varied sequences (good, prevents mode collapse)")
    print("  • Validity: Higher = more biologically realistic sequences (should be ~1.0)")
    print("  • Quality: Higher = better overall (combines diversity and validity)")
    print("\n" + "=" * 80)
