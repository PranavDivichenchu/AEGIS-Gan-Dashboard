import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
import numpy as np
import matplotlib.pyplot as plt
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

print(f"Number of unique proteases: {num_proteases}")
print(f"Protease classes: {protease_encoder.classes_}")


data = df_pos[sequence_cols].values.astype(float)
protease_labels = df_pos['Protease_Encoded'].values


scaler = StandardScaler()
data = scaler.fit_transform(data)
real_data = torch.tensor(data, dtype=torch.float32)
protease_tensor = torch.tensor(protease_labels, dtype=torch.long)


latent_dim = 16
data_dim = real_data.shape[1]
hidden_dim = 200
batch_size = 32
lr = 0.001
epochs = 300
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print(f"Using device: {device}")


class ConditionalGenerator(nn.Module):
    def __init__(self, latent_dim, num_classes, data_dim, hidden_dim):
        super().__init__()
        self.label_embedding = nn.Embedding(num_classes, num_classes)

        self.net = nn.Sequential(
            nn.Linear(latent_dim + num_classes, hidden_dim),
            nn.LeakyReLU(0.2),
            nn.BatchNorm1d(hidden_dim),
            nn.Linear(hidden_dim, hidden_dim),
            nn.LeakyReLU(0.2),
            nn.BatchNorm1d(hidden_dim),
            nn.Linear(hidden_dim, hidden_dim),
            nn.LeakyReLU(0.2),
            nn.BatchNorm1d(hidden_dim),
            nn.Linear(hidden_dim, data_dim)
        )

    def forward(self, z, labels):
        
        label_embedding = self.label_embedding(labels)
        gen_input = torch.cat([z, label_embedding], dim=1)
        return self.net(gen_input)

class ConditionalDiscriminator(nn.Module):
    def __init__(self, data_dim, num_classes, hidden_dim):
        super().__init__()
        self.label_embedding = nn.Embedding(num_classes, num_classes)

        self.net = nn.Sequential(
            nn.Linear(data_dim + num_classes, hidden_dim),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.3),
            nn.Linear(hidden_dim, hidden_dim),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.3),
            nn.Linear(hidden_dim, hidden_dim),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.3),
            nn.Linear(hidden_dim, 1),
            nn.Sigmoid()
        )

    def forward(self, x, labels):
        
        label_embedding = self.label_embedding(labels)
        disc_input = torch.cat([x, label_embedding], dim=1)
        return self.net(disc_input)


def save_models(generator, discriminator, gen_path="cgan_generator.pth", disc_path="cgan_discriminator.pth"):
    torch.save(generator.state_dict(), gen_path)
    torch.save(discriminator.state_dict(), disc_path)
    print(f"Models saved to {gen_path} and {disc_path}")

def load_models(generator, discriminator, gen_path="cgan_generator.pth", disc_path="cgan_discriminator.pth"):
    if os.path.exists(gen_path) and os.path.exists(disc_path):
        generator.load_state_dict(torch.load(gen_path, map_location=device))
        discriminator.load_state_dict(torch.load(disc_path, map_location=device))
        generator.eval()
        discriminator.eval()
        print(f"Models loaded from {gen_path} and {disc_path}")
        return True
    return False


G = ConditionalGenerator(latent_dim, num_proteases, data_dim, hidden_dim).to(device)
D = ConditionalDiscriminator(data_dim, num_proteases, hidden_dim).to(device)

 
if not load_models(G, D):
    print("No saved models found, proceeding with training from scratch.")


criterion = nn.BCELoss()
optimizer_G = optim.Adam(G.parameters(), lr=lr, betas=(0.5, 0.999))
optimizer_D = optim.Adam(D.parameters(), lr=lr, betas=(0.5, 0.999))

G_losses, D_losses = [], []


def generate_sequences(G, protease_name=None, protease_idx=None, num_samples=10):
    """
    Generate sequences conditioned on a specific protease.

    Args:
        G: Generator model
        protease_name: Name of protease (e.g., "Neutrophil elastase (ELANE)")
        protease_idx: Index of protease (alternative to protease_name)
        num_samples: Number of sequences to generate
    """
    if protease_name is not None:
        protease_idx = np.where(protease_encoder.classes_ == protease_name)[0][0]
    elif protease_idx is None:
        protease_idx = 0  

    z = torch.randn(num_samples, latent_dim).to(device)
    labels = torch.full((num_samples,), protease_idx, dtype=torch.long).to(device)

    synthetic_data = G(z, labels).detach().cpu().numpy()
    synthetic_data = scaler.inverse_transform(synthetic_data)

    synthetic_sequences = []
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
        synthetic_sequences.append(aa_row)

    return synthetic_sequences, protease_encoder.classes_[protease_idx]

def compare_distributions(real_data, fake_data, epoch):
    real_mean = np.mean(real_data, axis=0)
    fake_mean = np.mean(fake_data, axis=0)
    diff = np.abs(real_mean - fake_mean).mean()
    print(f"Epoch {epoch}: Mean feature deviation = {diff:.4f}")


print("\nStarting Conditional GAN training...")
print("=" * 60)

for epoch in range(epochs):
    epoch_d_loss = 0
    epoch_g_loss = 0
    num_batches = len(real_data) // batch_size

    for _ in range(num_batches):
        
        D.zero_grad()
        idx = torch.randint(0, len(real_data), (batch_size,))
        real_batch = real_data[idx].to(device)
        real_protease_labels = protease_tensor[idx].to(device)
        real_labels = torch.ones(batch_size, 1).to(device)
        fake_labels = torch.zeros(batch_size, 1).to(device)

        
        loss_real = criterion(D(real_batch, real_protease_labels), real_labels)

       
        z = torch.randn(batch_size, latent_dim).to(device)
        fake_batch = G(z, real_protease_labels)
        loss_fake = criterion(D(fake_batch.detach(), real_protease_labels), fake_labels)

        loss_D = loss_real + loss_fake
        loss_D.backward()
        optimizer_D.step()

      
        G.zero_grad()
        z = torch.randn(batch_size, latent_dim).to(device)
        fake_batch = G(z, real_protease_labels)
        loss_G = criterion(D(fake_batch, real_protease_labels), real_labels)
        loss_G.backward()
        optimizer_G.step()

        epoch_d_loss += loss_D.item()
        epoch_g_loss += loss_G.item()

    
    G_losses.append(epoch_g_loss / num_batches)
    D_losses.append(epoch_d_loss / num_batches)

    
    if (epoch + 1) % 50 == 0:
        print(f"\nEpoch {epoch+1}/{epochs}: D Loss={D_losses[-1]:.4f}, G Loss={G_losses[-1]:.4f}")

        
        print("\nSample generated sequences for different proteases:")
        for i in range(min(3, num_proteases)):
            sequences, protease_name = generate_sequences(G, protease_idx=i, num_samples=2)
            print(f"\n{protease_name}:")
            for seq in sequences:
                print(f"  {seq}")
        print("-" * 60)


plt.figure(figsize=(10, 6))
plt.plot(D_losses, label="Discriminator Loss", alpha=0.7)
plt.plot(G_losses, label="Generator Loss", alpha=0.7)
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()
plt.title("Conditional GAN Training Losses")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("cgan_training_losses.png")
print("\nTraining loss plot saved as 'cgan_training_losses.png'")
plt.show()


save_models(G, D)


print("\nFinal generated sequences for all proteases:")
for i in range(num_proteases):
    sequences, protease_name = generate_sequences(G, protease_idx=i, num_samples=5)
    print(f"\n{protease_name}:")
    for seq in sequences:
        print(f"  {' '.join(seq)}")

print("Training completed.")
