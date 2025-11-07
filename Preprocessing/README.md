# Sepsis Protease GAN-Based Inhibitor Discovery

> AI-driven peptide generation and molecular docking for discovering protease inhibitors targeting sepsis

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-ee4c2c.svg)](https://pytorch.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

This project combines **Generative Adversarial Networks (GANs)** with **molecular docking** to discover novel peptide-based protease inhibitors for sepsis treatment. We generate peptide sequences using state-of-the-art GANs and evaluate their binding affinity to 29 sepsis-related proteases using computational docking.

### Key Features

- 🧬 **Three GAN Architectures**: SupremeGAN, ConditionalGAN, and WGAN-GP
- 🎯 **29 Target Proteases**: Including neutrophil elastase, MMPs, caspases, and coagulation factors
- 🔬 **Complete Docking Pipeline**: From sequence generation to binding affinity analysis
- 📊 **Automated Analysis**: Comprehensive visualization and ranking of results
- ⚡ **Scalable**: Process thousands of peptide-protease interactions

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    GAN Training & Generation                     │
│  SupremeGAN / ConditionalGAN / WGAN-GP → Generate 8-mer Peptides│
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ↓
┌─────────────────────────────────────────────────────────────────┐
│              Structure Prediction (ESMFold)                      │
│        Generate 3D structures for peptide sequences              │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ↓
┌─────────────────────────────────────────────────────────────────┐
│         Protease Preparation (PDB Database)                      │
│    Download & prepare 29 protease structures from RCSB PDB      │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ↓
┌─────────────────────────────────────────────────────────────────┐
│            Molecular Docking (AutoDock Vina)                     │
│      Dock peptides to proteases & calculate binding affinity    │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ↓
┌─────────────────────────────────────────────────────────────────┐
│              Analysis & Visualization                            │
│    Rank by affinity, generate plots, identify top binders       │
└─────────────────────────────────────────────────────────────────┘
```

## Target Proteases

We target 29 proteases implicated in sepsis pathophysiology:

| Category | Proteases |
|----------|-----------|
| **Neutrophil Serine Proteases** | Elastase (ELANE), Proteinase 3, Cathepsin G |
| **Matrix Metalloproteinases** | MMP1, MMP2, MMP7, MMP8, MMP9, MMP12 |
| **Coagulation Factors** | Thrombin, Factor VIIa, Factor IXa, Factor Xa |
| **Fibrinolytic** | Plasmin, tPA, Urokinase |
| **Caspases** | Caspase-1, 3, 6, 7, 8, 9 |
| **Kallikreins** | Kallikrein 1, Kallikrein 2 |
| **Others** | Granzyme B, NSP1, NSP2 |

## GAN Architectures

### 1. SupremeGAN (Recommended)
Advanced architecture featuring:
- Self-attention mechanism for long-range dependencies
- Spectral normalization for training stability
- Conditional batch normalization
- Auxiliary classifier for protease specificity
- Diversity loss to prevent mode collapse

**Training Metrics** (Epoch 250/400):
- Auxiliary Accuracy: 29.84% (8.7× better than random)
- Diversity Score: 0.88 (excellent variation)
- Wasserstein Distance: -0.06 (strong convergence)

### 2. ConditionalGAN
- Class-conditional generation
- Label embedding for protease targeting
- BatchNorm and LeakyReLU activation
- BCE loss with Adam optimizer

### 3. WGAN-GP
- Wasserstein loss with gradient penalty
- Critic architecture for stable training
- No sigmoid/log-loss functions

## Installation

### Prerequisites

```bash
# Clone the repository
git clone https://github.com/PranavDivichenchu/sepsis-protease-gan-docking.git
cd sepsis-protease-gan-docking

# Install Miniconda (if not already installed)
brew install miniconda
conda init zsh  # or bash

# Create conda environment with Python 3.12
conda create -n docking python=3.12 -y
conda activate docking

# Install AutoDock Vina
conda install -c conda-forge vina -y

# Install Python dependencies
pip install torch pandas scikit-learn matplotlib seaborn requests beautifulsoup4 biopython
```

### Optional Tools

```bash
# AutoDock Tools (for PDBQT conversion)
conda install -c bioconda mgltools

# OpenBabel (alternative converter)
conda install -c conda-forge openbabel

# Local ESMFold (for faster structure prediction)
pip install fair-esm[esmfold]
```

## Usage

### Quick Start: Complete Pipeline

Run the entire pipeline with one command:

```bash
conda activate docking
python run_docking_pipeline.py --model supreme
```

This will:
1. Generate 100 sequences per protease (2,900 total)
2. Download 29 protease structures from PDB
3. Predict 3D structures using ESMFold
4. Perform molecular docking
5. Generate analysis reports

### Test Run (Recommended First)

Start with a small test to validate everything works:

```bash
python run_docking_pipeline.py \
  --model supreme \
  --sequences 5 \
  --max-predictions 10 \
  --max-dockings 10
```

### Individual Pipeline Steps

#### 1. Generate Sequences

```bash
python generate_sequences.py
```

Outputs:
- `generated_sequences/supremegan_sequences.csv`
- `generated_sequences/supremegan_sequences.fasta`

#### 2. Prepare Protease Structures

```bash
python prepare_protease_structures.py
```

Outputs:
- `protease_structures/raw/` - Downloaded PDB files
- `protease_structures/prepared/` - Cleaned structures
- `protease_structures/structure_summary.csv`

#### 3. Predict Peptide Structures

```bash
python predict_structures.py --input generated_sequences/supremegan_sequences.csv
```

Outputs:
- `predicted_structures/pdb_files/` - 3D structures
- `predicted_structures/prediction_results_*.csv`

#### 4. Molecular Docking

```bash
python molecular_docking.py \
  --peptides predicted_structures/prediction_results_supremegan_sequences.csv \
  --proteases protease_structures/structure_summary.csv
```

Outputs:
- `docking_results/docking_results.csv`
- `docking_results/vina_results/` - Docked poses

#### 5. Analyze Results

```bash
python analyze_docking_results.py --results docking_results/docking_results.csv
```

Outputs:
- `docking_analysis/ranked_results.csv` - All results ranked by affinity
- `docking_analysis/top_binders.csv` - Top 3 per protease
- `docking_analysis/*.png` - Visualizations
- `docking_analysis/statistics.json` - Summary statistics

## Results Interpretation

### Binding Affinity (kcal/mol)

| Range | Interpretation |
|-------|----------------|
| < -11 | Very strong binding |
| -9 to -11 | Strong binding |
| -7 to -9 | Good binding |
| -5 to -7 | Moderate binding |
| > -5 | Weak binding |

**Note**: More negative = stronger binding

### Output Files

- **`ranked_results.csv`**: All dockings sorted by binding affinity
- **`top_binders.csv`**: Best candidates for each protease
- **`affinity_distribution.png`**: Overall binding affinity histogram
- **`per_protease_comparison.png`**: Affinity comparison across proteases
- **`top_binders_heatmap.png`**: Visual matrix of top binders
- **`sequence_analysis.png`**: Amino acid composition analysis

## Project Structure

```
sepsis-protease-gan-docking/
├── README.md                           # This file
├── DOCKING_PIPELINE_README.md          # Detailed pipeline documentation
├── .gitignore                          # Git ignore rules
│
├── ConditionalGAN.py                   # ConditionalGAN implementation
├── SupremeGAN.py                       # SupremeGAN implementation
├── WGAN_GP.py                          # WGAN-GP implementation
├── compare_all_gans.py                 # GAN comparison tool
│
├── generate_sequences.py               # Sequence generation from GANs
├── prepare_protease_structures.py      # PDB structure preparation
├── predict_structures.py               # ESMFold structure prediction
├── molecular_docking.py                # AutoDock Vina docking
├── analyze_docking_results.py          # Results analysis & visualization
├── run_docking_pipeline.py             # Main orchestration script
│
├── DataCollection.py                   # MEROPS data scraping
├── IntialModel.py                      # Initial baseline GAN
└── JournalEntries/                     # Research journal
```

## Training Your Own GANs

### SupremeGAN Training

```bash
python SupremeGAN.py
```

Key hyperparameters:
- Latent dimension: 128
- Hidden dimension: 256
- Batch size: 64
- Learning rates: G=0.0001, D=0.0004
- Epochs: 400
- Gradient penalty weight: 10

### ConditionalGAN Training

```bash
python ConditionalGAN.py
```

Faster training, simpler architecture, good baseline results.

### WGAN-GP Training

```bash
python WGAN_GP.py
```

Stable training with Wasserstein distance metric.

## Performance & Scaling

### Time Estimates (100 sequences/protease)

| Step | Time | Notes |
|------|------|-------|
| Sequence Generation | ~1 min | Fast |
| Protease Preparation | ~5-10 min | One-time download |
| Structure Prediction | ~4-8 hours | ESMFold API with rate limiting |
| Docking | ~5-10 hours | Depends on exhaustiveness |
| Analysis | ~1-2 min | Fast |
| **Total** | **~10-18 hours** | For full pipeline |

### Optimization Tips

1. **Use local ESMFold** (requires GPU) - 10x faster structure prediction
2. **Process in batches** - Use `--max-predictions` and `--max-dockings`
3. **Skip completed steps** - Use `--skip` flag to resume
4. **Parallelize docking** - Modify code for multiprocessing

## Scientific Background

### Why GANs for Drug Discovery?

- **Explore chemical space**: Generate novel sequences beyond training data
- **Target specificity**: Conditional generation for specific proteases
- **Diversity**: Avoid mode collapse to explore varied candidates
- **Speed**: Generate thousands of candidates in minutes

### Why These Proteases?

Sepsis involves dysregulated protease activity:
- **Neutrophil proteases**: Tissue damage, inflammation
- **MMPs**: ECM degradation, organ dysfunction
- **Coagulation cascade**: DIC, microvascular thrombosis
- **Caspases**: Apoptosis, immune cell death

Inhibiting these proteases may reduce sepsis mortality.

## Citation

If you use this code in your research, please cite:

```bibtex
@software{divichenchu2025sepsis,
  author = {Divichenchu, Pranav},
  title = {Sepsis Protease GAN-Based Inhibitor Discovery},
  year = {2025},
  url = {https://github.com/PranavDivichenchu/sepsis-protease-gan-docking}
}
```

## References

### Tools & Methods

- **ESMFold**: Lin et al., "Language models of protein sequences at the scale of evolution enable accurate structure prediction" (2022)
- **AutoDock Vina**: Trott & Olson, "AutoDock Vina: improving the speed and accuracy of docking" (2010)
- **MEROPS Database**: Rawlings et al., "The MEROPS database of proteolytic enzymes" (2018)
- **WGAN-GP**: Gulrajani et al., "Improved Training of Wasserstein GANs" (2017)
- **SA-GAN**: Zhang et al., "Self-Attention Generative Adversarial Networks" (2019)

## License

MIT License - see LICENSE file for details

## Acknowledgments

- RCSB Protein Data Bank for protease structures
- MEROPS database for substrate specificity data
- ESMFold team for structure prediction API
- AutoDock Vina developers

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## Contact

**Pranav Divichenchu**
- GitHub: [@PranavDivichenchu](https://github.com/PranavDivichenchu)
- Repository: [sepsis-protease-gan-docking](https://github.com/PranavDivichenchu/sepsis-protease-gan-docking)

---

**⚠️ Disclaimer**: This is a computational research tool. Any peptide candidates require extensive experimental validation before clinical consideration.
