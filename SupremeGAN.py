import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
import numpy as np
import matplotlib.pyplot as plt
import os
from torch.nn.utils import spectral_norm

# =====================
# Advanced Building Blocks
# =====================

class SelfAttention(nn.Module):
    """
    Self-attention mechanism for capturing long-range dependencies.
    Adapted from SA-GAN (Zhang et al., 2019)
    """
    def __init__(self, in_dim):
        super().__init__()
        self.query = spectral_norm(nn.Linear(in_dim, in_dim // 8))
        self.key = spectral_norm(nn.Linear(in_dim, in_dim // 8))
        self.value = spectral_norm(nn.Linear(in_dim, in_dim))
        self.gamma = nn.Parameter(torch.zeros(1))  # Learnable weight

    def forward(self, x):
        batch_size = x.size(0)

        # Compute attention
        query = self.query(x)  # [B, in_dim//8]
        key = self.key(x)      # [B, in_dim//8]
        value = self.value(x)  # [B, in_dim]

        # Attention scores
        attention = torch.matmul(query, key.transpose(0, 1))  # [B, B]
        attention = F.softmax(attention, dim=-1)

        # Apply attention to values
        out = torch.matmul(attention, value)  # [B, in_dim]

        # Residual connection with learnable weight
        out = self.gamma * out + x
        return out

class ConditionalBatchNorm1d(nn.Module):
    """
    Conditional Batch Normalization (from BigGAN).
    Modulates normalization parameters based on class label.
    """
    def __init__(self, num_features, num_classes):
        super().__init__()
        self.num_features = num_features
        self.bn = nn.BatchNorm1d(num_features, affine=False)

        # Learnable scale and bias for each class
        self.embed_gamma = nn.Embedding(num_classes, num_features)
        self.embed_beta = nn.Embedding(num_classes, num_features)

        # Initialize
        self.embed_gamma.weight.data.fill_(1.0)
        self.embed_beta.weight.data.zero_()

    def forward(self, x, y):
        out = self.bn(x)
        gamma = self.embed_gamma(y)
        beta = self.embed_beta(y)
        out = gamma * out + beta
        return out

class ResidualBlock(nn.Module):
    """
    Residual block with conditional batch norm for generator.
    """
    def __init__(self, dim, num_classes):
        super().__init__()
        self.fc1 = spectral_norm(nn.Linear(dim, dim))
        self.fc2 = spectral_norm(nn.Linear(dim, dim))
        self.cbn1 = ConditionalBatchNorm1d(dim, num_classes)
        self.cbn2 = ConditionalBatchNorm1d(dim, num_classes)
        self.activation = nn.LeakyReLU(0.2)

    def forward(self, x, labels):
        residual = x

        out = self.cbn1(x, labels)
        out = self.activation(out)
        out = self.fc1(out)

        out = self.cbn2(out, labels)
        out = self.activation(out)
        out = self.fc2(out)

        return out + residual

# =====================
# Supreme Generator
# =====================
class SupremeGenerator(nn.Module):
    """
    Advanced generator with:
    - Spectral normalization
    - Self-attention
    - Conditional batch normalization
    - Residual connections
    - Progressive complexity
    """
    def __init__(self, latent_dim, num_classes, data_dim, hidden_dim):
        super().__init__()

        # Initial projection
        self.fc_initial = spectral_norm(nn.Linear(latent_dim, hidden_dim))

        # Residual blocks with conditional batch norm
        self.res_block1 = ResidualBlock(hidden_dim, num_classes)
        self.res_block2 = ResidualBlock(hidden_dim, num_classes)

        # Self-attention for capturing dependencies
        self.attention = SelfAttention(hidden_dim)

        # Additional layers
        self.fc_mid = spectral_norm(nn.Linear(hidden_dim, hidden_dim))
        self.cbn_mid = ConditionalBatchNorm1d(hidden_dim, num_classes)

        # Final projection
        self.fc_out = spectral_norm(nn.Linear(hidden_dim, data_dim))

        self.activation = nn.LeakyReLU(0.2)

    def forward(self, z, labels):
        # Initial projection
        x = self.fc_initial(z)
        x = self.activation(x)

        # Residual blocks with conditional normalization
        x = self.res_block1(x, labels)
        x = self.res_block2(x, labels)

        # Self-attention
        x = self.attention(x)

        # Middle layer
        x = self.cbn_mid(x, labels)
        x = self.activation(x)
        x = self.fc_mid(x)
        x = self.activation(x)

        # Output
        x = self.fc_out(x)

        return x

# =====================
# Supreme Critic (Multi-task)
# =====================
class SupremeCritic(nn.Module):
    """
    Advanced critic with:
    - Spectral normalization
    - Self-attention
    - Multi-task: real/fake prediction + class classification
    - Multi-scale discrimination
    """
    def __init__(self, data_dim, num_classes, hidden_dim):
        super().__init__()

        # Input layers
        self.fc1 = spectral_norm(nn.Linear(data_dim, hidden_dim))
        self.fc2 = spectral_norm(nn.Linear(hidden_dim, hidden_dim))

        # Self-attention
        self.attention = SelfAttention(hidden_dim)

        # Additional layers
        self.fc3 = spectral_norm(nn.Linear(hidden_dim, hidden_dim))
        self.fc4 = spectral_norm(nn.Linear(hidden_dim, hidden_dim))

        # Output heads
        self.fc_validity = spectral_norm(nn.Linear(hidden_dim, 1))  # Real/fake
        self.fc_class = spectral_norm(nn.Linear(hidden_dim, num_classes))  # Protease class

        self.activation = nn.LeakyReLU(0.2)
        self.dropout = nn.Dropout(0.3)

    def forward(self, x):
        # Feature extraction
        x = self.activation(self.fc1(x))
        x = self.dropout(x)

        x = self.activation(self.fc2(x))
        x = self.dropout(x)

        # Self-attention
        x = self.attention(x)

        x = self.activation(self.fc3(x))
        x = self.dropout(x)

        x = self.activation(self.fc4(x))

        # Multi-task outputs
        validity = self.fc_validity(x)
        class_pred = self.fc_class(x)

        return validity, class_pred

# =====================
# Advanced Loss Functions
# =====================

def compute_gradient_penalty(critic, real_samples, fake_samples, device):
    """Gradient penalty for WGAN-GP"""
    batch_size = real_samples.size(0)
    alpha = torch.rand(batch_size, 1).to(device)
    interpolates = (alpha * real_samples + (1 - alpha) * fake_samples).requires_grad_(True)

    validity, _ = critic(interpolates)

    gradients = torch.autograd.grad(
        outputs=validity,
        inputs=interpolates,
        grad_outputs=torch.ones_like(validity),
        create_graph=True,
        retain_graph=True,
        only_inputs=True
    )[0]

    gradients = gradients.view(batch_size, -1)
    gradient_penalty = ((gradients.norm(2, dim=1) - 1) ** 2).mean()
    return gradient_penalty

def diversity_loss(generated_samples):
    """
    Diversity loss to prevent mode collapse.
    Encourages generated samples to be different from each other.
    """
    # Pairwise distances
    batch_size = generated_samples.size(0)
    if batch_size < 2:
        return torch.tensor(0.0).to(generated_samples.device)

    # Normalize samples
    normalized = F.normalize(generated_samples, p=2, dim=1)

    # Compute similarity matrix
    similarity = torch.matmul(normalized, normalized.t())

    # Penalize high similarity (want diversity)
    # Exclude diagonal (self-similarity)
    mask = torch.ones_like(similarity) - torch.eye(batch_size).to(similarity.device)
    diversity_penalty = (similarity * mask).sum() / (batch_size * (batch_size - 1))

    return diversity_penalty

def consistency_regularization(generator, z, labels, device):
    """
    Consistency regularization: small changes in input should produce small changes in output.
    Improves robustness and generalization.
    """
    with torch.no_grad():
        # Original output
        output1 = generator(z, labels)

    # Add small noise to latent
    noise = torch.randn_like(z) * 0.05
    z_perturbed = z + noise

    # Perturbed output
    output2 = generator(z_perturbed, labels)

    # Penalize large changes
    consistency_loss = F.mse_loss(output1, output2)

    return consistency_loss

# =====================
# Generation function
# =====================
def generate_sequences(G, protease_encoder, encoders, scaler, sequence_cols, latent_dim, device, protease_name=None, protease_idx=None, num_samples=10):
    """Generate sequences with the trained generator"""
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
# Save/load utilities
# =====================
def save_models(generator, critic, gen_path="supreme_generator.pth", critic_path="supreme_critic.pth"):
    torch.save(generator.state_dict(), gen_path)
    torch.save(critic.state_dict(), critic_path)
    print(f"Models saved to {gen_path} and {critic_path}")

def load_models(generator, critic, gen_path="supreme_generator.pth", critic_path="supreme_critic.pth"):
    if os.path.exists(gen_path) and os.path.exists(critic_path):
        generator.load_state_dict(torch.load(gen_path, map_location=device))
        critic.load_state_dict(torch.load(critic_path, map_location=device))
        print(f"Models loaded from {gen_path} and {critic_path}")
        return True
    return False

if __name__ == "__main__":
    # =====================
    # Data Loading and Setup
    # =====================
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

    # =====================
    # Hyperparameters
    # =====================
    latent_dim = 128
    data_dim = real_data.shape[1]
    hidden_dim = 256
    batch_size = 64
    lr_g = 0.0001
    lr_d = 0.0004
    epochs = 400
    n_critic = 3
    lambda_gp = 10
    lambda_aux = 1.0
    lambda_diversity = 0.1
    lambda_consistency = 0.5
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    print(f"Using device: {device}")
    print(f"Batch size: {batch_size}, Latent dim: {latent_dim}")

    # =====================
    # Initialize models
    # =====================
    G = SupremeGenerator(latent_dim, num_proteases, data_dim, hidden_dim).to(device)
    C = SupremeCritic(data_dim, num_proteases, hidden_dim).to(device)

    print(f"\nGenerator parameters: {sum(p.numel() for p in G.parameters()):,}")
    print(f"Critic parameters: {sum(p.numel() for p in C.parameters()):,}")

    # =====================
    # Optimizers
    # =====================
    optimizer_G = optim.Adam(G.parameters(), lr=lr_g, betas=(0.0, 0.9))
    optimizer_C = optim.Adam(C.parameters(), lr=lr_d, betas=(0.0, 0.9))

    scheduler_G = optim.lr_scheduler.ExponentialLR(optimizer_G, gamma=0.99)
    scheduler_C = optim.lr_scheduler.ExponentialLR(optimizer_C, gamma=0.99)

    criterion_aux = nn.CrossEntropyLoss()

    # =====================
    # Tracking metrics
    # =====================
    G_losses, C_losses = [], []
    wasserstein_distances = []
    aux_accuracies = []
    diversity_scores = []

    # Try to load existing models
    if not load_models(G, C):
        print("No saved models found, training from scratch.\n")

    # =====================
    # Training Loop
    # =====================
    print("=" * 80)
    print("SUPREME GAN TRAINING")
    print("=" * 80)
    print("Advanced features enabled:")
    print("  ✓ Wasserstein loss with gradient penalty")
    print("  ✓ Self-attention mechanism")
    print("  ✓ Spectral normalization")
    print("  ✓ Auxiliary classifier (AC-GAN)")
    print("  ✓ Diversity loss")
    print("  ✓ Consistency regularization")
    print("  ✓ Conditional batch normalization")
    print("  ✓ Residual connections")
    print("  ✓ Multi-task learning")
    print("=" * 80)
    print()
    
    for epoch in range(epochs):
        epoch_c_loss = 0
        epoch_g_loss = 0
        epoch_wd = 0
        epoch_aux_acc = 0
        epoch_diversity = 0
        num_batches = len(real_data) // batch_size
    
        for batch_idx in range(num_batches):
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
    
                # Critic predictions
                real_validity, real_class_pred = C(real_batch)
                fake_validity, fake_class_pred = C(fake_batch)
    
                # Wasserstein loss
                wasserstein_loss = -torch.mean(real_validity) + torch.mean(fake_validity)
    
                # Gradient penalty
                gp = compute_gradient_penalty(C, real_batch, fake_batch, device)
    
                # Auxiliary classifier loss (only on real data for stability)
                aux_loss_real = criterion_aux(real_class_pred, real_protease_labels)
    
                # Total critic loss
                loss_C = wasserstein_loss + lambda_gp * gp + lambda_aux * aux_loss_real
    
                loss_C.backward()
                optimizer_C.step()
    
                # Calculate auxiliary accuracy
                _, predicted = torch.max(real_class_pred.data, 1)
                aux_acc = (predicted == real_protease_labels).float().mean().item()
                epoch_aux_acc += aux_acc
    
            # ----- Train Generator (once) -----
            G.zero_grad()
    
            # Generate fake data
            z = torch.randn(batch_size, latent_dim).to(device)
            fake_batch = G(z, real_protease_labels)
    
            # Critic predictions
            fake_validity, fake_class_pred = C(fake_batch)
    
            # Generator adversarial loss
            adv_loss = -torch.mean(fake_validity)
    
            # Auxiliary classifier loss (generator should produce samples of correct class)
            aux_loss_fake = criterion_aux(fake_class_pred, real_protease_labels)
    
            # Diversity loss (prevent mode collapse)
            div_loss = diversity_loss(fake_batch)
    
            # Consistency regularization
            cons_loss = consistency_regularization(G, z, real_protease_labels, device)
    
            # Total generator loss
            loss_G = adv_loss + lambda_aux * aux_loss_fake + lambda_diversity * div_loss + lambda_consistency * cons_loss
    
            loss_G.backward()
            optimizer_G.step()
    
            # Track metrics
            epoch_c_loss += loss_C.item()
            epoch_g_loss += loss_G.item()
    
            with torch.no_grad():
                wd = torch.mean(real_validity).item() - torch.mean(fake_validity).item()
                epoch_wd += wd
                epoch_diversity += (1.0 - div_loss.item())  # Higher is better
    
        # Update learning rates
        scheduler_G.step()
        scheduler_C.step()
    
        # Record average metrics
        C_losses.append(epoch_c_loss / (num_batches * n_critic))
        G_losses.append(epoch_g_loss / num_batches)
        wasserstein_distances.append(epoch_wd / (num_batches * n_critic))
        aux_accuracies.append(epoch_aux_acc / (num_batches * n_critic))
        diversity_scores.append(epoch_diversity / num_batches)
    
        # Print progress
        if (epoch + 1) % 25 == 0:
            print(f"\nEpoch {epoch+1}/{epochs}:")
            print(f"  Critic Loss: {C_losses[-1]:.4f}")
            print(f"  Generator Loss: {G_losses[-1]:.4f}")
            print(f"  Wasserstein Distance: {wasserstein_distances[-1]:.4f}")
            print(f"  Auxiliary Accuracy: {aux_accuracies[-1]*100:.2f}%")
            print(f"  Diversity Score: {diversity_scores[-1]:.4f}")
            print(f"  Learning Rate (G): {scheduler_G.get_last_lr()[0]:.6f}")
    
            # Generate samples
            if (epoch + 1) % 50 == 0:
                print("\nSample sequences:")
                for i in range(min(2, num_proteases)):
                    sequences, protease_name = generate_sequences(G, protease_encoder, encoders, scaler, sequence_cols, latent_dim, device, protease_idx=i, num_samples=2)
                    print(f"\n{protease_name}:")
                    for seq in sequences:
                        print(f"  {' '.join(seq)}")
                print("-" * 80)
    
    # =====================
    # Plot comprehensive metrics
    # =====================
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    
    # Loss plot
    axes[0, 0].plot(C_losses, label="Critic Loss", alpha=0.7)
    axes[0, 0].plot(G_losses, label="Generator Loss", alpha=0.7)
    axes[0, 0].set_xlabel("Epoch")
    axes[0, 0].set_ylabel("Loss")
    axes[0, 0].legend()
    axes[0, 0].set_title("Training Losses")
    axes[0, 0].grid(True, alpha=0.3)
    
    # Wasserstein distance
    axes[0, 1].plot(wasserstein_distances, color='green', alpha=0.7)
    axes[0, 1].set_xlabel("Epoch")
    axes[0, 1].set_ylabel("Distance")
    axes[0, 1].set_title("Wasserstein Distance")
    axes[0, 1].grid(True, alpha=0.3)
    
    # Auxiliary accuracy
    axes[0, 2].plot(aux_accuracies, color='orange', alpha=0.7)
    axes[0, 2].set_xlabel("Epoch")
    axes[0, 2].set_ylabel("Accuracy")
    axes[0, 2].set_title("Protease Classification Accuracy")
    axes[0, 2].grid(True, alpha=0.3)
    
    # Diversity score
    axes[1, 0].plot(diversity_scores, color='purple', alpha=0.7)
    axes[1, 0].set_xlabel("Epoch")
    axes[1, 0].set_ylabel("Diversity Score")
    axes[1, 0].set_title("Sample Diversity (Higher is Better)")
    axes[1, 0].grid(True, alpha=0.3)
    
    # Loss ratio (should stabilize)
    loss_ratio = np.array(G_losses) / (np.array(C_losses) + 1e-8)
    axes[1, 1].plot(loss_ratio, color='red', alpha=0.7)
    axes[1, 1].set_xlabel("Epoch")
    axes[1, 1].set_ylabel("G Loss / C Loss")
    axes[1, 1].set_title("Loss Ratio (Balance Indicator)")
    axes[1, 1].grid(True, alpha=0.3)
    
    # Combined quality score
    quality_score = np.array(aux_accuracies) * np.array(diversity_scores)
    axes[1, 2].plot(quality_score, color='blue', alpha=0.7)
    axes[1, 2].set_xlabel("Epoch")
    axes[1, 2].set_ylabel("Quality Score")
    axes[1, 2].set_title("Overall Quality (Accuracy × Diversity)")
    axes[1, 2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("supreme_gan_training_metrics.png", dpi=150)
    print("\nComprehensive metrics saved as 'supreme_gan_training_metrics.png'")
    plt.show()
    
    # =====================
    # Save final models
    # =====================
    save_models(G, C)
    
    # =====================
    # Final evaluation
    # =====================
    print("\n" + "=" * 80)
    print("FINAL GENERATED SEQUENCES")
    print("=" * 80)

    for i in range(num_proteases):
        sequences, protease_name = generate_sequences(G, protease_encoder, encoders, scaler, sequence_cols, latent_dim, device, protease_idx=i, num_samples=5)
        print(f"\n{protease_name}:")
        for j, seq in enumerate(sequences, 1):
            print(f"  {j}. {' '.join(seq)}")
    
    print("\n" + "=" * 80)
    print("SupremeGAN Training Completed Successfully!")
    print("=" * 80)
    print("\nFinal Metrics:")
    print(f"  Final Wasserstein Distance: {wasserstein_distances[-1]:.4f}")
    print(f"  Final Auxiliary Accuracy: {aux_accuracies[-1]*100:.2f}%")
    print(f"  Final Diversity Score: {diversity_scores[-1]:.4f}")
    print(f"  Final Quality Score: {quality_score[-1]:.4f}")
    print("=" * 80)
