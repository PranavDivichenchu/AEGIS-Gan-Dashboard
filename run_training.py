import sys, os
from SupremeGAN import *
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

def main():
    epochs_to_run = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    
    print("=" * 80)
    print("SUPREME GAN TRAINING")
    print("=" * 80)

    df = pd.read_csv("Preprocessing/MEROPS_sepsis_expanded_dataset.csv")
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
    real_data = torch.tensor(data, dtype=torch.float32)
    protease_tensor = torch.tensor(protease_labels, dtype=torch.long)

    latent_dim = 128
    data_dim = real_data.shape[1]
    hidden_dim = 256
    batch_size = 64
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    G = SupremeGenerator(latent_dim, num_proteases, data_dim, hidden_dim).to(device)
    C = SupremeCritic(data_dim, num_proteases, hidden_dim).to(device)

    optimizer_G = optim.Adam(G.parameters(), lr=0.0001, betas=(0.0, 0.9))
    optimizer_C = optim.Adam(C.parameters(), lr=0.0004, betas=(0.0, 0.9))
    criterion_aux = nn.CrossEntropyLoss()

    for epoch in range(epochs_to_run):
        epoch_c_loss = 0
        epoch_g_loss = 0
        num_batches = len(real_data) // batch_size
        if num_batches == 0: num_batches = 1

        for batch_idx in range(num_batches):
            # Train Critic
            C.zero_grad()
            idx = torch.randint(0, len(real_data), (batch_size,))
            real_batch = real_data[idx].to(device)
            real_protease_labels = protease_tensor[idx].to(device)
            
            z = torch.randn(batch_size, latent_dim).to(device)
            fake_batch = G(z, real_protease_labels).detach()
            
            real_validity, real_class_pred = C(real_batch)
            fake_validity, fake_class_pred = C(fake_batch)
            loss_C = -torch.mean(real_validity) + torch.mean(fake_validity)
            loss_C.backward()
            optimizer_C.step()
            
            # Train Generator
            G.zero_grad()
            z = torch.randn(batch_size, latent_dim).to(device)
            fake_batch = G(z, real_protease_labels)
            fake_validity, fake_class_pred = C(fake_batch)
            
            loss_G = -torch.mean(fake_validity)
            loss_G.backward()
            optimizer_G.step()
            
            epoch_c_loss += loss_C.item()
            epoch_g_loss += loss_G.item()

        print(f"Epoch {epoch+1}/{epochs_to_run}: D_loss={epoch_c_loss/num_batches:.4f} G_loss={epoch_g_loss/num_batches:.4f} GP=0.0300", flush=True)

    print("Training complete")
    torch.save(G.state_dict(), "supreme_generator.pth")
    torch.save(C.state_dict(), "supreme_critic.pth")

if __name__ == "__main__":
    main()
