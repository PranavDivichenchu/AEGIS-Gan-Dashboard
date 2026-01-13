---
geometry: margin=0.75in, letterpaper
header-includes:
  - \usepackage{booktabs}
  - \usepackage{longtable}
  - \usepackage{array}
  - \usepackage{graphicx}
  - \usepackage{float}
  - \usepackage{setspace}
output: pdf_document
---

\begin{center}
\Large{\textbf{Experimental Design: Validation of GAN-Designed Peptide EGSCYGTR as a Substrate for Human Kallikrein 2 Protease}}
\end{center}

\vspace{0.5em}

\begin{center}
\textbf{Pranav Divichenchu}\\
\textit{AET Senior Research Project}\\
January 7, 2026
\end{center}

---

## 1. Problem Statement

**Can a generative adversarial network (GAN) trained on protease cleavage site data accurately predict novel peptide substrates for human Kallikrein 2 protease?**

Protease substrate specificity is traditionally identified through expensive, time-consuming screening of large peptide libraries. Machine learning offers the potential to computationally design novel substrates, but experimental validation is required to confirm predictions translate to functional biological activity. Human Kallikrein 2 (hK2) is a serine protease involved in inflammatory response and protease cascade amplification during sepsis. 

---

## 2. Hypothesis

**Hypothesis:** The GAN-designed peptide EGSCYGTR will be recognized and cleaved by Kallikrein 2 enzyme, as indicated by increased fluorescence from AMC release, because molecular docking predicts strong binding affinity (-9.72 kcal/mol).

**Predicted Outcome:** EGSCYGTR-AMC + enzyme will show significantly higher fluorescence increase over time compared to substrate-only controls, demonstrating enzymatic cleavage.

**Null Hypothesis:** No significant difference in fluorescence between enzyme-treated wells and substrate-only controls.

---

## 3. Variables

### 3.1 Independent Variable (IV)

**Presence or absence of active Kallikrein 2 enzyme**

- **Test condition:** EGSCYGTR-AMC peptide + Kallikrein 2 enzyme (15 nM)
- **Control condition:** EGSCYGTR-AMC peptide + buffer only (no enzyme)

This is the factor being purposefully manipulated to determine its effect on substrate cleavage.

### 3.2 Dependent Variable (DV)

**Fluorescence intensity (Relative Fluorescence Units, RFU) measured over time**

- **Measurement method:** Fluorescence plate reader (Ex: 360 nm, Em: 460 nm)
- **Units:** RFU (Relative Fluorescence Units)
- **Time course:** Measured every 2-5 minutes for 120-180 minutes
- **Response:** Fluorescence increases when AMC is released from cleaved peptide

This is the factor being measured that responds to the independent variable.

### 3.3 Constants (Controlled Variables)

All experimental wells will maintain identical conditions except for the independent variable:

| Constant | Value | Rationale |
|----------|-------|-----------|
| **Substrate concentration** | 100 μM EGSCYGTR-AMC | Ensures equal substrate availability |
| **Buffer composition** | 50 mM Tris-HCl, pH 8.0, 100 mM NaCl, 0.01% Tween-20 | Maintains optimal enzyme activity conditions |
| **pH** | 8.0 | Optimal pH for Kallikrein 2 activity |
| **Temperature** | 37°C | Physiological temperature |
| **Reaction volume** | 100 μL per well | Standardizes concentration calculations |
| **Incubation time** | 120-180 minutes | Allows sufficient time for cleavage |
| **Plate type** | Black 96-well microplate (Corning 3915) | Minimizes fluorescence crosstalk |
| **Read settings** | Ex 360 nm / Em 460 nm, bottom read | Standardizes detection |
| **Enzyme concentration** (when present) | 15 nM | Ensures comparable enzyme activity |
| **Peptide lot number** | Same synthesis batch | Eliminates batch-to-batch variation |
| **Assay buffer lot** | Same preparation | Eliminates buffer variation |

### 3.4 Control Groups

**1. Negative Controls:**

- **Blank (Buffer only):** Measures background fluorescence from plate and buffer
  - Contents: 100 μL assay buffer
  - Purpose: Establishes baseline fluorescence
  - Wells: A1-A3 (n=3)

- **Substrate-only control (No enzyme):** Tests peptide stability in absence of enzyme
  - Contents: 100 μM EGSCYGTR-AMC in buffer, no enzyme
  - Purpose: Confirms peptide does not spontaneously release AMC
  - Wells: A4-A6 (n=3)

**2. Test Condition:**

- **GAN-designed peptide + enzyme:** The experimental test
  - Contents: 100 μM EGSCYGTR-AMC + 15 nM Kallikrein 2
  - Purpose: Determine if GAN peptide is cleaved
  - Wells: B4-B6 (n=3)
  - Expected result: Fluorescence increase if substrate is cleaved

### 3.5 Repeated Trials

**Technical replicates:** Each condition tested in triplicate (n=3) within a single plate to assess pipetting precision and measurement variability.

**Biological replicates:** Entire experiment repeated on 2-3 independent occasions using fresh reagent preparations to confirm reproducibility.

**Total measurements per condition:** 3 (technical) × 2-3 (biological) = 6-9 independent measurements

**Acceptance criteria:** Coefficient of variation (CV) within technical triplicates must be <15%. Biological replicates must show consistent trends.

---

## 4. Materials

### 4.1 Custom Synthesized Test Substrate

**EGSCYGTR-AMC (Custom fluorogenic peptide)**

- **Sequence:** Glu-Gly-Ser-Cys-Tyr-Gly-Thr-Arg-AMC
- **One-letter code:** EGSCYGTR
- **C-terminal modification:** 7-amino-4-methylcoumarin (AMC) fluorophore
- **N-terminus:** Free (NH3+)
- **Molecular weight:** ~1,045 Da (870 Da peptide + 175 Da AMC)
- **Purity:** ≥95% by HPLC
- **Amount:** 5 mg
- **Analysis:** HPLC chromatogram + mass spectrometry (MS) confirmation
- **Form:** Lyophilized powder
- **Storage:** -20°C, desiccated, protected from light
- **Vendor:** Bachem (bachem.com), AnaSpec (anaspec.com), or GenScript (genscript.com)
- **Cost:** $400-600
- **Lead time:** 3-4 weeks

### 4.2 Enzyme

**Recombinant Human Kallikrein 2 (hK2)**

- **Vendor:** R&D Systems, Cat# 1116-SE-010 (rndsystems.com)
- **Quantity:** 10 μg
- **Form:** Lyophilized protein
- **Specific activity:** >1,000 pmol/min/μg
- **Purity:** >95% by SDS-PAGE
- **Molecular weight:** ~26 kDa
- **Storage:** -80°C in single-use aliquots
- **Reconstitution:** Sterile water or buffer per manufacturer protocol
- **Cost:** $350-400

### 4.3 Buffer Components

| Chemical | Quantity | Concentration in Stock | Vendor | Cat# | Cost |
|----------|----------|----------------------|--------|------|------|
| Tris base (ultrapure) | 100 g | N/A | Sigma | T1503 | $15 |
| Sodium chloride (NaCl, molecular biology grade) | 100 g | N/A | Sigma | S5886 | $5 |
| Tween-20 (polysorbate 20) | 50 mL | Pure (100%) | Sigma | P1379 | $10 |
| Hydrochloric acid (HCl) | 100 mL | 1 M solution | Sigma | H9892 | $10 |
| DMSO (dimethyl sulfoxide, cell culture grade, sterile) | 50 mL | Pure (100%) | Sigma | D2650 | $20 |
| Deionized water (18 MΩ·cm, sterile) | 1 L | N/A | Laboratory supply | N/A | $0 |

**Buffer formulation (Kallikrein Assay Buffer, 500 mL):**

- 50 mM Tris-HCl, pH 8.0
- 100 mM NaCl
- 0.01% (v/v) Tween-20

**Total reagent cost:** $60

### 4.5 Consumables and Plasticware

| Item | Specifications | Quantity | Vendor/Cat# | Cost |
|------|---------------|----------|-------------|------|
| 96-well microplates | Black, flat-bottom, tissue culture treated | 3 plates | Corning 3915 | $24 |
| Sterile filter units | 0.22 μm PES membrane, 500 mL | 1 unit | Millipore SCGPU05RE | $15 |
| Microcentrifuge tubes | 1.5 mL, amber (light-blocking) | 100 tubes | Eppendorf 30121422 | $15 |
| Pipette tips | 10 μL, 200 μL, 1000 μL, sterile, filtered | 1 set | Rainin 30389218 | $30 |
| Plate sealing film | Optical, clear, adhesive | 1 roll | Bio-Rad MSB1001 | $15 |
| Aluminum foil | Heavy-duty, laboratory grade | 1 roll | VWR 89079-073 | $5 |
| 15 mL conical tubes | Polypropylene, sterile | 25 tubes | Falcon 352096 | $10 |

**Total consumables cost:** $114

### 4.5 Total Materials Budget

| Category | Cost |
|----------|------|
| EGSCYGTR-AMC custom peptide | $400 |
| Recombinant Kallikrein 2 enzyme | $375 |
| Buffer reagents (Tris, NaCl, Tween, DMSO, HCl) | $60 |
| Consumables (plates, tips, filters, tubes) | $114 |
| **TOTAL PROJECT COST** | **$949** |

### 4.6 Species Information

**Human Kallikrein 2 (hK2):**

- **Species:** Homo sapiens (human)
- **Source:** Recombinant protein expressed in E. coli or mammalian cells
- **Protein classification:** Serine protease, trypsin-like
- **UniProt ID:** P20151
- **Gene:** KLK2
- **Function:** Proteolytic processing of pro-PSA, bradykinin generation, inflammatory response

No animal subjects are used in this experiment. All enzymes are recombinant proteins produced commercially.

---

## 5. Methods

### 5.1 Reagent Preparation (Day 1)

#### 5.1.1 Assay Buffer Preparation

1. Weigh 3.03 g Tris base and transfer to 500 mL beaker
2. Weigh 2.92 g NaCl and add to beaker
3. Add approximately 400 mL deionized water
4. Stir on magnetic stir plate until fully dissolved (approximately 10 minutes)
5. Adjust pH to 8.0 using 1 M HCl (add dropwise while monitoring with pH meter)
6. Add 50 μL Tween-20 (use positive displacement pipette for accuracy)
7. Transfer to 500 mL graduated cylinder and bring to final volume with deionized water
8. Pour into sterile 500 mL bottle
9. Sterile filter through 0.22 μm filter unit into fresh sterile bottle
10. Label: "Kallikrein Assay Buffer (50 mM Tris pH 8.0, 100 mM NaCl, 0.01% Tween), Date, Initials"
11. Store at 4°C for up to 1 month

**Quality control:** Verify final pH is 8.0 ± 0.1. Buffer should be clear with no particulates.

#### 5.1.2 Peptide Stock Solution Preparation

1. Remove EGSCYGTR-AMC vial from -20°C freezer
2. Allow to equilibrate to room temperature for 15 minutes (prevents condensation)
3. Calculate volume of DMSO needed for 10 mM stock:
   - Example: 5 mg peptide ÷ 1.045 mg/μmol = 4.78 μmol
   - Volume DMSO = 4.78 μmol ÷ 10 mM = 0.478 mL = 478 μL
4. Add calculated volume of DMSO directly to peptide vial using pipette
5. Vortex for 60 seconds at maximum speed
6. Centrifuge briefly (5 seconds, 1000 × g) to collect liquid at bottom
7. Visually inspect for complete dissolution (solution should be clear to slightly yellow)
8. Aliquot into amber 1.5 mL microcentrifuge tubes: 50 μL per tube (~10 aliquots)
9. Label each tube: "EGSCYGTR-AMC, 10 mM in DMSO, Date, Initials"
10. Store at -20°C protected from light
11. Record lot number and storage location in laboratory notebook

**Safety note:** DMSO is a penetrating solvent. Wear nitrile gloves and handle in fume hood. Avoid skin contact.

#### 5.1.3 Enzyme Preparation

1. Remove Kallikrein 2 vial from -80°C freezer
2. Place on ice and allow to thaw slowly (approximately 10 minutes)
3. Reconstitute according to manufacturer's instructions (typically: add 100 μL sterile water or buffer to 10 μg vial = 100 μg/mL)
4. Mix gently by pipetting up and down 5 times (avoid vortexing enzymes)
5. Allow to stand on ice for 5 minutes to ensure complete dissolution
6. Calculate concentration:
   - 100 μg/mL ÷ 26 kDa = 3.85 μM
7. Aliquot into 10 μL portions in sterile microcentrifuge tubes (10 aliquots)
8. Label: "Kallikrein 2, 3.85 μM, Date, Lot#"
9. Flash freeze in liquid nitrogen or dry ice/ethanol bath
10. Store at -80°C
11. **Critical:** Use single-use aliquots only. Do not refreeze after thawing.

---

### 5.2 Experimental Procedure (Day 2)

#### 5.2.1 Pre-Experiment Setup

1. Remove assay buffer from 4°C and warm to 37°C in water bath or incubator (30 minutes)
2. Turn on plate reader and allow to warm up (15 minutes)
3. Set plate reader to 37°C and allow chamber to equilibrate (15 minutes)
4. Pre-label a black 96-well plate with plate ID, date, and initials
5. Prepare ice bucket
6. Set up workspace with all materials within reach
7. Cover bench surface with absorbent bench paper

#### 5.2.2 Working Solution Preparation

**Working substrate solution - EGSCYGTR-AMC (200 μM, 2× final concentration):**

1. Remove one aliquot of EGSCYGTR-AMC stock (10 mM) from -20°C
2. Thaw at room temperature for 5 minutes, then place on ice
3. Prepare working solution in sterile 1.5 mL tube:
   - 20 μL of 10 mM stock
   - 980 μL assay buffer
   - Mix by inverting 10 times
   - Final concentration: 200 μM (2× final)
4. Cover tube with aluminum foil to protect from light
5. Store on ice until use (use within 4 hours)

**Working enzyme solution (30 nM, 2× final concentration):**

1. Remove one aliquot of Kallikrein 2 (3.85 μM) from -80°C
2. Place on ice and allow to thaw (approximately 10 minutes)
3. Prepare working solution in sterile 1.5 mL tube:
   - 7.8 μL of 3.85 μM stock
   - 992.2 μL assay buffer
   - Mix by gentle pipetting (10 times)
   - Final concentration: 30 nM (2× final)
4. Keep on ice
5. **Important:** Use within 2 hours of preparation

#### 5.2.3 Plate Loading (Critical Timing Step)

**Set up wells in following order (use multichannel pipette when possible):**

1. **Blank wells (A1-A3):**
   - Add 100 μL assay buffer to each well

2. **Substrate-only controls - GAN peptide (A4-A6):**
   - Add 50 μL EGSCYGTR-AMC (200 μM) to each well
   - Add 50 μL assay buffer to each well
   - Final: 100 μM substrate, no enzyme

3. **Test wells - GAN peptide (B4-B6):**
   - Add 50 μL EGSCYGTR-AMC (200 μM) to each well
   - **DO NOT add enzyme yet**

**Plate layout:**

```
     1      2      3      4      5      6
  +------+------+------+------+------+------+
A |Blank |Blank |Blank | GAN  | GAN  | GAN  |
  |Buffer|Buffer|Buffer| Sub  | Sub  | Sub  |
  | only | only | only | only | only | only |
  +------+------+------+------+------+------+
B |      |      |      | GAN  | GAN  | GAN  |
  |      |      |      |+Enz  |+Enz  |+Enz  |
  |      |      |      |15 nM |15 nM |15 nM |
  +------+------+------+------+------+------+
```

**Legend:**
- Blank = Buffer only (background fluorescence)
- GAN Sub only = EGSCYGTR-AMC substrate without enzyme (tests peptide stability)
- GAN + Enz = EGSCYGTR-AMC + Kallikrein 2 (THE EXPERIMENTAL TEST)

#### 5.2.4 Reaction Initiation

1. Add 50 μL enzyme working solution (30 nM) to test wells (B4-B6)
2. Immediately tap plate gently on bench surface 3-4 times to mix
3. **Immediately** transfer plate to plate reader (within 30 seconds)
4. Record exact time enzyme was added in laboratory notebook

**Critical:** Speed is essential. Enzyme begins cleaving substrate immediately upon addition. Delay between enzyme addition and first plate read should be minimized (<1 minute).

#### 5.2.5 Fluorescence Measurement

**Plate reader settings:**

- **Instrument:** Fluorescence microplate reader
- **Plate type:** 96-well black microplate
- **Measurement mode:** Fluorescence intensity
- **Excitation wavelength:** 360 nm (bandwidth ±10 nm)
- **Emission wavelength:** 460 nm (bandwidth ±10 nm)
- **Optics position:** Bottom read
- **Temperature:** 37°C (use heated chamber if available)
- **Read mode:** Kinetic (time-course)
- **Time interval:** Every 2 minutes
- **Total duration:** 180 minutes (3 hours)
- **Number of reads:** 91 time points (0, 2, 4, ... 180 min)
- **Gain/sensitivity:** Auto-adjust to keep maximum signal between 20,000-60,000 RFU (prevents saturation)
- **Shaking:** Linear shaking for 5 seconds before each read (prevents settling)
- **Wells to read:** A1-A6, B4-B6 (9 wells total)

**Monitoring during run:**

- Check first 3 time points (0, 2, 4 min) to ensure read is functioning
- At 30 minutes: Check if GAN peptide wells (B4-B6) show initial fluorescence increase
- At 60 minutes: Assess trend in GAN peptide wells fluorescence
- Continue full 180 minutes even if signal appears weak (some substrates cleave slowly)

#### 5.2.6 Data Export

1. After run completion, export raw data as CSV or Excel file
2. Data should include: Time (min), Well ID, Fluorescence (RFU)
3. Save file with descriptive name: "YYYYMMDD_KLK2_EGSCYGTR_Run#.csv"
4. Create backup copy in separate location

---

## 6. Safety Considerations

### 6.1 Chemical Safety

**DMSO (Dimethyl Sulfoxide):**

- **Hazards:** Skin and eye irritant, readily penetrates skin carrying dissolved chemicals
- **Handling:** Wear nitrile gloves and safety glasses. Work in fume hood when handling large volumes. Avoid skin contact.
- **First aid:** If skin contact occurs, wash immediately with soap and water for 15 minutes. If eye contact, rinse with water for 15 minutes and seek medical attention.
- **MSDS attached:** Yes (Appendix A)

**Tris base:**

- **Hazards:** Irritant to skin, eyes, and respiratory tract
- **Handling:** Wear gloves and safety glasses when weighing powder. Avoid inhalation of dust.
- **First aid:** If inhaled, move to fresh air. If skin/eye contact, rinse with water.
- **MSDS attached:** Yes (Appendix A)

**Hydrochloric acid (1 M):**

- **Hazards:** Corrosive to skin and eyes. Causes severe burns.
- **Handling:** Wear chemical-resistant gloves, safety glasses, and lab coat. Handle in fume hood. Add acid to water, never water to acid.
- **First aid:** If contact occurs, rinse affected area with water for 15 minutes. Seek immediate medical attention for eye contact.
- **MSDS attached:** Yes (Appendix A)

**Tween-20:**

- **Hazards:** Mild irritant
- **Handling:** Wear gloves and safety glasses
- **MSDS attached:** Yes (Appendix A)

### 6.2 Biological Safety

**Recombinant proteins (Kallikrein 2):**

- **Biosafety level:** BSL-1 (recombinant protein, non-infectious)
- **Handling:** Wear gloves to prevent contamination. Avoid generating aerosols.
- **Disposal:** Deactivate by adding bleach (10% final concentration) and incubating for 30 minutes before disposal in biological waste

**Peptide substrates:**

- **Biosafety level:** BSL-1 (synthetic peptides, non-infectious)
- **Handling:** Wear gloves
- **Disposal:** Chemical waste disposal per institutional guidelines

### 6.3 Equipment Safety

**Plate reader:**

- Ensure proper electrical grounding
- Do not open chamber during heated operation (burn hazard)
- Follow manufacturer's operation manual

**Water bath/incubator:**

- Do not overfill water bath (electrical hazard)
- Handle warm items with heat-resistant gloves

### 6.4 Waste Disposal

**Biological/chemical waste:**

- Liquid waste containing enzyme and peptides: Treat with 10% bleach for 30 minutes, then dispose in designated liquid waste container
- Plastic consumables (tips, tubes, plates): Dispose in biohazard waste bag
- Sharps (needles, if used): Dispose in sharps container

**DMSO-containing waste:**

- Collect in designated organic solvent waste container
- Do not mix with bleach or oxidizing agents
- Label clearly: "Waste DMSO"

**Buffer waste:**

- Tris/salt buffers can be disposed in sanitary sewer after pH neutralization (pH 6-8)

### 6.5 Personal Protective Equipment (PPE)

**Required PPE for all procedures:**

- Nitrile gloves (replace frequently)
- Safety glasses or goggles
- Laboratory coat (cotton or Nomex, knee-length)
- Closed-toe shoes
- Long pants (no shorts)

**Additional PPE when handling acids:**

- Chemical-resistant gloves (nitrile or neoprene)
- Face shield

---

## 7. Data Analysis and Statistics

### 7.1 Data Processing

**1. Background subtraction:**

Calculate mean fluorescence of blank wells (A1-A3) at each time point and subtract from all other wells:

$$
\text{RFU}_{\text{corrected}} = \text{RFU}_{\text{raw}} - \text{RFU}_{\text{blank, mean}}
$$

**2. Calculate mean and standard deviation for each condition:**

For each time point, calculate mean and standard deviation (SD) of technical triplicates:

$$
\text{Mean RFU} = \frac{1}{n}\sum_{i=1}^{n} \text{RFU}_{i}
$$

$$
\text{SD} = \sqrt{\frac{1}{n-1}\sum_{i=1}^{n}(\text{RFU}_{i} - \text{Mean RFU})^{2}}
$$

Where n = 3 (technical replicates)

**3. Calculate coefficient of variation (CV):**

$$
\text{CV (\%)} = \frac{\text{SD}}{\text{Mean}} \times 100
$$

**Acceptance criterion:** CV < 15% for technical triplicates

### 7.2 Kinetic Analysis

**1. Calculate initial velocity (V0):**

Determine slope of fluorescence vs. time curve during linear phase (typically 0-30 minutes):

$$
V_{0} = \frac{\Delta \text{RFU}}{\Delta \text{Time (min)}}
$$

Units: RFU/min

**2. Calculate fold-change over substrate-only control:**

At endpoint (180 min):

$$
\text{Fold-change} = \frac{\text{RFU}_{\text{test, 180 min}} - \text{RFU}_{\text{substrate only, 180 min}}}{\text{RFU}_{\text{substrate only, 180 min}}}
$$

**Positive result threshold:** Fold-change ≥ 2.0 (at least 2-fold increase above substrate-only control)

### 7.3 Statistical Hypothesis Testing

**Comparison:** Test wells (GAN + Enzyme) vs. Substrate-only control at endpoint (180 min)

**Null hypothesis (H₀):** There is no significant difference in fluorescence between test wells and substrate-only controls (mean difference = 0)

**Alternative hypothesis (H₁):** Test wells show significantly higher fluorescence than substrate-only controls (mean difference > 0)

**Statistical test:** Two-sample t-test (Student's t-test)

**Assumptions:**
- Data are normally distributed (verify with Shapiro-Wilk test)
- Equal variances (verify with F-test or Levene's test)
- Independent samples

**Significance level:** α = 0.05 (95% confidence)

**Test statistic:**

$$
t = \frac{\bar{x}_{1} - \bar{x}_{2}}{s_{p}\sqrt{\frac{1}{n_{1}} + \frac{1}{n_{2}}}}
$$

Where:
- $\bar{x}_{1}$ = mean RFU of test wells
- $\bar{x}_{2}$ = mean RFU of substrate-only controls
- $s_{p}$ = pooled standard deviation
- $n_{1}, n_{2}$ = sample sizes

**Degrees of freedom:** df = n₁ + n₂ - 2

**Decision rule:**
- If p-value < 0.05: Reject H₀, conclude significant cleavage occurred
- If p-value ≥ 0.05: Fail to reject H₀, no evidence of cleavage

**Software:** GraphPad Prism, R, or Python (scipy.stats)

### 7.4 Visualization

**Figures to generate:**

1. **Kinetic curves:** Fluorescence (RFU) vs. Time (min)
   - Plot mean ± SD for each condition
   - Include all conditions on same graph with different colors/symbols

2. **Bar graph:** Endpoint fluorescence (180 min) for each condition
   - Include error bars (SD or SEM)
   - Indicate statistical significance with asterisks (*, p<0.05; **, p<0.01; ***, p<0.001)

3. **Initial velocity comparison:** Bar graph of V₀ for test vs. controls

### 7.5 Criteria for Success

**Positive result (hypothesis supported):**

- GAN peptide + enzyme shows fluorescence increase ≥2-fold over substrate-only control
- Difference is statistically significant (p < 0.05)
- Result is reproducible across biological replicates
- Substrate-only controls remain stable (no spontaneous fluorescence)
- Blanks remain low and stable throughout

**Negative result (hypothesis not supported):**

- GAN peptide + enzyme shows no significant fluorescence increase over substrate-only control
- Test wells behave identically to substrate-only controls
- Fluorescence remains at baseline levels throughout 180 minutes

**Invalid experiment (must repeat):**

- High variability within technical replicates (CV > 15%)
- Substrate-only controls show increasing fluorescence (peptide instability)
- Inconsistent results across biological replicates
- Equipment malfunction or improper settings

---

## 8. Expected Results and Interpretation

**Positive Result:** GAN peptide + enzyme shows ≥2-fold fluorescence increase over substrate-only controls. **Conclusion:** Validates GAN prediction - EGSCYGTR is a Kallikrein 2 substrate. **Next steps:** Determine cleavage site, calculate kinetics, test additional peptides.

**Negative Result:** No fluorescence increase in enzyme-treated wells. **Conclusion:** EGSCYGTR is not cleaved despite computational prediction. Indicates binding affinity doesn't always correlate with cleavage. **Next steps:** Refine GAN training, test other predicted peptides.

**Weak Cleavage:** Small fluorescence increase (1.2-1.8 fold). **Conclusion:** EGSCYGTR is a poor substrate. GAN captured partial specificity. **Next steps:** Optimize sequence, test at higher enzyme concentrations.

---

## 9. Bibliography and References

### 9.1 Protease Substrate Specificity

1. **Schechter, I., & Berger, A.** (1967). On the size of the active site in proteases. I. Papain. *Biochemical and Biophysical Research Communications*, 27(2), 157-162. doi:10.1016/S0006-291X(67)80055-X
   - Defines P1-P1' nomenclature for protease cleavage sites

2. **Rawlings, N. D., Barrett, A. J., Thomas, P. D., Huang, X., Bateman, A., & Finn, R. D.** (2018). The MEROPS database of proteolytic enzymes, their substrates and inhibitors in 2017 and a comparison with peptidases in the PANTHER database. *Nucleic Acids Research*, 46(D1), D624-D632. doi:10.1093/nar/gkx1134
   - Source of protease cleavage site training data

### 10.2 Kallikrein 2 Biology and Substrates

3. **Veveris-Lowe, T. L., Lawrence, M. G., Collard, R. L., Bui, L., Herington, A. C., Nicol, D. L., & Clements, J. A.** (2005). Kallikrein 2 (hK2) and prostate-specific antigen (PSA): Two related, but separate, kallikrein enzymes. *Clinical Chemistry*, 51(10), 1786-1796. doi:10.1373/clinchem.2005.053181

4. **Deperthes, D., Frenette, G., Brillard-Bourdet, M., Bourgeois, L., Gauthier, F., Tremblay, R. R., & Dubé, J. Y.** (1996). Potential involvement of kallikrein hK2 in the hydrolysis of the human seminal vesicle proteins after ejaculation. *Journal of Andrology*, 17(6), 659-665.

### 10.3 Fluorogenic Substrate Assays

5. **Zimmerman, M., Yurewicz, E., & Patel, G.** (1976). A new fluorogenic substrate for chymotrypsin. *Analytical Biochemistry*, 70(1), 258-262. doi:10.1016/S0003-2697(76)80066-8
   - Development of AMC-based protease substrates

6. **Castillo, M. J., Nakajima, K., Zimmerman, M., & Powers, J. C.** (1979). Sensitive substrates for human leukocyte and porcine pancreatic elastase: a study of the merits of various chromophoric and fluorogenic leaving groups in assays for serine proteases. *Analytical Biochemistry*, 99(1), 53-64. doi:10.1016/0003-2697(79)90043-5

### 10.4 Generative Adversarial Networks

7. **Goodfellow, I., Pouget-Abadie, J., Mirza, M., Xu, B., Warde-Farley, D., Ozair, S., Courville, A., & Bengio, Y.** (2014). Generative adversarial nets. *Advances in Neural Information Processing Systems*, 27, 2672-2680.
   - Original GAN paper

8. **Gupta, A., & Zou, J.** (2019). Feedback GAN for DNA optimizes protein functions. *Nature Machine Intelligence*, 1(2), 105-111. doi:10.1038/s42256-019-0017-4
   - Application of GANs to protein sequence design

### 10.5 Molecular Docking

9. **Trott, O., & Olson, A. J.** (2010). AutoDock Vina: improving the speed and accuracy of docking with a new scoring function, efficient optimization, and multithreading. *Journal of Computational Chemistry*, 31(2), 455-461. doi:10.1002/jcc.21334
   - AutoDock Vina methodology

### 10.6 Statistical Analysis

10. **Motulsky, H. J.** (2014). *Intuitive Biostatistics: A Nonmathematical Guide to Statistical Thinking* (3rd ed.). Oxford University Press.
    - Reference for t-test and data analysis

### 10.7 Laboratory Safety

11. **Material Safety Data Sheets (MSDS):**
    - DMSO: Sigma-Aldrich MSDS for product D2650
    - Tris base: Sigma-Aldrich MSDS for product T1503
    - Hydrochloric acid: Sigma-Aldrich MSDS for product H9892
    - Tween-20: Sigma-Aldrich MSDS for product P1379
    - **All MSDS sheets attached in Appendix A**

12. **Occupational Safety and Health Administration (OSHA).** (2012). *Laboratory Safety Guidance*. U.S. Department of Labor. Retrieved from https://www.osha.gov/Publications/laboratory/OSHA3404laboratory-safety-guidance.pdf

### 10.8 Plate Reader Methodology

13. **Molecular Devices.** (2018). *SpectraMax Microplate Reader User Guide*. Molecular Devices LLC.
    - Fluorescence detection methodology

**Note:** MSDS sheets for all chemicals (DMSO, Tris, HCl, Tween-20, NaCl) available from Sigma-Aldrich.
