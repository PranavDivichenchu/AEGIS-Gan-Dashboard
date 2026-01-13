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

# \hfill Journal #7
## \hfill Pranav Divichenchu
\vspace{-0.5em}
\hfill January 10, 2026

\vspace{1em}
\hrule
\vspace{0.5em}

**Research Topic:** Design a Generative Adverserial Network (GAN) to design novel protein sequences that are able to predict and enhance model cleavage.

**Weekly Goal (1/6/26 - 1/10/26):**

Submit comprehensive experimental design document to Dr. Hanson for review and approval.

Begin preparation for wet-lab validation by researching proper fluorometric assay techniques and plate reader operation.

Familiarize with best practices for handling fluorogenic substrates and enzyme kinetics measurements.

\vspace{1em}
\hrule
\vspace{1em}

## Daily Log (1/6/26-1/10/26)

**Monday, 1/6/26:**
Finalized the comprehensive experimental design document for the Kallikrein 2 substrate validation experiment. Made final revisions to ensure all sections met the experimental design rubric requirements, including clear problem statement, testable hypothesis with null hypothesis, explicitly defined independent and dependent variables, comprehensive controls (blanks and substrate-only), detailed materials list with vendor specifications and catalog numbers, step-by-step numbered procedures, safety considerations with MSDS references, and complete bibliography. The final document includes detailed protocols for the fluorometric substrate cleavage assay using EGSCYGTR-AMC peptide, with a total project budget of $949. Submitted the experimental design to Dr. Hanson for review and approval. The document outlines testing a single high-confidence GAN-designed peptide (EGSCYGTR, predicted binding affinity -9.72 kcal/mol) rather than the entire 27-peptide panel, allowing for thorough validation within budget constraints.

**Wednesday, 1/8/26:**
Followed up on the experimental design submission to Dr. Hanson. Currently awaiting feedback and approval to proceed with reagent ordering and equipment scheduling. Used the waiting period productively to review the experimental design document and identify any potential areas for revision based on Dr. Hanson's feedback. Began preliminary research into best practices for fluorometric enzyme assays, focusing on proper handling of AMC-conjugated substrates and common pitfalls in kinetic fluorescence measurements. Reviewed literature on AMC fluorophore characteristics, including optimal excitation/emission wavelengths (360 nm/460 nm), sensitivity to pH and temperature, and potential quenching effects. This preparation will be valuable when executing the actual assay.

**Friday, 1/10/26:**
Continued preparation for wet-lab validation by conducting in-depth research into practical aspects of the fluorometric substrate cleavage assay. Watched several instructional videos and tutorials on YouTube and vendor websites (Molecular Devices, BioTek, Corning) covering:

- Proper technique for preparing fluorogenic substrate stock solutions in DMSO
- Best practices for enzyme handling and aliquoting to maintain activity
- Plate reader operation and optimization of gain/sensitivity settings
- Common sources of error in kinetic fluorescence assays (edge effects, evaporation, temperature drift)
- Data analysis workflows for enzyme kinetics experiments

Paid particular attention to videos demonstrating multichannel pipetting technique for adding enzyme to multiple wells simultaneously, which is critical for minimizing time differences in reaction initiation. Also reviewed protocols for maintaining sterile technique when working with recombinant proteins. This hands-on preparation through visual learning complements the written protocols in my experimental design and will help ensure successful execution when approval is granted and reagents arrive.

## Timeline Update

\begin{longtable}{|p{3cm}|p{6cm}|p{6cm}|}
\hline
\textbf{Date} & \textbf{Goal} & \textbf{Met?} \\
\hline
1/6/2026 & Design comprehensive experimental validation protocol for EGSCYGTR peptide & Done \\
\hline
1/6/2026 & Submit experimental design to Dr. Hanson for approval & Done \\
\hline
1/15/2026 & Receive approval and finalize equipment access & In Progress \\
\hline
1/20/2026 & Order all reagents for validation experiments & Pending \\
\hline
2/1/2026 & Execute initial substrate cleavage assays and collect kinetic data & Pending \\
\hline
\end{longtable}

## Reflection

This week marked an important transition from experimental design to preparation for actual implementation. Submitting the comprehensive experimental design document to Dr. Hanson represents a critical milestone - moving from computational predictions to planning wet-lab validation. The waiting period for approval has been valuable for deepening my understanding of the practical techniques required for fluorometric assays.

The video-based learning approach on Friday was particularly helpful. Seeing experienced researchers demonstrate proper pipetting technique, plate setup, and troubleshooting strategies provides context that written protocols alone cannot convey. Understanding common pitfalls like edge effects (wells on plate edges evaporating faster) and the importance of temperature equilibration will help me avoid these issues when I run the actual experiment.

One key insight from this week's research is the critical importance of timing when adding enzyme to substrate wells. The videos emphasized that even small delays (30-60 seconds) between adding enzyme to the first and last wells can introduce variability in kinetic measurements. This reinforces my decision to use a multichannel pipette and practice the motion before the actual experiment.

The experimental design is now in Dr. Hanson's hands. Once approved, the next steps will be ordering the custom EGSCYGTR-AMC peptide (3-4 week synthesis time), purchasing the recombinant Kallikrein 2 enzyme, and scheduling plate reader access. The peptide synthesis timeline means that even with prompt approval, I'm realistically looking at mid-to-late February for running the actual assay. This timeline aligns well with the semester schedule and allows buffer for troubleshooting if needed.

Whether the experiment shows positive results (validating the GAN prediction) or negative results (revealing limitations in the computational approach), the data will provide valuable feedback for refining the machine learning model and understanding the relationship between predicted binding affinity and actual enzymatic cleavage.
