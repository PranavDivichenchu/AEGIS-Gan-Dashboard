# Plate Reader Assay Product Sheet
## Kallikrein 2 Substrate Cleavage Assay - GAN-Designed Peptide Validation

**Project:** Sepsis Protease Inhibitor Design using GANs and Molecular Docking
**Name:** Pranav Divichenchu
**Pathway:** Academy of Engineering and Technology (AET)
**Date Prepared:** December 8, 2024
**Meeting with:** Dr. Hanson (Plate Reader Access - December 6, 2024)

---

## 1. Project Overview & Objectives

### Background
This experimental validation aims to test whether a GAN-designed peptide sequence (EGSCYGTE) can function as a cleavable substrate for human Kallikrein 2 (hK2). The peptide was generated using a Generative Adversarial Network trained on protease substrate data from the MEROPS database and showed a predicted binding affinity of -9.72 kcal/mol through molecular docking simulations.

### Primary Objective
**Test if Kallikrein 2 can cleave the GAN-designed peptide EGSCYGTE**

The peptide will be synthesized with a fluorophore attached. When Kallikrein 2 cleaves the peptide at the predicted cleavage site, the fluorophore is released, resulting in an increase in fluorescence signal.

### Hypothesis
- **H1:** Kallikrein 2 will recognize and cleave the GAN-designed peptide EGSCYGTE at one or more positions
- **H2:** Fluorescence will increase over time as the peptide is cleaved and fluorophore is released
- **H3:** The computational prediction (binding affinity -9.72 kcal/mol) indicates this peptide will be a good substrate

### Success Criteria
- Measurable increase in fluorescence over time when peptide + enzyme are incubated together
- No fluorescence increase in control (peptide alone, no enzyme)
- Clear kinetic curve showing enzyme activity
- Ability to calculate cleavage rate (kcat/Km)

---

## 2. Assay Design

### Assay Type
**Fluorometric Substrate Cleavage Assay**

### Detection Principle
The GAN-designed peptide (EGSCYGTE) is synthesized with a fluorophore (AMC, AFC, or EDANS) attached at the C-terminus or as part of a FRET pair. When Kallikrein 2 cleaves the peptide, the fluorophore is released or dequenched, causing fluorescence to increase.

### Two Possible Substrate Designs

**Option 1: Direct Fluorophore Conjugate (Simpler)**
- Peptide-AMC: EGSCYGTE-AMC
- When cleaved, free AMC is released → fluorescence increases
- Detection: Ex 360 nm / Em 460 nm

**Option 2: FRET-based Substrate (More Expensive)**
- EDANS-EGSCYGTE-DABCYL or MCA-EGSCYGTE-DNP
- FRET pair is separated upon cleavage → fluorescence increases
- Detection: Ex/Em depends on FRET pair

**Recommendation:** Start with Option 1 (Peptide-AMC) - simpler and cheaper

---

## 3. Materials & Reagents

### Test Substrate (GAN-Designed Peptide with Fluorophore)

**Peptide Sequence:** EGSCYGTE-AMC
- **Full Name:** Glu-Gly-Ser-Cys-Tyr-Gly-Thr-Glu-AMC
- **Modification:** C-terminal AMC (7-amino-4-methylcoumarin) conjugate
- **Vendor:** GenScript, Bachem, AnaSpec, or LifeTein (custom peptide synthesis)
- **Purity:** ≥95% by HPLC
- **Amount:** 1-5 mg
- **Analysis Required:** HPLC + MS confirmation of AMC conjugation
- **Storage:** -20°C, desiccated, protect from light
- **Cost:** $300-600 (C-terminal AMC conjugation adds $100-200 to base peptide cost)

**Alternative if AMC not available:**
- EGSCYGTE-AFC (7-amino-4-trifluoromethylcoumarin): Ex 400 nm / Em 505 nm
- EGSCYGTE-pNA (para-nitroaniline): Absorbance at 405 nm (colorimetric, not fluorescence)

### Enzyme

**Recombinant Human Kallikrein 2 (hK2)**
- **Vendor:** R&D Systems (Cat# 1116-SE), Sino Biological, Fitzgerald Industries
- **Form:** Lyophilized or solution
- **Specific Activity:** >1,000 pmol/min/µg
- **Working Concentration:** 15 nM (final in assay)
- **Quantity:** 10 µg (sufficient for ~50 assays)
- **Storage:** -80°C in single-use aliquots
- **Cost:** ~$300-450 per 10 µg

### Positive Control Substrate

**Commercial Kallikrein Substrate (to validate enzyme activity)**
- Boc-Phe-Ser-Arg-AMC or H-D-Pro-Phe-Arg-AMC
- **Vendor:** Bachem, Enzo Life Sciences
- **Purpose:** Confirm enzyme is active before testing GAN peptide
- **Cost:** $200-300 per 5 mg

### Assay Buffer

**Kallikrein Assay Buffer:**
- 50 mM Tris-HCl, pH 8.0
- 100 mM NaCl
- 0.01% Tween-20
- Optional: 1 mM EDTA

**Preparation:**
- 500 mL stock, sterile filter (0.22 µm)
- Store at 4°C
- Warm to 37°C before use

### Additional Reagents
- **DMSO:** For substrate stock solutions (10-50 mM)
- **Stop Solution (optional):** 30% acetic acid or 0.2 M glycine pH 2.0 (stops enzyme reaction for endpoint reading)

---

## 4. Plate Layout & Experimental Design

### 96-Well Plate Layout (Simplified)

```
        1      2      3      4      5      6      7      8      9     10     11     12
    ┌──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┐
  A │Blank │Blank │Blank │ GAN  │ GAN  │ GAN  │ Pos  │ Pos  │ Pos  │      │      │      │
    │      │      │      │ only │ only │ only │Ctrl  │Ctrl  │Ctrl  │      │      │      │
    │      │      │      │(no E)│(no E)│(no E)│(no E)│(no E)│(no E)│      │      │      │
    ├──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤
  B │      │      │      │ GAN  │ GAN  │ GAN  │ Pos  │ Pos  │ Pos  │      │      │      │
    │      │      │      │ +Enz │ +Enz │ +Enz │ +Enz │ +Enz │ +Enz │      │      │      │
    │      │      │      │ 15nM │ 15nM │ 15nM │ 15nM │ 15nM │ 15nM │      │      │      │
    └──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┘
```

**Legend:**
- **Blank:** Buffer only (background fluorescence)
- **GAN only (no E):** GAN peptide (EGSCYGTE-AMC) WITHOUT enzyme (proves substrate doesn't auto-fluoresce)
- **GAN +Enz:** GAN peptide WITH Kallikrein 2 enzyme (15 nM) - **THIS IS THE TEST**
- **Pos Ctrl +Enz:** Commercial kallikrein substrate (Boc-FSR-AMC) WITH enzyme (15 nM) - proves enzyme is active

### Experimental Conditions

**Single enzyme concentration:** 15 nM Kallikrein 2
**Single substrate concentration:** 100 µM for both GAN peptide and positive control
**Replicates:** Triplicates for each condition

### Total Wells Required
- 3 blanks (buffer only)
- 3 GAN peptide-only controls (no enzyme)
- 3 GAN peptide + enzyme (THE TEST)
- 3 positive control substrate-only (no enzyme)
- 3 positive control + enzyme (validates enzyme works)
- **Total: 15 wells (less than 1/6 of a 96-well plate)**

**Note:** Remaining wells can be used for replicates or saved for future experiments

---

## 5. Experimental Protocol

### Step 1: Preparation (30 min)

**1.1 Prepare Substrate Stock Solutions**
- Dissolve GAN peptide (EGSCYGTE-AMC) in DMSO to make 10 mM stock
  - Example: 1 mg peptide (MW ~1,000 Da) in ~100 µL DMSO
- Dissolve positive control substrate (Boc-FSR-AMC) in DMSO to 10 mM
- Vortex, centrifuge briefly
- Store at -20°C in aliquots

**1.2 Prepare Working Substrate Solution**
- Dilute both substrate stocks in assay buffer to 200 µM (2× final concentration)
  - Example: 2 µL of 10 mM stock + 98 µL assay buffer = 200 µM
- Keep on ice, protect from light

**1.3 Prepare Enzyme Working Solution**
- Thaw enzyme aliquot on ice
- Dilute in assay buffer to 30 nM (2× final concentration)
  - Final concentration in assay will be 15 nM after mixing
- Keep on ice

**1.4 Pre-warm Assay Buffer**
- Warm buffer to 37°C (or room temperature if no temp control available)

---

### Step 2: Plate Setup (10 min)

**2.1 Add Substrate to Wells**
- **Blanks (A1-A3):** Add 100 µL assay buffer only
- **Substrate-only controls (A4-A6 for GAN, A7-A9 for positive control):**
  - Add 50 µL substrate working solution (200 µM)
  - Add 50 µL assay buffer (no enzyme)
- **Test wells (B4-B6 for GAN, B7-B9 for positive control):**
  - Add 50 µL substrate working solution (200 µM)
  - DO NOT add enzyme yet (add in next step)

**2.2 Add Enzyme to Initiate Reaction**
- Pipette 50 µL enzyme working solution (30 nM) into test wells B4-B9
- Mix gently by tapping plate
- **Final volume:** 100 µL per well
- **Final concentrations:**
  - Substrate: 100 µM (both GAN peptide and positive control)
  - Enzyme: 15 nM Kallikrein 2

---

### Step 3: Kinetic Reading (1-3 hours)

**3.1 Immediately Place Plate in Reader**
- Load plate into plate reader
- Start kinetic protocol

**3.2 Reading Parameters**
- **Mode:** Kinetic (time-course)
- **Interval:** Every 2-5 minutes
- **Duration:** 60-180 minutes (depends on cleavage rate)
- **Temperature:** 37°C (if available)

**3.3 Monitor Progress**
- Check first few reads to ensure signal is increasing in positive control wells
- Fluorescence should be steadily rising by 30-60 min
- GAN peptide signal may be slower to develop - wait for full 2-3 hour run

---

### Step 4: Data Collection

**Export Data:**
- Save raw fluorescence data (RFU vs. time) as Excel or CSV
- Include plate map and metadata (date, enzyme lot, substrate lot)

---

## 6. Plate Reader Settings & Requirements

### Required Plate Reader Capabilities

**Essential:**
1. **Fluorescence detection** - Excitation 360 nm / Emission 460 nm (for AMC)
2. **96-well plate** - Bottom reading capability (for black plates)
3. **Kinetic mode** - Time-series measurements every 2-5 min for 1-3 hours
4. **Temperature control (preferred):** 37°C

### Specific Settings

| Parameter | Setting |
|-----------|---------|
| **Measurement Type** | Fluorescence Intensity |
| **Plate Type** | 96-well black microplate (Corning 3915 or equivalent) |
| **Read Mode** | Kinetic |
| **Excitation** | 360 nm (±10 nm) |
| **Emission** | 460 nm (±10 nm) |
| **Optics** | Bottom read |
| **Gain/Sensitivity** | Auto-adjust (target 20,000-60,000 RFU at endpoint) |
| **Temperature** | 37°C (if available) |
| **Interval** | 2-5 minutes |
| **Duration** | 120-180 minutes |
| **Shaking** | Optional: 5 sec before each read |

---

## 7. Data Analysis Plan

### Step 1: Quality Control

**Check Controls:**
- **Blank wells:** Low, stable RFU (<1,000)
- **Substrate-only wells:** Minimal increase (substrate should be stable without enzyme)
- **Positive control (commercial substrate + enzyme):** Strong fluorescence increase → confirms enzyme is active

### Step 2: Plot Kinetic Curves

**Create Time-Course Plots:**
- X-axis: Time (minutes)
- Y-axis: Fluorescence (RFU)
- Plot curves for all conditions on same graph

**Expected Result:**
- Blank: Low, flat baseline
- Substrate-only (no enzyme): Flat line, minimal increase
- GAN peptide + enzyme: Increasing fluorescence (if peptide is cleaved)
- Positive control + enzyme: Strong increasing fluorescence

### Step 3: Calculate Reaction Velocity

**From Linear Portion of Curve (typically first 30-60 min):**
```
Velocity (V) = ΔRFU / Δtime (units: RFU/min)
```

Use linear regression on the kinetic data to determine slope

### Step 4: Calculate Cleavage Efficiency

**Relative Activity:**
```
Relative Activity = V_GAN_peptide / V_positive_control × 100%
```

This tells you how efficiently Kallikrein 2 cleaves your GAN peptide compared to a known good substrate.

**Example interpretation:**
- Relative Activity = 80% → GAN peptide is an excellent substrate (cleaved almost as well as commercial substrate)
- Relative Activity = 20% → GAN peptide is cleaved but less efficiently
- Relative Activity < 5% → GAN peptide is poorly cleaved or not a substrate

### Step 5: Determine if Peptide is Cleaved

**Success Indicators:**
- Fluorescence increases over time (at least 2-5× over substrate-only control)
- Clear difference between substrate-only vs. substrate + enzyme wells
- Curve shape is similar to positive control (linear increase or gradual saturation)

**If No Cleavage:**
- Fluorescence stays flat (similar to substrate-only control)
- No difference between wells with and without enzyme
- Possible reasons: Peptide is not a substrate, fluorophore attachment prevents binding, or wrong cleavage site predicted

---

## 8. Expected Results & Interpretation

### Scenario 1: GAN Peptide IS Cleaved (Success!)
- **Observation:** Fluorescence increases steadily over time
- **Interpretation:** GAN successfully predicted a substrate sequence; computational approach validated
- **Next Steps:** Determine exact cleavage site via mass spectrometry; test other GAN peptides

### Scenario 2: GAN Peptide is NOT Cleaved (Negative Result)
- **Observation:** Fluorescence remains flat (similar to substrate-only control), while positive control shows strong increase
- **Interpretation:**
  - Peptide may bind but not be in correct orientation for cleavage
  - Computational prediction was a false positive
  - Fluorophore attachment sterically blocks cleavage
  - Enzyme is working (positive control proves this) but GAN peptide is not a substrate
- **Next Steps:**
  - Try different fluorophore position (N-terminal instead of C-terminal)
  - Test unmodified peptide via mass spectrometry (direct detection of cleavage products)
  - Select different GAN candidate with different sequence

### Scenario 3: Weak Cleavage (Moderate Result)
- **Observation:** Small increase in fluorescence (1.5-3× over background), less than positive control
- **Interpretation:** Peptide is cleaved but inefficiently (not an optimal substrate)
- **Next Steps:** Optimize by testing different GAN-generated sequences or modify current sequence based on cleavage site analysis

---

## 9. Budget Summary

| Item | Vendor | Quantity | Unit Price | Total |
|------|--------|----------|------------|-------|
| **GAN Peptide-AMC (EGSCYGTE-AMC)** | GenScript/Bachem | 1-5 mg | $300-600 | $450 |
| **Recombinant Kallikrein 2** | R&D Systems | 10 µg | $300-450 | $375 |
| **Positive Control Substrate (Boc-FSR-AMC)** | Bachem | 5 mg | $200-300 | $250 |
| **96-well Black Microplates** | Corning | 3 plates | $5-10 each | $20 |
| **Assay Buffer Components** | Sigma | Bulk | - | $50 |
| **Consumables (Tips, tubes, DMSO)** | VWR/Fisher | - | - | $30 |
| **TOTAL** | | | | **~$1,175** |

**Budget-Optimized Option (~$800):**
- Skip positive control substrate (use literature values to verify enzyme)
- Order smaller quantity of GAN peptide (1-2 mg instead of 5 mg)
- Use 1-2 plates instead of 3

---

## 10. Timeline

### Week 1: Equipment Access & Training
- **Friday, Dec 6:** Meeting with Dr. Hanson
- Confirm plate reader specs
- Reserve time slots

### Week 2-3: Peptide Synthesis (2-3 weeks)
- Order GAN peptide with AMC conjugation (EGSCYGTE-AMC)
- Order enzyme and positive control substrate
- **Note:** Custom fluorophore conjugation takes longer than standard peptide synthesis

### Week 4: GAN Peptide Testing
- Run cleavage assay with GAN peptide (15 nM enzyme, 100 µM substrate)
- Validate enzyme activity using positive control substrate
- Collect kinetic data over 2-3 hours

### Week 5: Data Analysis & Follow-up
- Analyze kinetic curves and calculate cleavage efficiency
- Determine if GAN peptide is a valid substrate for Kallikrein 2
- If positive: Plan mass spectrometry to identify exact cleavage site
- If negative: Troubleshoot (test different fluorophore position, select different GAN candidate)
- Update journal and plan next experiments

---

## 11. Questions for Dr. Hanson (Meeting Checklist)

### Equipment
- [ ] Does the plate reader support Ex 360 nm / Em 460 nm (for AMC detection)?
- [ ] Can it run kinetic assays for 2-3 hours with readings every 2-5 min?
- [ ] Is temperature control (37°C) available?
- [ ] Does it have bottom reading capability for black plates?

### Access & Scheduling
- [ ] How do I reserve the plate reader?
- [ ] Are there usage fees?
- [ ] Can I run experiments outside regular hours if needed?

### Training & Support
- [ ] Will you provide hands-on training?
- [ ] Is there an SOP I should follow?
- [ ] Who do I contact for technical issues during experiments?

### Data & Software
- [ ] What software does it use?
- [ ] Can I export data to Excel/CSV?
- [ ] How do I save/backup data files?

### Consumables
- [ ] What plate brands are compatible? (Need black 96-well for fluorescence)
- [ ] Do you have fluorescence standards for calibration?

---

## 12. Safety & Waste Disposal

### Hazards
- **Kallikrein 2:** Serine protease (biological material, potential allergen)
- **DMSO:** Skin penetrant, always wear gloves
- **AMC fluorophore:** Low toxicity but handle with care

### PPE
- Lab coat
- Safety glasses
- Nitrile gloves

### Waste Disposal
- Enzyme/peptide solutions: Inactivate with 10% bleach for 1 hour, dispose as biohazard
- Plates: Rinse after inactivation, dispose per institutional guidelines
- DMSO waste: Organic solvent waste container

---

## 13. Appendix: Substrate Synthesis Specifications

### When Ordering EGSCYGTE-AMC from Vendor

**Provide to Peptide Synthesis Company:**
- **Sequence:** Glu-Gly-Ser-Cys-Tyr-Gly-Thr-Glu
- **N-terminus:** Free (NH3+) or Acetylated (Ac-) - specify preference
- **C-terminus:** AMC conjugate (7-amino-4-methylcoumarin)
- **Purity:** ≥95% by HPLC
- **Amount:** 1-5 mg
- **Analysis:** HPLC chromatogram + Mass Spectrometry (MS) confirmation
- **Salt form:** TFA salt acceptable
- **Delivery:** Lyophilized powder

**Ask Vendor:**
- Can you synthesize peptide-AMC conjugates? (Not all vendors offer this)
- What is the turnaround time? (Custom fluorophore conjugation may take 3-4 weeks)
- What is the exact cost for this modification?
- Do you provide a certificate of analysis (CoA)?

**Recommended Vendors for Fluorophore Conjugation:**
- **Bachem:** https://www.bachem.com (specializes in fluorogenic substrates)
- **AnaSpec:** https://www.anaspec.com (expertise in AMC conjugates)
- **GenScript:** https://www.genscript.com (custom peptides with modifications)

---

## 14. Success Metrics

### Technical Success
- [ ] Positive control substrate shows strong fluorescence increase (validates enzyme activity)
- [ ] Substrate-only controls show minimal fluorescence change (confirms substrate stability)
- [ ] Clean kinetic curves with low well-to-well variability (CV < 15%)

### Biological Success
- [ ] GAN peptide shows fluorescence increase >2× substrate-only control
- [ ] Clear difference between GAN peptide + enzyme vs. GAN peptide alone
- [ ] Cleavage kinetics are measurable (can calculate velocity)

### Computational Validation
- [ ] If peptide is cleaved → GAN approach validated
- [ ] Binding affinity (-9.72 kcal/mol) correlates with substrate activity
- [ ] Can proceed to test other GAN-designed peptides

---

**END OF DOCUMENT**

**Document Status:** Ready for Dr. Hanson meeting (December 6, 2024)
**Assay Type:** Substrate Cleavage Assay (NOT inhibition assay)
**Key Reagent:** EGSCYGTE-AMC (custom peptide synthesis with fluorophore conjugation)
**Version:** 2.0 - Corrected for substrate cleavage testing
