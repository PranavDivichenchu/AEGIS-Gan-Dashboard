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
protease_col = 'Protease_Name'

# Filter positive samples
df_pos = df[df[label_col] == 1].copy()

# Encode amino acids numerically
encoders = {}
for col in sequence_cols:
    le = LabelEncoder()
    df_pos[col] = le.fit_transform(df_pos[col])
    encoders[col] = le

# Encode protease types
protease_encoder = LabelEncoder()
df_pos['Protease_Encoded'] = protease_encoder.fit_transform(df_pos[protease_col])
num_proteases = len(protease_encoder.classes_)

print(f"Number of unique proteases: {num_proteases}")
print(f"Protease classes: {protease_encoder.classes_}")

# Extract sequence data and protease labels
data = df_pos[sequence_cols].values.astype(float)
protease_labels = df_pos['Protease_Encoded'].values

# Standardize sequence data
scaler = StandardScaler()
data = scaler.fit_transform(data)
real_data = torch.tensor(data, dtype=torch.float32)
protease_tensor = torch.tensor(protease_labels, dtype=torch.long)

# =====================
# Hyperparameters
# =====================
latent_dim = 16
data_dim = real_data.shape[1]
hidden_dim = 200
batch_size = 32
lr = 0.0001  # Lower learning rate for WGAN-GP
epochs = 250
n_critic = 5  # Number of critic updates per generator update
lambda_gp = 10  # Gradient penalty coefficient
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print(f"Using device: {device}")

# =====================
# WGAN-GP Model definitions
# =====================
class WGANGenerator(nn.Module):
    """
    Conditional Generator for WGAN-GP
    Takes random noise + protease label → generates peptide sequence
    """
    def __init__(self, latent_dim, num_classes, data_dim, hidden_dim):
        super().__init__()
        self.label_embedding = nn.Embedding(num_classes, num_classes)

        self.net = nn.Sequential(
            nn.Linear(latent_dim + num_classes, hidden_dim),
            nn.LayerNorm(hidden_dim),  # LayerNorm instead of BatchNorm for better stability
            nn.LeakyReLU(0.2),

            nn.Linear(hidden_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.LeakyReLU(0.2),

            nn.Linear(hidden_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.LeakyReLU(0.2),

            nn.Linear(hidden_dim, data_dim)
        )

    def forward(self, z, labels):
        label_embedding = self.label_embedding(labels)
        gen_input = torch.cat([z, label_embedding], dim=1)
        return self.net(gen_input)

class WGANCritic(nn.Module):
    """
    Conditional Critic (Discriminator) for WGAN-GP
    Takes peptide sequence + protease label → outputs score (not probability!)
    Key difference: NO SIGMOID activation at the end
    """
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

            nn.Linear(hidden_dim, 1)
            # NO SIGMOID - outputs raw score (can be any real number)
        )

    def forward(self, x, labels):
        label_embedding = self.label_embedding(labels)
        critic_input = torch.cat([x, label_embedding], dim=1)
        return self.net(critic_input)

# =====================
# Gradient Penalty
# =====================
def compute_gradient_penalty(critic, real_samples, fake_samples, labels, device):
    """
    Calculates the gradient penalty loss for WGAN-GP.

    The gradient penalty enforces the Lipschitz constraint by penalizing
    the critic if its gradients deviate from norm 1 on interpolated samples.

    Args:
        critic: The critic network
        real_samples: Real data batch
        fake_samples: Generated data batch
        labels: Protease labels for conditioning
        device: cuda or cpu

    Returns:
        gradient_penalty: Scalar loss value
    """
    batch_size = real_samples.size(0)

    # Random weight term for interpolation between real and fake samples
    alpha = torch.rand(batch_size, 1).to(device)

    # Get random interpolation between real and fake samples
    interpolates = (alpha * real_samples + (1 - alpha) * fake_samples).requires_grad_(True)

    # Calculate critic scores on interpolated samples
    critic_interpolates = critic(interpolates, labels)

    # Get gradient w.r.t. interpolates
    gradients = torch.autograd.grad(
        outputs=critic_interpolates,
        inputs=interpolates,
        grad_outputs=torch.ones_like(critic_interpolates),
        create_graph=True,
        retain_graph=True,
        only_inputs=True
    )[0]

    # Flatten gradients
    gradients = gradients.view(batch_size, -1)

    # Calculate penalty
    gradient_norm = gradients.norm(2, dim=1)
    gradient_penalty = ((gradient_norm - 1) ** 2).mean()

    return gradient_penalty

# =====================
# Save/load utilities
# =====================
def save_models(generator, critic, gen_path="wgan_generator.pth", critic_path="wgan_critic.pth"):
    torch.save(generator.state_dict(), gen_path)
    torch.save(critic.state_dict(), critic_path)
    print(f"Models saved to {gen_path} and {critic_path}")

def load_models(generator, critic, gen_path="wgan_generator.pth", critic_path="wgan_critic.pth"):
    if os.path.exists(gen_path) and os.path.exists(critic_path):
        generator.load_state_dict(torch.load(gen_path, map_location=device))
        critic.load_state_dict(torch.load(critic_path, map_location=device))
        generator.eval()
        critic.eval()
        print(f"Models loaded from {gen_path} and {critic_path}")
        return True
    return False

# Initialize models
G = WGANGenerator(latent_dim, num_proteases, data_dim, hidden_dim).to(device)
C = WGANCritic(data_dim, num_proteases, hidden_dim).to(device)

# Try to load existing models
if not load_models(G, C):
    print("No saved models found, proceeding with training from scratch.")

# =====================
# Training setup
# =====================
# Use RMSprop or Adam with low learning rate
optimizer_G = optim.Adam(G.parameters(), lr=lr, betas=(0.0, 0.9))
optimizer_C = optim.Adam(C.parameters(), lr=lr, betas=(0.0, 0.9))

G_losses, C_losses, wasserstein_distances = [], [], []

# =====================
# Evaluation helpers
# =====================
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

# =====================
# Training loop
# =====================
print("\nStarting WGAN-GP training...")
print("=" * 60)
print(f"Training for {epochs} epochs with {n_critic} critic updates per generator update")
print("=" * 60)

for epoch in range(epochs):
    epoch_c_loss = 0
    epoch_g_loss = 0
    epoch_wd = 0
    num_batches = len(real_data) // batch_size

    for _ in range(num_batches):
        # ----- Train Critic (n_critic times) -----
        for _ in range(n_critic):
            C.zero_grad()

            # Sample real data
            idx = torch.randint(0, len(real_data), (batch_size,))
            real_batch = real_data[idx].to(device)
            real_protease_labels = protease_tensor[idx].to(device)

            # Generate fake data
            z = torch.randn(batch_size, latent_dim).to(device)
            fake_batch = G(z, real_protease_labels).detach()

            # Critic scores
            real_validity = C(real_batch, real_protease_labels)
            fake_validity = C(fake_batch, real_protease_labels)

            # Gradient penalty
            gp = compute_gradient_penalty(C, real_batch, fake_batch, real_protease_labels, device)

            # Wasserstein loss with gradient penalty
            # Critic wants to maximize: E[C(real)] - E[C(fake)]
            # So we minimize: -E[C(real)] + E[C(fake)] + lambda * GP
            loss_C = -torch.mean(real_validity) + torch.mean(fake_validity) + lambda_gp * gp

            loss_C.backward()
            optimizer_C.step()

        # ----- Train Generator (once) -----
        G.zero_grad()

        # Generate fake data
        z = torch.randn(batch_size, latent_dim).to(device)
        fake_batch = G(z, real_protease_labels)

        # Generator loss: wants critic to output high scores for fake data
        # Maximize: E[C(fake)] → Minimize: -E[C(fake)]
        fake_validity = C(fake_batch, real_protease_labels)
        loss_G = -torch.mean(fake_validity)

        loss_G.backward()
        optimizer_G.step()

        # Track losses
        epoch_c_loss += loss_C.item()
        epoch_g_loss += loss_G.item()

        # Wasserstein distance estimate (without GP term)
        wd = torch.mean(real_validity).item() - torch.mean(C(fake_batch.detach(), real_protease_labels)).item()
        epoch_wd += wd

    # Record average losses
    C_losses.append(epoch_c_loss / num_batches)
    G_losses.append(epoch_g_loss / num_batches)
    wasserstein_distances.append(epoch_wd / num_batches)

    # Evaluate and save every 50 epochs
    if (epoch + 1) % 50 == 0:
        print(f"\nEpoch {epoch+1}/{epochs}:")
        print(f"  Critic Loss: {C_losses[-1]:.4f}")
        print(f"  Generator Loss: {G_losses[-1]:.4f}")
        print(f"  Wasserstein Distance: {wasserstein_distances[-1]:.4f}")

        # Generate samples for a few different proteases
        print("\nSample generated sequences for different proteases:")
        for i in range(min(3, num_proteases)):
            sequences, protease_name = generate_sequences(G, protease_idx=i, num_samples=2)
            print(f"\n{protease_name}:")
            for seq in sequences:
                print(f"  {' '.join(seq)}")
        print("-" * 60)

# =====================
# Plot losses and Wasserstein distance
# =====================
fig, axes = plt.subplots(1, 2, figsize=(15, 5))

# Loss plot
axes[0].plot(C_losses, label="Critic Loss", alpha=0.7)
axes[0].plot(G_losses, label="Generator Loss", alpha=0.7)
axes[0].set_xlabel("Epoch")
axes[0].set_ylabel("Loss")
axes[0].legend()
axes[0].set_title("WGAN-GP Training Losses")
axes[0].grid(True, alpha=0.3)

# Wasserstein distance plot (should decrease and stabilize)
axes[1].plot(wasserstein_distances, label="Wasserstein Distance", color='green', alpha=0.7)
axes[1].set_xlabel("Epoch")
axes[1].set_ylabel("Distance")
axes[1].legend()
axes[1].set_title("Wasserstein Distance Over Training")
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("wgan_gp_training_plots.png")
print("\nTraining plots saved as 'wgan_gp_training_plots.png'")
plt.show()

# =====================
# Save final models
# =====================
save_models(G, C)

# =====================
# Generate samples for all proteases
# =====================
print("\nFinal generated sequences for all proteases:")
for i in range(num_proteases):
    sequences, protease_name = generate_sequences(G, protease_idx=i, num_samples=5)
    print(f"\n{protease_name}:")
    for seq in sequences:
        print(f"  {' '.join(seq)}")

print("\n" + "=" * 60)
print("WGAN-GP Training completed.")
print("=" * 60)
print("\nKey differences from vanilla GAN:")
print("1. Critic outputs raw scores (not probabilities)")
print("2. Wasserstein loss instead of BCE loss")
print("3. Gradient penalty for Lipschitz constraint")
print("4. 5 critic updates per generator update")
print("5. More stable training and better convergence")
