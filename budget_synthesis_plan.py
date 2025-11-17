#!/usr/bin/env python3
"""
Budget-Optimized Synthesis Plan ($200-400)
Strategic selection for maximum research value
"""

import pandas as pd

print("="*80)
print("BUDGET-OPTIMIZED PEPTIDE SYNTHESIS PLAN")
print("Budget: $200-400")
print("="*80)

# Load data
panel_df = pd.read_csv('docking_results/27_peptide_panel_synthesis_ready.csv')
inhibitor_df = pd.read_csv('docking_results/27_panel_inhibitor_designs.csv')

# Merge data
merged = panel_df.merge(inhibitor_df, on='Panel_ID')

# Selection criteria for budget-conscious research
# 1. Best binding affinity
# 2. Low cleavage risk (easier to work with)
# 3. Different protease classes (diversity)
# 4. Clinical relevance

# Score each peptide
scores = []
for _, row in merged.iterrows():
    score = 0

    # Binding affinity (most important)
    if row['Binding_Affinity'] < -10:
        score += 50
    elif row['Binding_Affinity'] < -9:
        score += 40
    elif row['Binding_Affinity'] < -8:
        score += 30

    # Low cleavage risk
    if row['Cleavage_Risk'] == 'Low':
        score += 20
    elif row['Num_Cleavage_Sites'] <= 1:
        score += 10

    # Clinical relevance (based on protease importance in sepsis/disease)
    clinical_targets = ['MMP', 'Caspase-3', 'Thrombin', 'Proteinase 3', 'Kallikrein']
    if any(target in row['Target_Protease_x'] for target in clinical_targets):
        score += 15

    # Synthesis ease (shorter sequences cheaper) - all are 8-mers, so skip
    # if row['Length'] <= 8:
    #     score += 5

    scores.append(score)

merged['Selection_Score'] = scores
merged = merged.sort_values('Selection_Score', ascending=False)

print("\n" + "="*80)
print("TOP 5 CANDIDATES (Ranked by Strategic Value)")
print("="*80)

top5 = merged.head(5)
print(f"\n{'Rank':<5} {'ID':<4} {'Target':<30} {'Affinity':>10} {'Risk':<8} {'Score':>6}")
print("-"*75)
for rank, (_, row) in enumerate(top5.iterrows(), 1):
    print(f"{rank:<5} {int(row['Panel_ID']):<4} {row['Target_Protease_x'][:30]:<30} {row['Binding_Affinity']:>10.3f} {row['Cleavage_Risk']:<8} {row['Selection_Score']:>6.0f}")

# ============================================
# BUDGET SCENARIOS
# ============================================
print("\n" + "="*80)
print("BUDGET SCENARIOS")
print("="*80)

top1 = top5.iloc[0]
top2 = top5.iloc[1]

print("\n--- SCENARIO 1: $250-300 (RECOMMENDED) ---")
print("Strategy: 1 peptide, 2 versions (proof-of-concept)")
print(f"\nPeptide: #{int(top1['Panel_ID'])} - {top1['Target_Protease_x']}")
print(f"Sequence: {top1['Sequence_x']}")
print(f"Binding: {top1['Binding_Affinity']:.3f} kcal/mol")
print(f"Cleavage Risk: {top1['Cleavage_Risk']}")
print("\nOrders:")
print("  1. Unmodified peptide (control)")
print(f"     Sequence: {top1['Sequence_x']}")
print("     Cost: $100-120")
print("     Purpose: Test if it's a substrate vs inhibitor")
print("\n  2. Basic inhibitor (Ac-peptide-NH2)")
print(f"     Sequence: Ac-{top1['Sequence_x']}-NH2")
print("     Cost: $150-180")
print("     Purpose: Test if modifications prevent cleavage")
print("\nTotal Cost: $250-300")
print("Key Test: Compare IC50 values. Inhibitor should be >>100x better")

print("\n--- SCENARIO 2: $350-400 ---")
print("Strategy: 2 peptides, different versions (diversity)")
print(f"\nPeptide A: #{int(top1['Panel_ID'])} - {top1['Target_Protease_x']}")
print(f"  - Basic inhibitor: Ac-{top1['Sequence_x']}-NH2")
print(f"  - Cost: $150-180")
print(f"\nPeptide B: #{int(top2['Panel_ID'])} - {top2['Target_Protease_x']}")
print(f"  - Basic inhibitor: Ac-{top2['Sequence_x']}-NH2")
print(f"  - Cost: $150-180")
print("\nTotal Cost: $300-360")
print("Advantage: Test 2 different proteases, both as inhibitors")
print("Trade-off: No unmodified controls")

print("\n--- SCENARIO 3: $200-250 ---")
print("Strategy: 2 peptides, unmodified only (binding validation)")
print(f"\nPeptide A: #{int(top1['Panel_ID'])} - {top1['Target_Protease_x']}")
print(f"  - Unmodified: {top1['Sequence_x']}")
print(f"  - Cost: $100-120")
print(f"\nPeptide B: #{int(top2['Panel_ID'])} - {top2['Target_Protease_x']}")
print(f"  - Unmodified: {top2['Sequence_x']}")
print(f"  - Cost: $100-120")
print("\nTotal Cost: $200-240")
print("Limitation: Can only test binding, not inhibition")
print("Use case: If you want to validate docking predictions first")

# ============================================
# RECOMMENDED CHOICE
# ============================================
print("\n" + "="*80)
print("RECOMMENDATION")
print("="*80)

print("\n✓ SCENARIO 1 (1 peptide, 2 versions) is BEST for your budget")
print("\nWhy:")
print("  • Answers critical question: substrate vs inhibitor?")
print("  • Direct comparison between modified and unmodified")
print("  • Proof-of-concept for your approach")
print("  • Best scientific value per dollar")

print(f"\n✓ TOP CHOICE: Panel #{int(top1['Panel_ID'])}")
print(f"  Target: {top1['Target_Protease_x']}")
print(f"  Sequence: {top1['Sequence_x']}")
print(f"  Affinity: {top1['Binding_Affinity']:.3f} kcal/mol")
print(f"  Why this one:")
print(f"    - Excellent binding affinity (<{top1['Binding_Affinity']:.1f} kcal/mol)")
print(f"    - {top1['Cleavage_Risk']} cleavage risk")
print(f"    - Clinically relevant target")
print(f"    - {top1['Protease_Class_x']} - well-studied inhibitor chemistry")

# ============================================
# SYNTHESIS SPECIFICATIONS
# ============================================
print("\n" + "="*80)
print("SYNTHESIS SPECIFICATIONS FOR VENDOR")
print("="*80)

synthesis_orders = [
    {
        'Order_ID': 'A1',
        'Peptide_Name': f'Panel{int(top1["Panel_ID"])}_Unmodified',
        'Sequence': top1['Sequence_x'],
        'N_terminus': 'Free (NH3+)',
        'C_terminus': 'Free (COO-)',
        'Purity': '≥95% (HPLC)',
        'Amount': '1-2 mg',
        'Modifications': 'None',
        'Est_Cost': '$100-120'
    },
    {
        'Order_ID': 'A2',
        'Peptide_Name': f'Panel{int(top1["Panel_ID"])}_BasicInhibitor',
        'Sequence': top1['Sequence_x'],
        'N_terminus': 'Acetylated (Ac-)',
        'C_terminus': 'Amidated (-NH2)',
        'Purity': '≥95% (HPLC)',
        'Amount': '1-2 mg',
        'Modifications': 'N-terminal acetylation, C-terminal amidation',
        'Est_Cost': '$150-180'
    }
]

print("\nORDER A1 - Unmodified Control")
print(f"  Peptide Name: Panel{int(top1['Panel_ID'])}_Unmodified_{top1['Target_Protease_x'].replace(' ', '_')}")
print(f"  Sequence: {top1['Sequence_x']}")
print(f"  N-terminus: Free (NH3+)")
print(f"  C-terminus: Free (COO-)")
print(f"  Purity: ≥95% by HPLC")
print(f"  Amount: 1-2 mg")
print(f"  Salt form: TFA salt acceptable")
print(f"  Estimated cost: $100-120")

print("\nORDER A2 - Basic Inhibitor")
print(f"  Peptide Name: Panel{int(top1['Panel_ID'])}_Inhibitor_{top1['Target_Protease_x'].replace(' ', '_')}")
print(f"  Sequence: Ac-{top1['Sequence_x']}-NH2")
print(f"  N-terminus: Acetylated (Ac-)")
print(f"  C-terminus: Amidated (-NH2)")
print(f"  Purity: ≥95% by HPLC")
print(f"  Amount: 1-2 mg")
print(f"  Salt form: TFA salt acceptable")
print(f"  Modifications: N-acetylation, C-amidation")
print(f"  Estimated cost: $150-180")

# Save to CSV
synthesis_df = pd.DataFrame(synthesis_orders)
output_file = 'docking_results/budget_synthesis_order.csv'
synthesis_df.to_csv(output_file, index=False)
print(f"\n✓ Synthesis specifications saved to: {output_file}")

# ============================================
# VENDOR RECOMMENDATIONS
# ============================================
print("\n" + "="*80)
print("RECOMMENDED VENDORS (Budget-Friendly)")
print("="*80)

vendors = [
    {
        'name': 'GenScript',
        'website': 'www.genscript.com/peptide-synthesis',
        'typical_cost': '$90-150/peptide',
        'turnaround': '2-3 weeks',
        'notes': 'Good quality, academic discounts available'
    },
    {
        'name': 'GeneCust',
        'website': 'www.genecust.com',
        'typical_cost': '$80-140/peptide',
        'turnaround': '2-4 weeks',
        'notes': 'EU-based, competitive pricing'
    },
    {
        'name': 'Biomatik',
        'website': 'www.biomatik.com',
        'typical_cost': '$100-160/peptide',
        'turnaround': '2-3 weeks',
        'notes': 'Custom modifications available'
    },
    {
        'name': 'LifeTein',
        'website': 'www.lifetein.com',
        'typical_cost': '$95-145/peptide',
        'turnaround': '2-3 weeks',
        'notes': 'Academic pricing, good for small orders'
    }
]

for vendor in vendors:
    print(f"\n{vendor['name']}")
    print(f"  Website: {vendor['website']}")
    print(f"  Typical cost: {vendor['typical_cost']}")
    print(f"  Turnaround: {vendor['turnaround']}")
    print(f"  Notes: {vendor['notes']}")

# ============================================
# TESTING PLAN
# ============================================
print("\n" + "="*80)
print("TESTING PLAN (After Receiving Peptides)")
print("="*80)

print("\nStep 1: Initial Validation")
print("  • Verify purity (should have HPLC/MS report from vendor)")
print("  • Dissolve in DMSO or appropriate buffer")
print("  • Prepare stock solutions (1-10 mM)")

print("\nStep 2: Binding Assay (if equipment available)")
print("  • Surface Plasmon Resonance (SPR)")
print("  • Fluorescence polarization")
print("  • OR skip to inhibition if no binding equipment")

print("\nStep 3: Inhibition Assay (CRITICAL TEST)")
print("  • Use fluorogenic substrate for target protease")
print("  • Test both peptides at multiple concentrations")
print("  • Calculate IC50 values")
print("  • EXPECTATION: Inhibitor should have IC50 100-1000x lower than unmodified")

print("\nStep 4: Data Interpretation")
print("  • If unmodified has poor IC50 → it's a substrate (gets cleaved)")
print("  • If Ac-peptide-NH2 has good IC50 → successful inhibitor!")
print("  • This validates your GAN + docking approach")

print("\nStep 5: Next Steps (if successful)")
print("  • Synthesize more top candidates")
print("  • Try enhanced versions (with warheads)")
print("  • Publish results!")
print("  • Apply for funding based on proof-of-concept")

# ============================================
# ALTERNATIVE: START WITH COMPUTATIONAL ONLY
# ============================================
print("\n" + "="*80)
print("ALTERNATIVE: $0 OPTION (Computational Only)")
print("="*80)

print("\nBefore spending money, you could:")
print("  1. Run molecular dynamics simulations")
print("  2. Predict ADMET properties")
print("  3. Literature comparison")
print("  4. Present computational results at conferences")
print("  5. Use data to apply for research grants")
print("  6. THEN synthesize with more funding")
print("\nThis approach: Maximize computational validation first")

print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print(f"\nRecommended investment: $250-300")
print(f"Peptide: Panel #{int(top1['Panel_ID'])} - {top1['Target_Protease_x']}")
print(f"Orders: Unmodified + Basic Inhibitor")
print(f"Expected outcome: Proof that modifications create inhibitors")
print(f"Value: Foundation for publication and future funding")
print("\n✓ BUDGET PLAN COMPLETE!")
