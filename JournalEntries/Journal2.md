---
geometry: margin=0.5in, letterpaper
header-includes:
  - \usepackage{booktabs}
  - \usepackage{longtable}
  - \usepackage{array}
  - \usepackage{graphicx}
  - \usepackage{float}
  - \usepackage{setspace}
  - \usepackage{fancyhdr}
  - \pagestyle{empty}
output: pdf_document
---

# \hfill Journal Report
## \hfill Pranav Divichenchu
\vspace{-0.5em}
\hfill November 5, 2025

\vspace{1em}
\hrule
\vspace{0.5em}

**Research Topic:** Design a Generative Adverserial Network (GAN) to design novel protein sequences that are able to predict and enhance model clevage. 

**Mid October Goal:** (What will you have done by 10/15-ish)

Annotate articles on novel usage of GAN that I could potentially use for my own. I also want to develop an initial baselines GANs, potentially one from class, and a few others from open source websites (Hugging Face or Github)


I want to begin collecting and downloading the cleavage and molecule data from Merops mainly through web scraping, but also looking through the website. (If possible - I’ve looked and haven't been able to find any trustworthy sources) I also want to download external data, other than Merops that I could potentially use to make the dataset bigger. I also NEED to download molecules that do NOT result in a cleavage


Analyze the data and see what specific strands in the sequence may hint at success during cleavage  (something to highlight as an input when training the GAN).

**October Goal:** (And by 10/30-ish)

Develop my own novel GAN using a variety of techniques I have found through research.

Begin training my GAN + the other baseline GANs over a few days.


Compare the results of the GAN and see whether improvements can be made to my own personal GAN or just to pick up one of the baselines to go forward with the process.
Also potentially find and choose a fluorescence attachment that would latch onto the molecules, but that likely would have to wait for after the “best” protein sequence had been created.
  
If the model is spitting out good results, then potentially choose a target protein sequence 


\vspace{1em}
\hrule
\vspace{1em}

## Daily Log (10/27/25-11/5/25)


### Monday October 27

Pipeline Integration: Combined sequence generation → structure prediction → molecular docking into a single workflow (run_docking_pipeline.py:1)
  - Critical Bug Fixes:
    - Resolved ESMFold API rejections by implementing is_standard_sequence() filter to remove non-standard amino acids (Dab, DPh, Mca, Nle, NH2)
    - Added STANDARD_AA_3LETTER validation set with 20 canonical amino acids
  - Code Updates: Added Python files including compare_gan_models.py, calculate_druglike_properties.py, validate_against_literature.py, design_inhibitors.py, validate_inhibitors.py, and
  generate_sequences.py
  - Model Training: Generated new CGAN model weights (discriminator & generator .pth files at ~350-380KB each)
  - 
  -  run_docking_pipeline.py (run_docking_pipeline.py:1): Master orchestration script that automates the entire 5-step pipeline:
    a. Generates peptide sequences from trained GANs (Supreme/Conditional/WGAN)
    b. Downloads and prepares protease structures from PDB database
    c. Predicts 3D structures using ESMFold API
    d. Performs molecular docking with AutoDock Vina
    e. Analyzes and visualizes binding affinity results
    - Includes timing tracking, error handling, and ability to skip steps for faster iteration
  
  - generate_sequences.py (generate_sequences.py:1): Loads trained GAN models and generates protease-specific 8-mer peptide sequences
    - Added is_standard_sequence() filter (generate_sequences.py:49) to remove non-standard amino acids (Dab, DPh, Mca, Nle, NH2)
    - Fixed SupremeGAN import issue by ensuring training code only runs when script is executed directly, not imported
    - Outputs sequences in both CSV and FASTA formats for downstream analysis
  
  - compare_gan_models.py (compare_gan_models.py:1): Compares binding affinity performance across all three GAN architectures
    - Calculates mean/median affinity, identifies strong binders (<-8 kcal/mol)
    - Determines which model works best for each protease
    - Generates heatmaps, boxplots, and distribution visualizations
    - Produces comprehensive comparison report showing "winner" model
  
  - calculate_druglike_properties.py (calculate_druglike_properties.py:1): Assesses pharmaceutical viability of generated peptides
    - Calculates molecular weight, net charge, hydrophobicity, and polar ratio
    - Assigns "druglikeness score" (0-100) based on Lipinski-like rules adapted for peptides
    - Identifies sequences with poor oral bioavailability, solubility issues, or membrane permeability problems
    - Ranks candidates by combined binding affinity + druglikeness

### Thursday October 29

 - Mentor Meeting: Discussed project progress with research mentor who provided key guidance:
    - Action Item #1: Investigate the true binding sites of target sepsis-related proteases (not just general docking)
    - Action Item #2: Analyze optimal peptide sequence lengths for each protease's binding pocket
  
  - Implementation:
    - Researched and documented actual binding site locations and dimensions for target proteases
    - Analyzed relationship between peptide length (8-mers) and binding pocket compatibility
    - Polished model architectures based on mentor feedback

  - GAN Model Comparison: Executed compare_gan_models.py to evaluate all three architectures:
    - Compared sequence quality, diversity, and predicted binding affinities across Conditional GAN, WGAN-GP, and SupremeGAN
    - Analyzed which model generated peptides with optimal characteristics for protease inhibition

  - validate_against_literature.py (validate_against_literature.py:1): Validates your computational results against known scientific literature
    - Compares your predicted binding affinities to published ranges for 7 major sepsis proteases
    - Known values from Nakajima (1979), Stubbs & Bode (1995), Nagase (2006), etc.
    - Checks if your peptides show protease specificity (preferential binding to target vs. off-targets)
    - Generates validation plots showing your results vs. literature benchmarks

  - design_inhibitors.py (design_inhibitors.py:1): Converts top-binding substrates into therapeutic peptidomimetic inhibitors
    - Modifies P1-P1' scissile bond with 4 strategies: reduced amide, ketomethylene, phosphonate, hydroxyethylene
    - Each modification makes the peptide uncleavable while retaining binding affinity
    - Generates synthesis protocols with vendor recommendations and cost estimates ($200-$2000 per inhibitor)
    - Creates clinical relevance context for each protease target

  - validate_inhibitors.py (validate_inhibitors.py:1): Computationally validates inhibitor designs and prepares ISEF presentation materials
    - Compares substrate vs. inhibitor predicted affinities (expects 0.5-2.0 kcal/mol improvement)
    - Generates ISEF summary explaining dual-use platform (diagnostic substrates + therapeutic inhibitors)
    - Creates mechanism diagrams showing how modified bonds block protease cleavage
    - Outlines experimental validation roadmap (in vitro → cell-based → animal studies)




## Timeline

\begin{longtable}{|p{3cm}|p{6cm}|p{6cm}|}
\hline
\textbf{Date} & \textbf{Goal} & \textbf{Met?} \\
\hline
9/25/2025 & Finish annotating GAN-related research papers and finalize which architectures to replicate & Done \\
\hline
10/06/2025 & Begin collecting cleavage data from Merops and test basic scraping scripts & Done \\
\hline
10/06/2025 & Finish dataset preprocessing + Download and Create initial GANs for testing & Done \\
\hline
10/15/2025 & Develop the structure for my own novel GAN and begin first round of training & Done \\
\hline
10/31/2025 & Compare results across GANs and refine input data or architecture for best performance Done \\
\hline
\end{longtable}


## Reflection

I have achieved my October goal of developing a novel GAN, training baseline GANs, and comparing results. I developed and trained three GAN architectures (Conditional GAN, WGAN-GP, and my
novel SupremeGAN with advanced techniques like gradient penalties, self-attention, spectral normalization, and conditional batch normalization), built a complete end-to-end pipeline integrating GAN generation
with ESMFold structure prediction and AutoDock Vina molecular docking, completed comprehensive GAN comparison analysis incorporating mentor-guided binding site specificity, 
By the end of October, I have successfully transitioned met all my goals and have made a strong start towards the next month of research. 