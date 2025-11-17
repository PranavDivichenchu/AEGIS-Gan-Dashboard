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

# \hfill Journal #11
## \hfill Pranav Divichenchu
\vspace{-0.5em}
\hfill November 17, 2025

\vspace{1em}
\hrule
\vspace{0.5em}

**Research Topic:** Design a Generative Adverserial Network (GAN) to design novel protein sequences that are able to predict and enhance model cleavage. 


**November Goal:** (By 11/30)

Validate all computational predictions against published literature to ensure the GAN-generated peptides fall within expected binding affinity ranges for sepsis-related proteases.

Complete comprehensive analysis of peptidomimetic inhibitor designs and generate synthesis protocols with cost estimates and vendor recommendations for experimental validation.

Scale up GAN training using cloud infrastructure (Google Colab) to generate larger, more diverse peptide libraries and improve model performance.

Freeze and document the complete Python environment to ensure reproducibility of all computational results.


Conduct binding site specificity analysis to determine optimal peptide lengths and sequences for each target protease's binding pocket.


\vspace{1em}
\hrule
\vspace{1em}

## Daily Log (11/10/25-11/17/25)
   
### Tuesday November 11

  - Full Pipeline Execution: Ran complete docking simulation pipeline across all three GAN models (SupremeGAN, Conditional GAN, WGAN-GP)
    - Generated 100+ peptide sequences per protease target
    - Processed structure predictions through ESMFold API
    - Completed molecular docking analysis with AutoDock Vina
    - Collected comprehensive binding affinity data for comparison analysis

  - Performance Monitoring: Tracked pipeline execution times and identified computational bottlenecks
    - ESMFold API calls: primary time constraint (~10-15 seconds per structure)
    - Docking calculations: secondary bottleneck (~5-8 seconds per peptide-protein pair)
    - Total runtime: approximately 6-8 hours for complete pipeline

### Thursday November 13

  - GAN Performance Comparison: Comprehensive statistical analysis comparing SupremeGAN vs ConditionalGAN
    - Analyzed 781 total docking results (536 ConditionalGAN, 245 SupremeGAN)
    - ConditionalGAN mean affinity: -7.25 kcal/mol; SupremeGAN: -7.18 kcal/mol
    - Statistical analysis revealed close performance (p-value for difference), validating ensemble approach
    - ConditionalGAN achieved 23 excellent binders (<-10 kcal/mol) vs 5 for SupremeGAN
    - Generated comprehensive visualizations: distribution plots, protease-specific comparisons, winner analysis
    - Protease-level analysis: ConditionalGAN won 14 proteases, SupremeGAN won 13 proteases

  - 27-Peptide Panel Design: Created strategic ensemble selection leveraging both GAN models
    - Selected best peptide per protease (27 proteases total) regardless of source model
    - Final panel composition: ConditionalGAN contributed 14 peptides, SupremeGAN contributed 13 peptides
    - Panel binding affinity range: -11.88 to -4.93 kcal/mol
    - Binding categories: 2 excellent (<-10), 8 strong (-10 to -8), 12 good (-8 to -6), 5 moderate (>-6)
    - Top candidates identified: Panel #14 (MMP1, -11.88), Panel #24 (Proteinase 3, -11.14), Panel #13 (Kallikrein 2, -9.72)

  - Drug-Likeness Assessment: Comprehensive ADMET analysis of 27-peptide panel
    - Calculated molecular properties: MW (689-1167 Da), hydrophobicity (GRAVY scores), net charge (-4 to +4)
    - Assessed H-bond donors/acceptors, polar ratios, aromatic content for binding predictions
    - Evaluated instability scores and peptide stability predictions
    - Druglikeness scoring system developed: mean 68.5/100, range 45-95
    - Identified 18 peptides with druglikeness score >=60 (suitable for development)
    - Combined scoring approach: binding affinity + druglikeness for prioritization

  - Inhibitor Design Development: Critical transformation from binding peptides to functional inhibitors
    - Recognized fundamental distinction between substrate binding vs active site inhibition
    - Designed protease class-specific chemical modifications:
      * Caspases (6 peptides): N-acetylation + aldehyde/FMK warheads at C-terminus
      * MMPs (6 peptides): Hydroxamate groups for zinc ion chelation
      * Serine proteases (13 peptides): Boronic acid/aldehyde warheads
      * Cysteine proteases (2 peptides): General inhibitor modifications
    - Identified cleavage risk sites in 25/27 peptides using protease specificity analysis
    - Generated 3 design versions per peptide: basic (Ac-peptide-NH2), enhanced (with warhead), cyclic
    - Created detailed synthesis specifications with estimated costs per modification type

### Sunday November 16

  - Budget-Optimized Synthesis Planning: Strategic plan development for $200-400 budget constraint
    - Scored all 27 peptides on multiple criteria: binding affinity, cleavage risk, clinical relevance
    - Top candidates: Panel #14 (MMP1, -11.88, high clinical relevance), Panel #13 (Kallikrein 2, -9.72, LOW cleavage risk)
    - Recommended approach: 1 peptide in 2 versions (unmodified + Ac-peptide-NH2) for proof-of-concept
    - Selected Panel #13 (Kallikrein 2) as optimal candidate due to low cleavage risk, excellent binding, and cyclization potential
    - Cost breakdown: unmodified peptide (~$110), basic inhibitor (~$170), total ~$280

  - Experimental Validation Protocol Design: Fluorescence-based inhibition assay development
    - Clarified assay mechanism: competitive inhibition using commercial fluorogenic substrate
    - No fluorescent labeling needed on test peptides - they compete with fluorogenic substrate
    - Identified complete reagent requirements: protease enzyme, fluorogenic substrate, test peptides, buffers
    - Full budget analysis: ~$700-900 for complete testing with Kallikrein 2 enzyme
    - Developed alternative strategy: Trypsin proof-of-concept (~$450 total) for budget feasibility


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
10/31/2025 & Compare results across GANs and refine input data or architecture for best performance & Done \\
\hline
11/15/2025 & Complete literature validation and peptidomimetic inhibitor design analysis & In Progress \\
\hline
11/22/2025 & Finish extended GAN training on Google Colab and freeze final models & Pending \\
\hline
\end{longtable}


## Reflection

This week (November 11-16) marked the transition from pure computational model development to experimental preparation and validation planning. The most significant achievement was completing comprehensive statistical comparison between SupremeGAN and ConditionalGAN across 781 docking results. The analysis revealed nearly equivalent performance (ConditionalGAN: -7.25 kcal/mol mean, SupremeGAN: -7.18 kcal/mol mean, p > 0.05), which validated my decision to pursue an ensemble approach rather than selecting a single "best" model. This finding demonstrates that both GAN architectures successfully learned meaningful patterns from the MEROPS dataset, and combining their strengths through strategic selection yields optimal results.

The creation of the 27-peptide panel represents the culmination of months of computational work. By selecting the best-performing peptide for each of the 27 sepsis-related proteases regardless of which GAN generated it, I created a diverse inhibitor library with binding affinities ranging from -11.88 to -4.93 kcal/mol. The drug-likeness assessment revealed that 18 of these 27 peptides (67%) have favorable druglikeness scores (>=60/100), suggesting they possess molecular properties suitable for therapeutic development. This analysis incorporated molecular weight, hydrophobicity, net charge, H-bond characteristics, and stability predictions - all critical factors for eventual in vivo efficacy.

Most importantly, I recognized a fundamental conceptual gap that required immediate correction: designing peptides that bind strongly to proteases is not equivalent to designing functional inhibitors. Through this realization, I understood that many of my high-affinity peptides could function as excellent substrates that get cleaved rather than as inhibitors that block catalytic activity. This insight drove the development of protease class-specific chemical modification strategies. For the six caspase-targeting peptides, I designed N-terminal acetylation with aldehyde or fluoromethyl ketone (FMK) warheads. For the six MMP-targeting peptides, I incorporated hydroxamate groups for zinc ion chelation. The thirteen serine protease inhibitors received boronic acid or aldehyde warheads with protective terminal modifications. Each peptide now has three design versions: basic (Ac-peptide-NH2), enhanced (with class-specific warhead), and cyclic (for conformational constraint).

The shift to experimental planning forced me to confront practical constraints that computational work abstracts away. With a realistic high school research budget of $200-400, I cannot afford to synthesize all 27 peptides or even conduct full validation experiments for a single candidate. This led to strategic prioritization using multi-criteria scoring (binding affinity, cleavage risk, clinical relevance, synthesis feasibility). Panel #13 targeting Kallikrein 2 emerged as the optimal proof-of-concept candidate: it has excellent predicted binding (-9.72 kcal/mol), low cleavage risk (no predicted cleavage sites), contains cysteine for potential cyclization, and targets a clinically-relevant protease in sepsis pathophysiology. The budget-optimized approach of synthesizing one peptide in two versions (unmodified control + basic inhibitor) for approximately $280 allows direct experimental comparison to validate the core hypothesis: chemical modifications convert binding peptides into functional inhibitors.

Understanding the fluorescence-based competitive inhibition assay mechanism was crucial for experimental planning. I initially misunderstood the assay, thinking my peptides would need fluorescent labels. Clarifying that the assay uses a commercial fluorogenic substrate that competes with my unlabeled inhibitor peptides was essential. However, complete experimental validation requires not just the synthesized peptides (~$280) but also the Kallikrein 2 enzyme (~$200-350), fluorogenic substrate (~$150-200), and assay consumables (~$50-100), totaling $680-930 - well beyond my budget. This realization necessitated development of alternative strategies: partnering with the Academies of Loudoun biochemistry lab for equipment access and reagent sharing, or starting with a cheaper proof-of-concept using Trypsin enzyme (~$450 total).

Progress toward November goals is substantial but incomplete. I have successfully validated computational predictions statistically through GAN comparison, completed comprehensive peptidomimetic inhibitor designs with detailed synthesis protocols and vendor recommendations, and thoroughly documented the computational environment for reproducibility. The literature validation framework is established but not yet fully executed - this remains pending. Extended GAN training on Google Colab is also pending as I focused this week on converting computational results into actionable experimental plans rather than generating additional peptide libraries. Binding site specificity analysis has been incorporated throughout the inhibitor design process, though formalized quantitative analysis could be expanded.

The next immediate steps are: (1) finalize collaboration arrangements with ACL's lab to secure equipment access and determine available reagents, (2) initiate peptide synthesis once lab collaboration and budget are confirmed, and (3) during the 2-3 week synthesis period, complete literature validation comparing my computational predictions to published inhibitor data and conduct any final computational analyses. The successful execution of even this single proof-of-concept experiment would provide invaluable experimental validation of the entire GAN → structure prediction → docking → inhibitor design pipeline, establishing a foundation for future expansion, publication, and potential research funding.

