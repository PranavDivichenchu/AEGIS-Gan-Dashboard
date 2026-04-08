#!/usr/bin/env python3
"""
run_baseline_comparison.py

Establishes a proper baseline for the three-stage GAN pipeline by running:
  1. Known MEROPS substrates  → "biological baseline" (what real biology produces)
  2. Random 8-mer sequences   → "chance baseline"    (what random guessing produces)
through the same ESMFold → AutoDock Vina pipeline as the GAN-generated sequences,
then produces a side-by-side comparison.

Usage:
  python run_baseline_comparison.py --run      # full pipeline (takes ~1-2 hrs)
  python run_baseline_comparison.py --compare  # just plot from existing results
  python run_baseline_comparison.py --run --n 3   # faster: 3 sequences per protease
"""

import argparse
import os
import sys
import random
import subprocess
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

PROJECT_ROOT = Path(__file__).parent

# Ensure vina (conda docking env) is on PATH for subprocess calls
_CONDA_DOCKING_BIN = Path('/opt/homebrew/Caskroom/miniconda/base/envs/docking/bin')
_ENV = os.environ.copy()
if _CONDA_DOCKING_BIN.exists():
    _ENV['PATH'] = str(_CONDA_DOCKING_BIN) + os.pathsep + _ENV.get('PATH', '')

# ── Amino acid lookup (3-letter → 1-letter, for validation only) ─────────────
AA_3TO1 = {
    'Ala': 'A', 'Arg': 'R', 'Asn': 'N', 'Asp': 'D', 'Cys': 'C',
    'Glu': 'E', 'Gln': 'Q', 'Gly': 'G', 'His': 'H', 'Ile': 'I',
    'Leu': 'L', 'Lys': 'K', 'Met': 'M', 'Phe': 'F', 'Pro': 'P',
    'Ser': 'S', 'Thr': 'T', 'Trp': 'W', 'Tyr': 'Y', 'Val': 'V',
}
AA_1TO3 = {v: k for k, v in AA_3TO1.items()}
STANDARD_AAS = list(AA_3TO1.keys())  # 3-letter codes


# ════════════════════════════════════════════════════════════════════════════════
# PHASE 1 — Build baseline sequence CSVs
# ════════════════════════════════════════════════════════════════════════════════

def extract_merops_substrates(merops_csv: Path, n_per_protease: int = 5,
                               seed: int = 42) -> pd.DataFrame:
    """
    Pull known real substrates from the MEROPS training dataset.
    Uses Label=1 (positive) rows only and reconstructs the 8-mer from P4–P4' columns.
    Returns a DataFrame matching the GAN sequences CSV format.
    """
    np.random.seed(seed)
    random.seed(seed)

    print("  Loading MEROPS dataset...")
    merops = pd.read_csv(merops_csv)

    # Get the target MEROPS IDs from existing generated sequences
    gen_seq = pd.read_csv(PROJECT_ROOT / 'generated_sequences' / 'supremegan_sequences.csv')
    target_ids = set(gen_seq['merops_id'].dropna().unique())
    print(f"  Target proteases: {len(target_ids)}")

    # Keep only positive substrates for our target proteases
    pos = merops[
        (merops['Label'] == 1) &
        (merops['MEROPS_ID'].isin(target_ids))
    ].copy()
    print(f"  Positive MEROPS substrates for target proteases: {len(pos)}")

    # The P4–P4' columns already contain 3-letter AA codes (e.g. "Ile", "Ala").
    # We concatenate them directly — that's the format the pipeline expects.
    p_cols = ['P4', 'P3', 'P2', 'P1', "P1'", "P2'", "P3'", "P4'"]
    pos = pos.dropna(subset=p_cols)

    def build_seq(row):
        parts = [str(row[c]).strip() for c in p_cols]
        # Reject if any position is missing ('-') or not a standard 3-letter code
        if all(p in AA_3TO1 for p in parts):
            return ''.join(parts)
        return None

    pos['sequence'] = pos.apply(build_seq, axis=1)
    pos = pos.dropna(subset=['sequence'])
    # Each 3-letter code is 3 chars, so valid 8-mers are 24 chars
    pos = pos[pos['sequence'].str.len() == 24]
    print(f"  Valid 8-mer MEROPS substrates: {len(pos)}")

    # Sample n_per_protease per protease
    rows = []
    for merops_id, group in pos.groupby('MEROPS_ID'):
        sample = group.sample(min(n_per_protease, len(group)), random_state=seed)
        for _, r in sample.iterrows():
            rows.append({
                'protease_name': r['Protease_Name'],
                'merops_id':     merops_id,
                'sequence':      r['sequence'],
                'model':         'MEROPS_Baseline',
            })

    result = pd.DataFrame(rows)
    print(f"  Extracted {len(result)} sequences across {result['merops_id'].nunique()} proteases")
    return result


def generate_random_sequences(n_per_protease: int = 5, seed: int = 42) -> pd.DataFrame:
    """
    Generate completely random 8-mer peptides for each of the 27 target proteases.
    Each amino acid is drawn uniformly from the 20 standard AAs.
    """
    np.random.seed(seed)
    random.seed(seed)

    gen_seq = pd.read_csv(PROJECT_ROOT / 'generated_sequences' / 'supremegan_sequences.csv')
    proteases = gen_seq[['protease_name', 'merops_id']].drop_duplicates()

    rows = []
    for _, row in proteases.iterrows():
        for _ in range(n_per_protease):
            aa_list = random.choices(STANDARD_AAS, k=8)  # 3-letter codes
            seq = ''.join(aa_list)
            rows.append({
                'protease_name': row['protease_name'],
                'merops_id':     row['merops_id'],
                'sequence':      seq,
                'model':         'Random_Baseline',
            })

    result = pd.DataFrame(rows)
    print(f"  Generated {len(result)} random sequences across {result['protease_name'].nunique()} proteases")
    return result


# ════════════════════════════════════════════════════════════════════════════════
# PHASE 2 — Run pipeline (predict structures → dock)
# ════════════════════════════════════════════════════════════════════════════════

def run_pipeline(sequences_csv: Path, label: str) -> Path | None:
    """
    Run predict_structures.py → molecular_docking.py on a sequences CSV.
    Saves results to docking_results/<label>/docking_results.csv.
    Returns that path, or None on failure.
    """
    dock_dir  = PROJECT_ROOT / 'docking_results' / label
    dock_file = dock_dir / 'docking_results.csv'

    # ── Structure prediction ──────────────────────────────────────────────────
    pred_stem = sequences_csv.stem
    pred_file = PROJECT_ROOT / 'predicted_structures' / f'prediction_results_{pred_stem}.csv'

    if pred_file.exists():
        print(f"  [skip] Structure predictions already exist → {pred_file.name}")
    else:
        print(f"  Predicting structures (ESMFold API) — this may take a while...")
        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / 'predict_structures.py'),
             '--input', str(sequences_csv)],
            cwd=str(PROJECT_ROOT), env=_ENV,
        )
        if result.returncode != 0 or not pred_file.exists():
            print(f"  ERROR: structure prediction failed for {label}")
            return None
        print(f"  Structures saved → {pred_file.name}")

    # ── Molecular docking ─────────────────────────────────────────────────────
    if dock_file.exists():
        print(f"  [skip] Docking results already exist → {dock_file}")
    else:
        dock_dir.mkdir(parents=True, exist_ok=True)
        print(f"  Running AutoDock Vina docking...")
        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / 'molecular_docking.py'),
             '--peptides',   str(pred_file),
             '--proteases',  str(PROJECT_ROOT / 'protease_structures' / 'structure_summary.csv'),
             '--output',     str(dock_dir)],
            cwd=str(PROJECT_ROOT), env=_ENV,
        )
        if result.returncode != 0 or not dock_file.exists():
            print(f"  ERROR: docking failed for {label}")
            return None
        print(f"  Docking saved → {dock_file}")

    return dock_file


# ════════════════════════════════════════════════════════════════════════════════
# PHASE 3 — Load, compare, visualise
# ════════════════════════════════════════════════════════════════════════════════

PALETTE = {
    'Random_Baseline': '#95a5a6',
    'MEROPS_Baseline': '#3498db',
    'SupremeGAN':      '#e74c3c',
    'ConditionalGAN':  '#e67e22',
}

SOURCE_ORDER = ['Random_Baseline', 'MEROPS_Baseline', 'SupremeGAN', 'ConditionalGAN']


def load_all_results() -> pd.DataFrame:
    """Collect every docking result CSV and tag each row with its source label."""
    results_dir = PROJECT_ROOT / 'docking_results'

    files = {
        'SupremeGAN':      results_dir / 'docking_results.csv',
        'ConditionalGAN':  results_dir / 'docking_results_conditionalgan.csv',
        'MEROPS_Baseline': results_dir / 'merops_baseline' / 'docking_results.csv',
        'Random_Baseline': results_dir / 'random_baseline' / 'docking_results.csv',
    }

    frames = []
    for label, path in files.items():
        if path.exists():
            df = pd.read_csv(path)
            df = df[df['status'] == 'success'].copy()
            df['source'] = label
            frames.append(df)
            print(f"  {label:20s}: {len(df):4d} successful dockings")
        else:
            print(f"  {label:20s}: [not found] {path}")

    if not frames:
        sys.exit("No docking results found. Run with --run first.")

    return pd.concat(frames, ignore_index=True)


def print_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """Print and return summary statistics + TOST equivalence test results."""
    present = [s for s in SOURCE_ORDER if s in df['source'].unique()]

    print("\n" + "=" * 72)
    print("BASELINE COMPARISON — SUMMARY STATISTICS")
    print("=" * 72)

    rows = []
    for src in present:
        data = df[df['source'] == src]['binding_affinity']
        rows.append({
            'Source':          src.replace('_', ' '),
            'N':               len(data),
            'Mean (kcal/mol)': round(data.mean(), 3),
            'Std':             round(data.std(), 3),
            'Median':          round(data.median(), 3),
            'Best':            round(data.min(), 3),
            '% < -7 kcal/mol': f"{100*(data < -7).sum()/len(data):.1f}%",
        })

    summary = pd.DataFrame(rows)
    print(summary.to_string(index=False))

    # ── TOST Equivalence Test (gold standard for proving equivalence) ──────────
    # Rationale for δ = 0.75 kcal/mol:
    #   AutoDock Vina's mean unsigned error vs. experimental binding data is
    #   ~1.5-2.0 kcal/mol (Trott & Olson 2010). Two sequences whose predicted
    #   affinities differ by < 0.75 kcal/mol cannot be computationally distinguished.
    #   This margin is therefore the scientifically appropriate threshold for
    #   claiming computational equivalence.
    DELTA = 0.75  # kcal/mol equivalence margin

    print(f"\n{'='*72}")
    print(f"TOST EQUIVALENCE TEST  (δ = {DELTA} kcal/mol)")
    print(f"  H₀: |μ_GAN − μ_baseline| ≥ {DELTA}  (not equivalent)")
    print(f"  H₁: |μ_GAN − μ_baseline| < {DELTA}  (equivalent within docking precision)")
    print(f"  Reject H₀ (prove equivalence) when BOTH p_lower < 0.05 AND p_upper < 0.05")
    print(f"  Equivalence margin justified: within AutoDock Vina's ~1.5–2.0 kcal/mol RMSE")
    print(f"{'='*72}")

    gan_groups = {
        'ConditionalGAN': df[df['source'] == 'ConditionalGAN']['binding_affinity'].dropna(),
        'SupremeGAN':     df[df['source'] == 'SupremeGAN']['binding_affinity'].dropna(),
        'GAN Combined':   df[df['source'].isin(['ConditionalGAN', 'SupremeGAN'])]['binding_affinity'].dropna(),
    }

    for bl in ['MEROPS_Baseline', 'Random_Baseline']:
        if bl not in df['source'].unique():
            continue
        bl_data = df[df['source'] == bl]['binding_affinity'].dropna()
        print(f"\n  Baseline: {bl}  (n={len(bl_data)}, mean={bl_data.mean():.4f})")

        for gan_label, gan_data in gan_groups.items():
            diff = gan_data.mean() - bl_data.mean()
            se   = np.sqrt(gan_data.var(ddof=1)/len(gan_data) + bl_data.var(ddof=1)/len(bl_data))
            df_t = min(len(gan_data) - 1, len(bl_data) - 1)  # conservative Welch df

            # Lower bound: test H₀: μ_diff ≤ -δ  →  reject when t > t_crit
            t_lower = (diff - (-DELTA)) / se
            p_lower = 1 - stats.t.cdf(t_lower, df=df_t)

            # Upper bound: test H₀: μ_diff ≥ +δ  →  reject when t < -t_crit
            t_upper = (diff - DELTA) / se
            p_upper = stats.t.cdf(t_upper, df=df_t)

            equivalent = p_lower < 0.05 and p_upper < 0.05
            verdict    = "EQUIVALENT ✓" if equivalent else "not equiv ✗"

            print(f"    {gan_label:16s}  n={len(gan_data):4d}  diff={diff:+.4f}  "
                  f"p_lower={p_lower:.4f}  p_upper={p_upper:.4f}  → {verdict}")

    # ── Supplementary: KS test (distribution shape) ───────────────────────────
    print(f"\n{'='*72}")
    print("KOLMOGOROV-SMIRNOV TEST  (H₀: same distribution shape)")
    print(f"{'='*72}")
    for bl in ['MEROPS_Baseline', 'Random_Baseline']:
        if bl not in df['source'].unique():
            continue
        bl_data = df[df['source'] == bl]['binding_affinity'].dropna()
        for gan_label, gan_data in gan_groups.items():
            ks, p = stats.ks_2samp(gan_data, bl_data)
            verdict = "Distributions indistinguishable" if p > 0.05 else "Different distributions"
            print(f"  {gan_label:16s} vs {bl:20s}  KS={ks:.4f}  p={p:.4f}  → {verdict}")

    # ── Supplementary: two-sided t-test for context ───────────────────────────
    print(f"\n{'='*72}")
    print("TWO-SIDED t-TEST  (context only — not valid for proving equivalence)")
    print(f"{'='*72}")
    gan_data_all = df[df['source'].isin(['SupremeGAN', 'ConditionalGAN'])]['binding_affinity']
    for bl in ['Random_Baseline', 'MEROPS_Baseline']:
        if bl in df['source'].unique():
            bl_data = df[df['source'] == bl]['binding_affinity']
            t, p    = stats.ttest_ind(gan_data_all, bl_data, equal_var=False)
            sig     = "***" if p < 0.001 else ("**" if p < 0.01 else ("*" if p < 0.05 else "ns"))
            print(f"  GAN vs {bl:20s}  t={t:6.3f}  p={p:.4f}  {sig}")

    return summary


def generate_plots(df: pd.DataFrame, out_dir: Path):
    """Save three publication-ready comparison figures."""
    out_dir.mkdir(parents=True, exist_ok=True)
    present = [s for s in SOURCE_ORDER if s in df['source'].unique()]
    colors  = [PALETTE[s] for s in present]
    labels  = [s.replace('_', '\n') for s in present]

    # ── Figure 1: Violin + box (overall distribution) ────────────────────────
    fig, ax = plt.subplots(figsize=(10, 6))
    df_plot = df.copy()
    df_plot['source'] = pd.Categorical(df_plot['source'], categories=present, ordered=True)
    sns.violinplot(data=df_plot, x='source', y='binding_affinity', hue='source',
                   order=present, palette=PALETTE, inner='box', ax=ax, cut=0, legend=False)
    ax.axhline(-7, color='black', linestyle='--', linewidth=1, alpha=0.5,
               label='Good binding threshold (−7 kcal/mol)')
    for i, src in enumerate(present):
        mean_val = df[df['source'] == src]['binding_affinity'].mean()
        ax.text(i, mean_val - 0.25, f'{mean_val:.2f}', ha='center',
                fontsize=10, fontweight='bold', color='white')
    ax.set_title('Binding Affinity Distribution by Source\n(lower = stronger binding)',
                 fontsize=14, fontweight='bold')
    ax.set_xlabel('')
    ax.set_ylabel('Binding Affinity (kcal/mol)', fontsize=12)
    ax.set_xticks(range(len(present)))
    ax.set_xticklabels(labels, fontsize=11)
    ax.legend(fontsize=9)
    plt.tight_layout()
    fig.savefig(out_dir / 'fig1_overall_distribution.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("  Saved: fig1_overall_distribution.png")

    # ── Figure 2: Histogram overlay ───────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(10, 5))
    for src in present:
        data = df[df['source'] == src]['binding_affinity']
        ax.hist(data, bins=30, alpha=0.55, density=True,
                label=src.replace('_', ' '), color=PALETTE[src])
    ax.axvline(-7, color='black', linestyle='--', alpha=0.7,
               label='Good binding (−7 kcal/mol)')
    ax.set_xlabel('Binding Affinity (kcal/mol)', fontsize=12)
    ax.set_ylabel('Density', fontsize=12)
    ax.set_title('Binding Affinity Frequency Distributions', fontsize=13, fontweight='bold')
    ax.legend(fontsize=10)
    plt.tight_layout()
    fig.savefig(out_dir / 'fig2_histogram_overlay.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("  Saved: fig2_histogram_overlay.png")

    # ── Figure 3: Per-protease — GAN best vs MEROPS best ─────────────────────
    if 'MEROPS_Baseline' in df['source'].unique():
        gan_src = [s for s in present if 'GAN' in s]
        if gan_src:
            gan_best   = df[df['source'].isin(gan_src)].groupby('protease_name')['binding_affinity'].min()
            merops_best = df[df['source'] == 'MEROPS_Baseline'].groupby('protease_name')['binding_affinity'].min()
            shared = sorted(set(gan_best.index) & set(merops_best.index))

            if shared:
                x     = np.arange(len(shared))
                width = 0.35
                fig, ax = plt.subplots(figsize=(max(14, len(shared)), 6))
                ax.bar(x - width/2, [gan_best[p]    for p in shared], width,
                       label='Best GAN peptide', color='#e74c3c', alpha=0.85)
                ax.bar(x + width/2, [merops_best[p] for p in shared], width,
                       label='Best MEROPS substrate', color='#3498db', alpha=0.85)
                ax.axhline(-7, color='gray', linestyle='--', alpha=0.5,
                           label='Good binding threshold')
                ax.set_xticks(x)
                short = [p.split('(')[0].strip()[:14] for p in shared]
                ax.set_xticklabels(short, rotation=45, ha='right', fontsize=8)
                ax.set_ylabel('Best Binding Affinity (kcal/mol)', fontsize=11)
                ax.set_title('GAN-Generated vs MEROPS Natural Substrate — Best Binder per Protease',
                             fontsize=12, fontweight='bold')
                ax.legend(fontsize=10)
                plt.tight_layout()
                fig.savefig(out_dir / 'fig3_per_protease_comparison.png', dpi=150, bbox_inches='tight')
                plt.close()
                print("  Saved: fig3_per_protease_comparison.png")

    # ── Figure 4: % of sequences with "good" binding (<-7 kcal/mol) ──────────
    fig, ax = plt.subplots(figsize=(8, 5))
    pct_good = []
    for src in present:
        data = df[df['source'] == src]['binding_affinity']
        pct_good.append(100 * (data < -7).sum() / len(data))
    bars = ax.bar(labels, pct_good, color=colors, alpha=0.85, edgecolor='white')
    for bar, pct in zip(bars, pct_good):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                f'{pct:.1f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')
    ax.set_ylabel('% of peptides with affinity < −7 kcal/mol', fontsize=11)
    ax.set_title('Fraction of "Good Binders" by Source', fontsize=13, fontweight='bold')
    ax.set_ylim(0, max(pct_good) * 1.15 + 5)
    plt.tight_layout()
    fig.savefig(out_dir / 'fig4_good_binder_fraction.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("  Saved: fig4_good_binder_fraction.png")


# ════════════════════════════════════════════════════════════════════════════════
# Main
# ════════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description='GAN Pipeline Baseline Comparison',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument('--run', action='store_true',
                        help='Run ESMFold + docking on MEROPS and random baselines')
    parser.add_argument('--compare', action='store_true',
                        help='Generate comparison plots from existing results only')
    parser.add_argument('--n', type=int, default=5, metavar='N',
                        help='Sequences per protease for each baseline (default: 5)')
    args = parser.parse_args()

    if not args.run and not args.compare:
        parser.print_help()
        sys.exit(1)

    MEROPS_CSV   = PROJECT_ROOT / 'Preprocessing' / 'MEROPS_sepsis_expanded_dataset.csv'
    SEQ_DIR      = PROJECT_ROOT / 'generated_sequences'
    ANALYSIS_DIR = PROJECT_ROOT / 'baseline_comparison'

    # ── Phase 1 + 2: build and run baselines ─────────────────────────────────
    if args.run:
        print("\n" + "=" * 60)
        print("PHASE 1  Building baseline sequence files")
        print("=" * 60)

        merops_seq_csv = SEQ_DIR / 'merops_baseline_sequences.csv'
        random_seq_csv = SEQ_DIR / 'random_baseline_sequences.csv'

        if not merops_seq_csv.exists():
            print(f"\nExtracting MEROPS natural substrates (n={args.n} per protease)...")
            merops_df = extract_merops_substrates(MEROPS_CSV, n_per_protease=args.n)
            merops_df.to_csv(merops_seq_csv, index=False)
            print(f"  Saved → {merops_seq_csv.name}")
        else:
            print(f"  [skip] {merops_seq_csv.name} already exists")

        if not random_seq_csv.exists():
            print(f"\nGenerating random sequences (n={args.n} per protease)...")
            random_df = generate_random_sequences(n_per_protease=args.n)
            random_df.to_csv(random_seq_csv, index=False)
            print(f"  Saved → {random_seq_csv.name}")
        else:
            print(f"  [skip] {random_seq_csv.name} already exists")

        print("\n" + "=" * 60)
        print("PHASE 2  Running pipeline on baselines")
        print("=" * 60)

        print(f"\n[MEROPS baseline]")
        merops_dock = run_pipeline(merops_seq_csv, 'merops_baseline')

        print(f"\n[Random baseline]")
        random_dock = run_pipeline(random_seq_csv, 'random_baseline')

        if merops_dock is None and random_dock is None:
            sys.exit("\nERROR: Both pipelines failed. Check ESMFold/Vina installation.")

    # ── Phase 3: comparison ───────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("PHASE 3  Loading results and generating comparison")
    print("=" * 60)

    print("\nLoading docking result files...")
    df = load_all_results()
    print(f"Total successful dockings: {len(df)}")

    summary = print_statistics(df)

    print("\nGenerating figures...")
    generate_plots(df, ANALYSIS_DIR)

    # Save combined data + summary
    ANALYSIS_DIR.mkdir(exist_ok=True)
    df.to_csv(ANALYSIS_DIR / 'all_results_combined.csv', index=False)
    summary.to_csv(ANALYSIS_DIR / 'summary_statistics.csv', index=False)

    print(f"\nAll outputs saved to  {ANALYSIS_DIR}/")
    print("Done.")


if __name__ == '__main__':
    main()
