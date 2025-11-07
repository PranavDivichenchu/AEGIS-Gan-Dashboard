import torch
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
import pickle
import os

PROTEASES = {
    "Neutrophil elastase (ELANE)": "S01.131",
    "Proteinase 3 (PRTN3)": "S01.132",
    "Cathepsin G (CTSG)": "S01.133",
    "MMP8 (Collagenase-2)": "M10.002",
    "MMP9 (Gelatinase B)": "M10.004",
    "Thrombin (F2, coagulation factor IIa)": "S01.217",
    "Plasmin": "S01.233",
    "Caspase-1": "C14.001",
    "NSP1": "S01.134",
    "NSP2": "S01.135",
    "Granzyme B": "S01.021",
    "Kallikrein 1": "S01.070",
    "Kallikrein 2": "S01.071",
    "MMP1 (Collagenase-1)": "M10.001",
    "MMP2 (Gelatinase A)": "M10.003",
    "MMP7 (Matrilysin)": "M10.005",
    "MMP12 (Macrophage metalloelastase)": "M10.006",
    "Factor VIIa": "S01.220",
    "Factor IXa": "S01.221",
    "Factor Xa": "S01.222",
    "tPA": "S01.234",
    "Urokinase": "S01.235",
    "Caspase-3": "C14.002",
    "Caspase-6": "C14.003",
    "Caspase-7": "C14.004",
    "Caspase-8": "C14.005",
    "Caspase-9": "C14.006",
}

# Standard 20 amino acids (3-letter codes)
STANDARD_AA_3LETTER = {
    'Ala', 'Arg', 'Asn', 'Asp', 'Cys', 'Gln', 'Glu', 'Gly', 'His', 'Ile',
    'Leu', 'Lys', 'Met', 'Phe', 'Pro', 'Ser', 'Thr', 'Trp', 'Tyr', 'Val'
}

SEQUENCES_PER_PROTEASE = 10
OUTPUT_DIR = "generated_sequences"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def is_standard_sequence(sequence):
    """Check if sequence contains only standard amino acids"""
    import re

    # Remove any special characters and check what's left
    # Standard sequences should ONLY contain 3-letter codes from our set

    # Try to match the entire sequence as a concatenation of standard 3-letter codes
    # Each standard AA is exactly 3 characters: Capital + lowercase + lowercase
    pattern = r'^(' + '|'.join(STANDARD_AA_3LETTER) + r')+$'

    return bool(re.match(pattern, sequence))


class SequenceGenerator:
    def __init__(self, base_dir="."):
        self.base_dir = base_dir
        self.device = DEVICE
        self.setup_encoders()

    def setup_encoders(self):
        df = pd.read_csv(os.path.join(self.base_dir, "MEROPS_sepsis_expanded_dataset.csv"))
        sequence_cols = ['P4','P3','P2','P1',"P1'","P2'","P3'","P4'"]
        label_col = 'Label'
        protease_col = 'Protease_Name'

        df_pos = df[df[label_col] == 1].copy()

        # Setup amino acid encoders
        self.encoders = {}
        for col in sequence_cols:
            le = LabelEncoder()
            df_pos[col] = le.fit_transform(df_pos[col])
            self.encoders[col] = le

        # Setup protease encoder
        self.protease_encoder = LabelEncoder()
        df_pos['Protease_Encoded'] = self.protease_encoder.fit_transform(df_pos[protease_col])

        # Setup scaler
        data = df_pos[sequence_cols].values.astype(float)
        self.scaler = StandardScaler()
        self.scaler.fit(data)

        self.sequence_cols = sequence_cols
        self.num_proteases = len(self.protease_encoder.classes_)

        print(f"Encoders setup for {self.num_proteases} proteases")

    def load_conditional_gan(self):
        from ConditionalGAN import ConditionalGenerator

        latent_dim = 16
        data_dim = 8
        hidden_dim = 200

        model = ConditionalGenerator(latent_dim, self.num_proteases, data_dim, hidden_dim).to(self.device)
        model.load_state_dict(torch.load("cgan_generator.pth", map_location=self.device))
        model.eval()

        return model, latent_dim, "ConditionalGAN"

    def load_supreme_gan(self):
        from SupremeGAN import SupremeGenerator

        latent_dim = 128
        data_dim = 8
        hidden_dim = 256

        model = SupremeGenerator(latent_dim, self.num_proteases, data_dim, hidden_dim).to(self.device)
        model.load_state_dict(torch.load("supreme_generator.pth", map_location=self.device))
        model.eval()

        return model, latent_dim, "SupremeGAN"

    def load_wgan_gp(self):
        """Load WGAN-GP model"""
        from WGAN_GP import Generator

        latent_dim = 32
        data_dim = 8
        hidden_dim = 256

        model = Generator(latent_dim, self.num_proteases, data_dim, hidden_dim).to(self.device)
        model.load_state_dict(torch.load("wgan_generator.pth", map_location=self.device))
        model.eval()

        return model, latent_dim, "WGAN-GP"

    def generate_sequences(self, generator, latent_dim, protease_idx, num_samples):
        """Generate sequences for a specific protease"""
        z = torch.randn(num_samples, latent_dim).to(self.device)
        labels = torch.full((num_samples,), protease_idx, dtype=torch.long).to(self.device)

        with torch.no_grad():
            synthetic_data = generator(z, labels).cpu().numpy()

        synthetic_data = self.scaler.inverse_transform(synthetic_data)

        sequences = []
        for row in synthetic_data:
            aa_row = []
            for i, col in enumerate(self.sequence_cols):
                value = row[i]
                valid_min, valid_max = 0, len(self.encoders[col].classes_) - 1
                if np.isnan(value):
                    idx = valid_min
                else:
                    idx = int(round(value))
                    idx = max(valid_min, min(valid_max, idx))
                aa = self.encoders[col].inverse_transform([idx])[0]
                aa_row.append(aa)
            sequences.append(''.join(aa_row))  # Join into single string

        return sequences

    def generate_all_sequences(self, model_name="supreme", num_sequences_per_protease=None):
        """Generate sequences from specified model for all proteases"""

        # Use parameter or fall back to default
        if num_sequences_per_protease is None:
            num_sequences_per_protease = SEQUENCES_PER_PROTEASE

        # Load appropriate model
        if model_name.lower() == "conditional":
            generator, latent_dim, model_label = self.load_conditional_gan()
        elif model_name.lower() == "supreme":
            generator, latent_dim, model_label = self.load_supreme_gan()
        elif model_name.lower() == "wgan":
            generator, latent_dim, model_label = self.load_wgan_gp()
        else:
            raise ValueError(f"Unknown model: {model_name}")

        print(f"\nGenerating sequences using {model_label}...")
        print(f"Generating {num_sequences_per_protease} sequences per protease...")

        all_sequences = []
        for protease_name, merops_id in PROTEASES.items():
            # Get protease index
            protease_idx = np.where(self.protease_encoder.classes_ == protease_name)[0]

            if len(protease_idx) == 0:
                print(f"Warning: {protease_name} not found in encoder, skipping...")
                continue

            protease_idx = protease_idx[0]

            # Generate sequences
            sequences = self.generate_sequences(generator, latent_dim, protease_idx, num_sequences_per_protease)

            for seq in sequences:
                all_sequences.append({
                    'protease_name': protease_name,
                    'merops_id': merops_id,
                    'sequence': seq,
                    'model': model_label
                })

            print(f"  Generated {len(sequences)} sequences for {protease_name}")

        # Create output directory
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        # Filter to only standard amino acids
        df = pd.DataFrame(all_sequences)
        original_count = len(df)

        print(f"\nFiltering to standard amino acids only...")
        df['is_standard'] = df['sequence'].apply(is_standard_sequence)
        df_filtered = df[df['is_standard']].copy()
        df_filtered = df_filtered.drop(columns=['is_standard'])

        filtered_count = len(df_filtered)
        removed_count = original_count - filtered_count

        print(f"  Original sequences: {original_count}")
        print(f"  Standard AA sequences: {filtered_count} ({filtered_count/original_count*100:.1f}%)")
        print(f"  Removed (non-standard): {removed_count}")

        # Save to CSV
        output_file = os.path.join(OUTPUT_DIR, f"{model_label.lower()}_sequences.csv")
        df_filtered.to_csv(output_file, index=False)

        print(f"\nSaved {len(df_filtered)} sequences to {output_file}")

        # Also save in FASTA format for structure prediction
        fasta_file = os.path.join(OUTPUT_DIR, f"{model_label.lower()}_sequences.fasta")
        with open(fasta_file, 'w') as f:
            for i, row in df_filtered.iterrows():
                header = f">{row['protease_name']}|{row['merops_id']}|seq_{i}"
                f.write(f"{header}\n{row['sequence']}\n")

        print(f"Saved FASTA format to {fasta_file}")

        return df_filtered


def main():
    """Main execution"""
    print("=" * 80)
    print("SEQUENCE GENERATION FOR MOLECULAR DOCKING")
    print("=" * 80)
    print(f"Device: {DEVICE}")
    print(f"Sequences per protease: {SEQUENCES_PER_PROTEASE}")
    print(f"Total proteases: {len(PROTEASES)}")
    print(f"Expected total sequences: {len(PROTEASES) * SEQUENCES_PER_PROTEASE}")
    print("=" * 80)

    generator = SequenceGenerator()

    # Generate from all models
    for model in ["supreme", "conditional"]:
        try:
            df = generator.generate_all_sequences(model_name=model)
            print(f"\n{model.upper()} generation complete!")
            print(f"Sample sequences:\n{df.head(10)}")
        except Exception as e:
            print(f"Error generating from {model}: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 80)
    print("SEQUENCE GENERATION COMPLETE!")
    print("=" * 80)


if __name__ == "__main__":
    main()
