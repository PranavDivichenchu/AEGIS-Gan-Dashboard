import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
import numpy as np
import matplotlib.pyplot as plt
import os

# =====================
# Load and preprocess data
# =====================
df = pd.read_csv("/Users/pranavdivichenchu/Documents/AET Senior Research/MEROPS_sepsis_expanded_dataset.csv")
sequence_cols = ['P4','P3','P2','P1',"P1'","P2'","P3'","P4'"]
label_col = 'Label'
df_pos = df[df[label_col] == 1].copy()

encoders = {}
for col in sequence_cols:
    le = LabelEncoder()
    df_pos[col] = le.fit_transform(df_pos[col])
    encoders[col] = le

data = df_pos[sequence_cols].values.astype(float)


scaler = StandardScaler()
data = scaler.fit_transform(data)
real_data = torch.tensor(data, dtype=torch.float32)


latent_dim = 16
data_dim = real_data.shape[1]
hidden_dim = 500  
batch_size = 32
lr = 0.0001
epochs = 250
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class Generator(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(latent_dim, hidden_dim),
            nn.LeakyReLU(0.2),
            nn.Linear(hidden_dim, hidden_dim),
            nn.LeakyReLU(0.2),
            nn.Linear(hidden_dim, hidden_dim),
            nn.LeakyReLU(0.2),
            nn.Linear(hidden_dim, data_dim)
        )
    def forward(self, z):
        return self.net(z)

class Discriminator(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(data_dim, hidden_dim),
            nn.LeakyReLU(0.2),
            nn.Linear(hidden_dim, hidden_dim),
            nn.LeakyReLU(0.2),
            nn.Linear(hidden_dim, hidden_dim),
            nn.LeakyReLU(0.2),
            nn.Linear(hidden_dim, 1),
            nn.Sigmoid()
        )
    def forward(self, x):
        return self.net(x)


def save_models(generator, discriminator, gen_path="generator.pth", disc_path="discriminator.pth"):
    torch.save(generator.state_dict(), gen_path)
    torch.save(discriminator.state_dict(), disc_path)
    print(f"✅ Models saved to {gen_path} and {disc_path}")

def load_models(generator, discriminator, gen_path="generator.pth", disc_path="discriminator.pth"):
    generator.load_state_dict(torch.load(gen_path))
    discriminator.load_state_dict(torch.load(disc_path))
    generator.eval()
    discriminator.eval()
    print(f"✅ Models loaded from {gen_path} and {disc_path}")

G = Generator().to(device)
D = Discriminator().to(device)


if os.path.exists("generator.pth") and os.path.exists("discriminator.pth"):
    load_models(G, D)
else:
    print("No saved models found, proceeding with training.")


criterion = nn.BCELoss()
optimizer_G = optim.Adam(G.parameters(), lr=lr, betas=(0.5, 0.999))
optimizer_D = optim.Adam(D.parameters(), lr=lr, betas=(0.5, 0.999))

G_losses, D_losses = [], []


def generate_sequences(G, num_samples=10):
    z = torch.randn(num_samples, latent_dim).to(device)
    synthetic_data = G(z).detach().cpu().numpy()
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
    return synthetic_sequences

def compare_distributions(real_data, fake_data, epoch):
    real_mean = np.mean(real_data, axis=0)
    fake_mean = np.mean(fake_data, axis=0)
    diff = np.abs(real_mean - fake_mean).mean()
    print(f"Epoch {epoch}: Mean feature deviation = {diff:.4f}")


for epoch in range(epochs):
    for _ in range(len(real_data) // batch_size):
        
        D.zero_grad()
        idx = torch.randint(0, len(real_data), (batch_size,))
        real_batch = real_data[idx].to(device)
        real_labels = torch.ones(batch_size, 1).to(device)
        fake_labels = torch.zeros(batch_size, 1).to(device)

        loss_real = criterion(D(real_batch), real_labels)
        z = torch.randn(batch_size, latent_dim).to(device)
        fake_batch = G(z)
        loss_fake = criterion(D(fake_batch.detach()), fake_labels)
        loss_D = loss_real + loss_fake
        loss_D.backward()
        optimizer_D.step()

        
        G.zero_grad()
        z = torch.randn(batch_size, latent_dim).to(device)
        fake_batch = G(z)
        loss_G = criterion(D(fake_batch), real_labels)
        loss_G.backward()
        optimizer_G.step()

   
    G_losses.append(loss_G.item())
    D_losses.append(loss_D.item())

   
    if (epoch + 1) % 50 == 0:
        print(f"\nEpoch {epoch+1}/{epochs}: D Loss={loss_D.item():.4f}, G Loss={loss_G.item():.4f}")
        fake_data_np = fake_batch.detach().cpu().numpy()
        compare_distributions(real_data.numpy(), fake_data_np, epoch + 1)

        print("Sample generated sequences:")
        for seq in generate_sequences(G, num_samples=5):
            print(seq)
        print("-" * 60)


plt.figure(figsize=(8,5))
plt.plot(D_losses, label="Discriminator Loss")
plt.plot(G_losses, label="Generator Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()
plt.title("GAN Training Losses")
plt.show()


save_models(G, D)

for seq in generate_sequences(G, num_samples=10):
    print(seq)
