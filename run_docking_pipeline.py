"""
Main orchestration script for the complete molecular docking pipeline
Integrates: GAN sequence generation -> Structure prediction -> Docking -> Analysis
"""
import argparse
import sys
from pathlib import Path
import time

# Import pipeline modules
from generate_sequences import SequenceGenerator
from prepare_protease_structures import ProteaseStructureManager
from predict_structures import StructurePredictor
from molecular_docking import MolecularDocking
from analyze_docking_results import DockingAnalyzer


class DockingPipeline:
    """Orchestrate the complete molecular docking pipeline"""

    def __init__(self, gan_model="supreme", sequences_per_protease=100, max_predictions=None, max_dockings=None):
        self.gan_model = gan_model
        self.sequences_per_protease = sequences_per_protease
        self.max_predictions = max_predictions
        self.max_dockings = max_dockings

        self.timing = {}

    def step1_generate_sequences(self):
        """Step 1: Generate sequences from GAN models"""
        print("\n" + "=" * 80)
        print("STEP 1: GENERATING SEQUENCES FROM GAN")
        print("=" * 80)

        start_time = time.time()

        generator = SequenceGenerator()
        df = generator.generate_all_sequences(model_name=self.gan_model)

        self.sequences_file = f"generated_sequences/{self.gan_model.lower()}gan_sequences.csv"

        elapsed = time.time() - start_time
        self.timing['sequence_generation'] = elapsed

        print(f"\n✓ Step 1 complete in {elapsed:.2f}s")
        print(f"  Generated {len(df)} sequences")
        print(f"  Output: {self.sequences_file}")

        return self.sequences_file

    def step2_prepare_proteases(self):
        """Step 2: Download and prepare protease structures"""
        print("\n" + "=" * 80)
        print("STEP 2: PREPARING PROTEASE STRUCTURES")
        print("=" * 80)

        start_time = time.time()

        manager = ProteaseStructureManager()
        df = manager.download_all_structures()
        manager.create_binding_site_info()

        self.proteases_file = "protease_structures/structure_summary.csv"

        elapsed = time.time() - start_time
        self.timing['protease_preparation'] = elapsed

        print(f"\n✓ Step 2 complete in {elapsed:.2f}s")
        print(f"  Prepared {len(df[df['status'] == 'success'])} protease structures")
        print(f"  Output: {self.proteases_file}")

        return self.proteases_file

    def step3_predict_structures(self, sequences_file):
        """Step 3: Predict 3D structures for peptides"""
        print("\n" + "=" * 80)
        print("STEP 3: PREDICTING PEPTIDE 3D STRUCTURES")
        print("=" * 80)

        start_time = time.time()

        predictor = StructurePredictor()
        df = predictor.predict_from_csv(
            sequences_file,
            use_local=False,
            max_sequences=self.max_predictions
        )

        self.predictions_file = f"predicted_structures/prediction_results_{Path(sequences_file).stem}.csv"

        elapsed = time.time() - start_time
        self.timing['structure_prediction'] = elapsed

        print(f"\n✓ Step 3 complete in {elapsed:.2f}s")
        print(f"  Predicted {len(df[df['status'] == 'success'])} structures")
        print(f"  Output: {self.predictions_file}")

        return self.predictions_file

    def step4_run_docking(self, predictions_file, proteases_file):
        """Step 4: Perform molecular docking"""
        print("\n" + "=" * 80)
        print("STEP 4: RUNNING MOLECULAR DOCKING")
        print("=" * 80)

        start_time = time.time()

        docker = MolecularDocking()
        df = docker.batch_dock(
            predictions_file,
            proteases_file,
            max_dockings=self.max_dockings
        )

        self.docking_results_file = "docking_results/docking_results.csv"

        elapsed = time.time() - start_time
        self.timing['docking'] = elapsed

        print(f"\n✓ Step 4 complete in {elapsed:.2f}s")
        print(f"  Completed {len(df[df['status'] == 'success'])} dockings")
        print(f"  Output: {self.docking_results_file}")

        return self.docking_results_file

    def step5_analyze_results(self, docking_results_file):
        """Step 5: Analyze and visualize results"""
        print("\n" + "=" * 80)
        print("STEP 5: ANALYZING DOCKING RESULTS")
        print("=" * 80)

        start_time = time.time()

        analyzer = DockingAnalyzer(docking_results_file)
        analyzer.run_full_analysis()

        elapsed = time.time() - start_time
        self.timing['analysis'] = elapsed

        print(f"\n✓ Step 5 complete in {elapsed:.2f}s")

    def run_complete_pipeline(self, skip_steps=None):
        """
        Run the complete pipeline

        Args:
            skip_steps: List of steps to skip (e.g., [1, 2] to skip sequence generation and protease prep)
        """
        if skip_steps is None:
            skip_steps = []

        print("=" * 80)
        print("MOLECULAR DOCKING PIPELINE")
        print("=" * 80)
        print(f"GAN Model: {self.gan_model}")
        print(f"Sequences per protease: {self.sequences_per_protease}")
        if self.max_predictions:
            print(f"Max predictions: {self.max_predictions}")
        if self.max_dockings:
            print(f"Max dockings: {self.max_dockings}")
        print("=" * 80)

        pipeline_start = time.time()

        try:
            # Step 1: Generate sequences
            if 1 not in skip_steps:
                sequences_file = self.step1_generate_sequences()
            else:
                sequences_file = f"generated_sequences/{self.gan_model.lower()}gan_sequences.csv"
                print(f"\nSkipping Step 1, using existing: {sequences_file}")

            # Step 2: Prepare proteases
            if 2 not in skip_steps:
                proteases_file = self.step2_prepare_proteases()
            else:
                proteases_file = "protease_structures/structure_summary.csv"
                print(f"\nSkipping Step 2, using existing: {proteases_file}")

            # Step 3: Predict structures
            if 3 not in skip_steps:
                predictions_file = self.step3_predict_structures(sequences_file)
            else:
                predictions_file = f"predicted_structures/prediction_results_{Path(sequences_file).stem}.csv"
                print(f"\nSkipping Step 3, using existing: {predictions_file}")

            # Step 4: Run docking
            if 4 not in skip_steps:
                docking_results_file = self.step4_run_docking(predictions_file, proteases_file)
            else:
                docking_results_file = "docking_results/docking_results.csv"
                print(f"\nSkipping Step 4, using existing: {docking_results_file}")

            # Step 5: Analyze results
            if 5 not in skip_steps:
                self.step5_analyze_results(docking_results_file)
            else:
                print(f"\nSkipping Step 5")

            # Final summary
            total_time = time.time() - pipeline_start

            print("\n" + "=" * 80)
            print("PIPELINE COMPLETE!")
            print("=" * 80)
            print("\nTiming Summary:")
            for step, elapsed in self.timing.items():
                print(f"  {step:25s}: {elapsed:8.2f}s ({elapsed/60:6.2f}m)")
            print(f"  {'Total':25s}: {total_time:8.2f}s ({total_time/60:6.2f}m)")
            print("=" * 80)

            print("\nOutput Files:")
            print(f"  1. Sequences: {sequences_file}")
            print(f"  2. Proteases: {proteases_file}")
            print(f"  3. Predictions: {predictions_file}")
            print(f"  4. Docking Results: {docking_results_file}")
            print(f"  5. Analysis: docking_analysis/")
            print("=" * 80)

        except Exception as e:
            print(f"\n{'='*80}")
            print("PIPELINE ERROR!")
            print("=" * 80)
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Complete molecular docking pipeline for GAN-generated peptides',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run complete pipeline with SupremeGAN
  python run_docking_pipeline.py --model supreme

  # Run with ConditionalGAN and limit to 10 sequences
  python run_docking_pipeline.py --model conditional --max-predictions 10

  # Skip sequence generation and protease preparation (use existing)
  python run_docking_pipeline.py --skip 1 2

  # Run only docking and analysis (assuming previous steps done)
  python run_docking_pipeline.py --skip 1 2 3

  # Test run with minimal data
  python run_docking_pipeline.py --sequences 50 --max-predictions 10 --max-dockings 5
        """
    )

    parser.add_argument('--model', type=str, default='supreme',
                        choices=['supreme', 'conditional', 'wgan'],
                        help='GAN model to use for sequence generation')

    parser.add_argument('--sequences', type=int, default=100,
                        help='Number of sequences to generate per protease')

    parser.add_argument('--max-predictions', type=int, default=None,
                        help='Maximum number of structure predictions (None = all)')

    parser.add_argument('--max-dockings', type=int, default=None,
                        help='Maximum number of dockings to perform (None = all)')

    parser.add_argument('--skip', nargs='+', type=int, default=[],
                        help='Steps to skip (1=gen, 2=prep, 3=predict, 4=dock, 5=analyze)')

    args = parser.parse_args()

    # Create and run pipeline
    pipeline = DockingPipeline(
        gan_model=args.model,
        sequences_per_protease=args.sequences,
        max_predictions=args.max_predictions,
        max_dockings=args.max_dockings
    )

    pipeline.run_complete_pipeline(skip_steps=args.skip)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("=" * 80)
        print("MOLECULAR DOCKING PIPELINE")
        print("=" * 80)
        print("\nThis pipeline performs:")
        print("  1. Generate peptide sequences from trained GANs")
        print("  2. Download and prepare protease structures from PDB")
        print("  3. Predict 3D structures for peptides using ESMFold")
        print("  4. Perform molecular docking with AutoDock Vina")
        print("  5. Analyze and visualize binding affinities")
        print("\nUsage:")
        print("  python run_docking_pipeline.py --model supreme")
        print("\nFor more options:")
        print("  python run_docking_pipeline.py --help")
        print("=" * 80)
    else:
        main()
