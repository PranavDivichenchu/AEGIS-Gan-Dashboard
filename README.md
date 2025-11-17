# Sepsis Protease Inhibitor Design using GANs and Molecular Docking

A computational drug design pipeline using Generative Adversarial Networks (GANs) to generate novel peptide inhibitors for sepsis-related proteases, validated through molecular docking simulations.

## Overview

This project addresses the critical challenge of designing effective protease inhibitors for sepsis treatment by combining machine learning with computational chemistry. The pipeline integrates three key technologies:

1. **Generative Adversarial Networks (GANs)** - Generate novel peptide sequences
2. **ESMFold Structure Prediction** - Predict 3D peptide structures
3. **AutoDock Vina Molecular Docking** - Evaluate binding affinity to target proteases

## Motivation

Sepsis is a life-threatening condition characterized by dysregulated protease activity. Current treatments are limited, and developing new protease inhibitors through traditional methods is time-consuming and expensive. This project demonstrates that machine learning can accelerate the early stages of drug discovery by computationally screening millions of potential inhibitor candidates.

## Key Features

- **Three GAN Architectures**: Implemented and compared SupremeGAN (novel architecture), Conditional GAN, and WGAN-GP
- **27 Target Proteases**: Covers major sepsis-related proteases across 4 classes (Caspases, MMPs, Serine proteases, Cysteine proteases)
- **Ensemble Approach**: Strategic selection combining strengths of multiple GAN models
- **Drug-likeness Assessment**: ADMET analysis and druglikeness scoring for therapeutic viability
- **Inhibitor Design**: Protease class-specific chemical modifications with warhead strategies
- **Budget-Optimized Validation**: Practical experimental protocols within research constraints

## Results

### GAN Performance
- **781 total docking simulations** across both GAN models
- **ConditionalGAN**: Mean binding affinity -7.25 kcal/mol, 23 excellent binders (<-10 kcal/mol)
- **SupremeGAN**: Mean binding affinity -7.18 kcal/mol, 5 excellent binders (<-10 kcal/mol)
- Statistical analysis validated ensemble approach (p > 0.05)

### 27-Peptide Inhibitor Panel
- **Best peptide selected per protease** regardless of source model
- **Binding affinity range**: -11.88 to -4.93 kcal/mol
- **Top candidates**:
  - Panel #14 (MMP1): -11.88 kcal/mol
  - Panel #24 (Proteinase 3): -11.14 kcal/mol
  - Panel #13 (Kallikrein 2): -9.72 kcal/mol
- **67% of peptides** have favorable druglikeness scores (≥60/100)

### Inhibitor Modifications
Each peptide designed with three versions:
- **Basic**: N-acetylation + C-amidation (Ac-peptide-NH2)
- **Enhanced**: Class-specific warheads (aldehydes, boronic acids, hydroxamates)
- **Cyclic**: Conformational constraint for stability

## Project Structure

```
├── ConditionalGAN.py              # Conditional GAN implementation
├── SupremeGAN.py                  # Novel GAN architecture with advanced techniques
├── WGAN_GP.py                     # Wasserstein GAN with gradient penalty
├── design_inhibitors.py           # Generate peptide sequences from trained models
├── predict_structures.py          # ESMFold structure prediction
├── molecular_docking.py           # AutoDock Vina docking simulations
├── run_docking_pipeline.py        # End-to-end pipeline execution
├── compare_docking_results.py     # Statistical GAN comparison
├── create_27_peptide_panel.py     # Ensemble peptide selection
├── design_peptide_inhibitors.py   # Inhibitor modification design
├── analyze_27_panel_druglikeness.py  # ADMET analysis
├── budget_synthesis_plan.py       # Experimental validation planning
├── docking_results/               # Results and analysis
│   ├── 27_peptide_panel.csv
│   ├── 27_panel_inhibitor_designs.csv
│   └── plots/
└── generated_sequences/           # GAN-generated peptides
```

## Installation

### Requirements
```bash
# Python 3.8+
pip install torch torchvision
pip install biopython rdkit pandas numpy scipy matplotlib seaborn
pip install requests  # For ESMFold API

# AutoDock Vina
# Download from: http://vina.scripps.edu/
```

### Dataset
The project uses the MEROPS database of protease substrates and cleavage sites:
- `MEROPS_sepsis_expanded_dataset.csv` - Preprocessed training data
- Includes substrate sequences, cleavage sites, and protease annotations

### Protease Structures
PDB structures for 27 sepsis-related proteases are required for docking:
- Download from RCSB PDB database
- Pre-process using `prepare_protease_structures.py`

## Usage

### 1. Train GAN Models
```bash
# Train Conditional GAN
python ConditionalGAN.py

# Train SupremeGAN
python SupremeGAN.py

# Train WGAN-GP
python WGAN_GP.py
```

### 2. Generate Peptide Sequences
```bash
python design_inhibitors.py --model supremegan --num_sequences 100
```

### 3. Run Complete Pipeline
```bash
python run_docking_pipeline.py --model_type supremegan
```

This executes:
1. Peptide sequence generation
2. 3D structure prediction via ESMFold
3. Molecular docking with AutoDock Vina
4. Results analysis and visualization

### 4. Compare Models
```bash
python compare_docking_results.py
```

### 5. Create Final Panel
```bash
python create_27_peptide_panel.py
```

### 6. Design Inhibitors
```bash
python design_peptide_inhibitors.py
```

## GAN Architectures

### SupremeGAN (Novel)
Advanced architecture incorporating:
- **Spectral Normalization**: Stabilizes discriminator training
- **Self-Attention Layers**: Captures long-range dependencies in sequences
- **Gradient Penalty**: Prevents mode collapse
- **Conditional Batch Normalization**: Protease-specific generation

### Conditional GAN
- Protease-conditioned generation
- Ensures target-specific peptide design
- Label embedding for protease type

### WGAN-GP
- Wasserstein distance loss
- Gradient penalty for Lipschitz constraint
- Improved training stability

## Drug-likeness Assessment

Each peptide evaluated on:
- **Molecular Weight**: 689-1167 Da range
- **Hydrophobicity (GRAVY score)**: Balance for membrane permeability
- **Net Charge**: pH 7 considerations
- **H-bond donors/acceptors**: Binding potential
- **Aromatic content**: Binding interactions
- **Instability index**: Degradation resistance

Scoring system: 0-100 scale combining all factors

## Experimental Validation Strategy

**Recommended Proof-of-Concept**: Panel #13 (Kallikrein 2)
- **Sequence**: EGSCYGTE
- **Binding Affinity**: -9.72 kcal/mol (computational prediction)
- **Modifications**:
  1. Unmodified (control): EGSCYGTE
  2. Basic inhibitor: Ac-EGSCYGTE-NH2
- **Cost**: ~$280 for synthesis (1-2 mg each, ≥95% purity)
- **Testing**: Fluorescence-based competitive inhibition assay
- **Expected outcome**: Modified version shows >>100x better inhibition

## Future Directions

1. **Experimental Validation**: Synthesize and test top candidates
2. **Extended GAN Training**: Larger datasets and longer training on cloud infrastructure
3. **Molecular Dynamics**: Validate binding stability over time
4. **Lead Optimization**: Structure-activity relationship (SAR) studies
5. **In Vivo Studies**: If in vitro validation is successful
6. **Broader Applications**: Extend to other disease-related proteases

## Technical Details

### Computational Performance
- **ESMFold API**: ~10-15 seconds per structure
- **Docking**: ~5-8 seconds per peptide-protease pair
- **Full pipeline**: ~6-8 hours for 100 peptides × 27 proteases
- **Hardware**: Runs on standard laptop (M-series Mac or x86 with GPU recommended)

### Protease Classes Covered
- **Caspases** (6 targets): Apoptosis regulators
- **Matrix Metalloproteinases** (6 targets): Tissue remodeling
- **Serine Proteases** (13 targets): Coagulation cascade, complement system
- **Cysteine Proteases** (2 targets): Viral proteases

## Limitations

- Computational predictions require experimental validation
- Peptides may function as substrates rather than inhibitors without chemical modifications
- In vitro binding ≠ in vivo efficacy
- ADMET predictions are estimates, not experimental measurements
- Budget constraints limit comprehensive experimental validation

## References

Key methodologies and tools:
- **MEROPS Database**: Protease substrate database
- **ESMFold**: Meta AI protein structure prediction
- **AutoDock Vina**: Molecular docking software
- **RCSB PDB**: Protein structure database

## Acknowledgments

This project was conducted as part of independent research at the Academy of Engineering and Technology (AET), Loudoun County Public Schools.

## License

This project is for academic and research purposes.

## Contact

For questions or collaboration inquiries, please open an issue on this repository.

---

**Last Updated**: November 2025
**Status**: Computational design complete, experimental validation in planning phase
