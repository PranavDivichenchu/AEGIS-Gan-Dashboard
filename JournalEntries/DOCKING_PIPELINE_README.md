# Molecular Docking Pipeline for GAN-Generated Peptides

Complete pipeline for evaluating GAN-generated peptide sequences against protease targets using molecular docking.

## Overview

This pipeline performs:
1. **Sequence Generation**: Generate peptide sequences from trained GAN models
2. **Structure Preparation**: Download and prepare protease structures from PDB
3. **Structure Prediction**: Predict 3D structures for peptides using ESMFold
4. **Molecular Docking**: Dock peptides to proteases using AutoDock Vina
5. **Analysis**: Analyze and visualize binding affinities

## Pipeline Components

### Scripts

- `generate_sequences.py` - Generate sequences from GANs (SupremeGAN, ConditionalGAN, WGAN-GP)
- `prepare_protease_structures.py` - Download and prepare protease structures from PDB
- `predict_structures.py` - Predict 3D structures using ESMFold API
- `molecular_docking.py` - Perform docking with AutoDock Vina
- `analyze_docking_results.py` - Analyze and visualize results
- `run_docking_pipeline.py` - **Main orchestration script**

### Target Proteases (29 total)

Sepsis-related proteases including:
- Neutrophil elastase, Proteinase 3, Cathepsin G
- MMPs (MMP1, MMP2, MMP7, MMP8, MMP9, MMP12)
- Coagulation factors (Thrombin, Factor VIIa, IXa, Xa)
- Caspases (Caspase-1, 3, 6, 7, 8, 9)
- Kallikreins, Granzyme B, tPA, Urokinase, and more

## Installation

### 1. Python Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install torch torchvision
pip install pandas numpy scikit-learn
pip install matplotlib seaborn
pip install requests beautifulsoup4
pip install biopython
```

### 2. AutoDock Vina

**Option A: Via Conda (Recommended)**
```bash
conda install -c conda-forge vina
```

**Option B: From Source**
Download from: https://github.com/ccsb-scripps/AutoDock-Vina/releases

### 3. AutoDock Tools (for PDBQT conversion)

```bash
conda install -c bioconda mgltools
```

**Alternative: OpenBabel**
```bash
conda install -c conda-forge openbabel
```

### 4. Optional: ESMFold (Local)

For local structure prediction (faster for many sequences):
```bash
pip install fair-esm[esmfold]
# Requires: PyTorch with GPU support
```

### 5. Optional Tools

**Reduce** (for adding hydrogens):
```bash
conda install -c bioconda reduce
```

**PyMOL** (for visualization):
```bash
conda install -c conda-forge pymol-open-source
```

## Usage

### Quick Start (Complete Pipeline)

Run the entire pipeline with one command:

```bash
python run_docking_pipeline.py --model supreme
```

This will:
1. Generate 100 sequences per protease using SupremeGAN (2,900 total)
2. Download 29 protease structures from PDB
3. Predict 3D structures for all peptides using ESMFold
4. Perform molecular docking for all peptide-protease pairs
5. Generate analysis reports and visualizations

### Test Run (Limited Data)

For testing or quick evaluation:

```bash
python run_docking_pipeline.py \
  --model supreme \
  --sequences 10 \
  --max-predictions 50 \
  --max-dockings 20
```

This generates only 10 sequences per protease and limits predictions/dockings.

### Using Different GAN Models

```bash
# Use ConditionalGAN
python run_docking_pipeline.py --model conditional

# Use WGAN-GP
python run_docking_pipeline.py --model wgan
```

### Skip Steps (Use Existing Data)

If you've already run some steps:

```bash
# Skip sequence generation and protease prep (use existing)
python run_docking_pipeline.py --skip 1 2

# Run only analysis on existing docking results
python run_docking_pipeline.py --skip 1 2 3 4
```

## Individual Script Usage

### 1. Generate Sequences

```bash
python generate_sequences.py
```

Output:
- `generated_sequences/supremegan_sequences.csv`
- `generated_sequences/supremegan_sequences.fasta`

### 2. Prepare Protease Structures

```bash
python prepare_protease_structures.py
```

Output:
- `protease_structures/raw/` - Downloaded PDB files
- `protease_structures/prepared/` - Cleaned structures
- `protease_structures/structure_summary.csv`
- `protease_structures/binding_sites.json`

### 3. Predict Structures

```bash
# Using ESMFold API
python predict_structures.py \
  --input generated_sequences/supremegan_sequences.csv

# Using local ESMFold (if installed)
python predict_structures.py \
  --input generated_sequences/supremegan_sequences.csv \
  --local

# Limit number of predictions
python predict_structures.py \
  --input generated_sequences/supremegan_sequences.csv \
  --max 100
```

Output:
- `predicted_structures/pdb_files/` - Predicted PDB structures
- `predicted_structures/prediction_results_*.csv`

### 4. Run Docking

```bash
python molecular_docking.py \
  --peptides predicted_structures/prediction_results_supremegan_sequences.csv \
  --proteases protease_structures/structure_summary.csv

# Limit number of dockings
python molecular_docking.py \
  --peptides predictions.csv \
  --proteases proteases.csv \
  --max 50
```

Output:
- `docking_results/pdbqt_files/` - Converted PDBQT files
- `docking_results/vina_results/` - Docking poses
- `docking_results/docking_results.csv`

### 5. Analyze Results

```bash
python analyze_docking_results.py \
  --results docking_results/docking_results.csv
```

Output:
- `docking_analysis/affinity_distribution.png`
- `docking_analysis/per_protease_comparison.png`
- `docking_analysis/top_binders_heatmap.png`
- `docking_analysis/sequence_analysis.png`
- `docking_analysis/ranked_results.csv`
- `docking_analysis/top_binders.csv`
- `docking_analysis/statistics.json`

## Output Interpretation

### Binding Affinity

- **Units**: kcal/mol
- **Range**: Typically -2 to -15 kcal/mol
- **Interpretation**:
  - More negative = Stronger binding
  - < -7 kcal/mol: Good binding affinity
  - < -9 kcal/mol: Strong binding affinity
  - < -11 kcal/mol: Very strong binding affinity

### Key Output Files

1. **ranked_results.csv**: All dockings ranked by affinity
2. **top_binders.csv**: Top 3 binders per protease
3. **statistics.json**: Overall and per-protease statistics
4. **Visualizations**: Distributions, comparisons, heatmaps

## Workflow Diagram

```
GAN Models (SupremeGAN/ConditionalGAN/WGAN-GP)
    ↓
Generate Sequences (8-mer peptides)
    ↓
ESMFold Structure Prediction
    ↓                              PDB Database
    ↓                                   ↓
    ↓                         Protease Structures
    ↓                                   ↓
    └──────→  AutoDock Vina Docking  ←─┘
                     ↓
           Binding Affinity Results
                     ↓
        Analysis & Visualization
```

## Directory Structure

```
AET Senior Research/
├── generate_sequences.py
├── prepare_protease_structures.py
├── predict_structures.py
├── molecular_docking.py
├── analyze_docking_results.py
├── run_docking_pipeline.py
├── DOCKING_PIPELINE_README.md
│
├── generated_sequences/
│   ├── supremegan_sequences.csv
│   └── supremegan_sequences.fasta
│
├── protease_structures/
│   ├── raw/
│   ├── prepared/
│   ├── structure_summary.csv
│   └── binding_sites.json
│
├── predicted_structures/
│   ├── pdb_files/
│   └── prediction_results_*.csv
│
├── docking_results/
│   ├── pdbqt_files/
│   ├── vina_results/
│   └── docking_results.csv
│
└── docking_analysis/
    ├── affinity_distribution.png
    ├── per_protease_comparison.png
    ├── top_binders_heatmap.png
    ├── sequence_analysis.png
    ├── ranked_results.csv
    ├── top_binders.csv
    └── statistics.json
```

## Performance Considerations

### Time Estimates

For 100 sequences per protease (2,900 total):
- Sequence generation: ~1 minute
- Protease preparation: ~5-10 minutes
- Structure prediction: ~4-8 hours (ESMFold API with rate limiting)
- Docking: ~5-10 hours (depends on exhaustiveness)
- Analysis: ~1-2 minutes

### Optimization Tips

1. **Use local ESMFold** for faster structure prediction (requires GPU)
2. **Parallelize docking** by modifying `molecular_docking.py` to use multiprocessing
3. **Start small** - test with 10 sequences first
4. **Skip completed steps** using `--skip` flag
5. **Use GPU** for structure prediction when available

## Troubleshooting

### ESMFold API Rate Limiting

If you hit rate limits:
- Increase `DELAY_BETWEEN_REQUESTS` in `predict_structures.py`
- Use `--max` to process in batches
- Consider installing local ESMFold

### AutoDock Vina Not Found

```bash
# Check installation
vina --version

# If not found, reinstall
conda install -c conda-forge vina
```

### PDBQT Conversion Errors

If AutoDock Tools fails:
```bash
# Install OpenBabel as fallback
conda install -c conda-forge openbabel
```

### Memory Issues

For large-scale runs:
- Process in batches using `--max-predictions` and `--max-dockings`
- Use `--skip` to run pipeline in stages

## Citation & References

### Tools Used

- **ESMFold**: Lin et al., "Language models of protein sequences at the scale of evolution enable accurate structure prediction" (2022)
- **AutoDock Vina**: Trott & Olson, "AutoDock Vina: improving the speed and accuracy of docking" (2010)
- **MEROPS Database**: Rawlings et al., "The MEROPS database of proteolytic enzymes" (2018)

## Next Steps

1. **Validate top binders** with experimental assays
2. **Refine binding sites** using known inhibitor structures
3. **Run MD simulations** on top complexes
4. **Optimize lead sequences** based on binding modes
5. **Test against real clinical samples**

## Support

For issues or questions:
1. Check the troubleshooting section
2. Verify all dependencies are installed
3. Try a test run with limited data
4. Review individual script outputs for errors

## License

This pipeline uses open-source tools. Please cite appropriate references when publishing results.
