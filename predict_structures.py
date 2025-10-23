"""
Predict 3D structures for generated peptide sequences using ESMFold
"""
import os
import requests
import time
from pathlib import Path
import pandas as pd
from typing import List, Dict
import json

# ESMFold API endpoint (Meta's public API)
ESMFOLD_API = "https://api.esmatlas.com/foldSequence/v1/pdb/"

OUTPUT_DIR = "predicted_structures"
DELAY_BETWEEN_REQUESTS = 2  # seconds to avoid rate limiting

# Amino acid conversion: 3-letter to 1-letter
AA_3TO1 = {
    'Ala': 'A', 'Arg': 'R', 'Asn': 'N', 'Asp': 'D', 'Cys': 'C',
    'Gln': 'Q', 'Glu': 'E', 'Gly': 'G', 'His': 'H', 'Ile': 'I',
    'Leu': 'L', 'Lys': 'K', 'Met': 'M', 'Phe': 'F', 'Pro': 'P',
    'Ser': 'S', 'Thr': 'T', 'Trp': 'W', 'Tyr': 'Y', 'Val': 'V'
}

def convert_3letter_to_1letter(sequence_3letter):
    """Convert 3-letter amino acid code sequence to 1-letter code"""
    import re
    # Extract all 3-letter codes
    aa_codes = re.findall(r'[A-Z][a-z]{2}', sequence_3letter)

    # Convert to 1-letter
    sequence_1letter = ''.join(AA_3TO1.get(aa, 'X') for aa in aa_codes)

    return sequence_1letter


class StructurePredictor:
    """Predict 3D structures using ESMFold API"""

    def __init__(self, output_dir=OUTPUT_DIR):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Create subdirectory for PDB files
        self.pdb_dir = self.output_dir / "pdb_files"
        self.pdb_dir.mkdir(exist_ok=True)

    def predict_structure_esmfold(self, sequence: str, sequence_id: str) -> Dict:
        """
        Predict structure using ESMFold API

        Args:
            sequence: Amino acid sequence
            sequence_id: Unique identifier for the sequence

        Returns:
            Dictionary with prediction results
        """
        output_file = self.pdb_dir / f"{sequence_id}.pdb"

        # Check if already predicted
        if output_file.exists():
            print(f"  Structure already predicted: {sequence_id}")
            return {
                'sequence_id': sequence_id,
                'sequence': sequence,
                'status': 'cached',
                'pdb_file': str(output_file),
                'error': None
            }

        try:
            # Convert 3-letter to 1-letter code if needed
            sequence_1letter = convert_3letter_to_1letter(sequence)
            print(f"  Converted to 1-letter: {sequence_1letter}")

            # Make API request
            response = requests.post(
                ESMFOLD_API,
                data=sequence_1letter,
                headers={'Content-Type': 'text/plain'},
                timeout=60
            )
            response.raise_for_status()

            # Save PDB file
            with open(output_file, 'w') as f:
                f.write(response.text)

            print(f"  Successfully predicted: {sequence_id}")

            return {
                'sequence_id': sequence_id,
                'sequence': sequence,
                'status': 'success',
                'pdb_file': str(output_file),
                'error': None
            }

        except requests.exceptions.Timeout:
            print(f"  TIMEOUT: {sequence_id}")
            return {
                'sequence_id': sequence_id,
                'sequence': sequence,
                'status': 'timeout',
                'pdb_file': None,
                'error': 'Request timeout'
            }

        except requests.exceptions.RequestException as e:
            print(f"  ERROR: {sequence_id} - {e}")
            return {
                'sequence_id': sequence_id,
                'sequence': sequence,
                'status': 'failed',
                'pdb_file': None,
                'error': str(e)
            }

    def predict_structure_local(self, sequence: str, sequence_id: str) -> Dict:
        """
        Predict structure using local ESMFold installation
        Requires: pip install fair-esm[esmfold]

        This is a fallback method if you have ESMFold installed locally
        """
        try:
            import torch
            from esm.esmfold.v1.pretrained import esmfold_v1

            output_file = self.pdb_dir / f"{sequence_id}.pdb"

            if output_file.exists():
                print(f"  Structure already predicted: {sequence_id}")
                return {
                    'sequence_id': sequence_id,
                    'sequence': sequence,
                    'status': 'cached',
                    'pdb_file': str(output_file),
                    'error': None
                }

            # Load model (will be cached after first load)
            if not hasattr(self, 'esmfold_model'):
                print("Loading ESMFold model (this may take a while)...")
                self.esmfold_model = esmfold_v1()
                self.esmfold_model.eval()
                if torch.cuda.is_available():
                    self.esmfold_model = self.esmfold_model.cuda()

            # Convert 3-letter to 1-letter code if needed
            sequence_1letter = convert_3letter_to_1letter(sequence)

            # Predict structure
            with torch.no_grad():
                output = self.esmfold_model.infer_pdb(sequence_1letter)

            # Save PDB
            with open(output_file, 'w') as f:
                f.write(output)

            print(f"  Successfully predicted (local): {sequence_id}")

            return {
                'sequence_id': sequence_id,
                'sequence': sequence,
                'status': 'success',
                'pdb_file': str(output_file),
                'error': None
            }

        except ImportError:
            return {
                'sequence_id': sequence_id,
                'sequence': sequence,
                'status': 'failed',
                'pdb_file': None,
                'error': 'ESMFold not installed locally'
            }
        except Exception as e:
            print(f"  ERROR (local): {sequence_id} - {e}")
            return {
                'sequence_id': sequence_id,
                'sequence': sequence,
                'status': 'failed',
                'pdb_file': None,
                'error': str(e)
            }

    def predict_from_csv(self, csv_file: str, use_local: bool = False, max_sequences: int = None):
        """
        Predict structures for sequences from CSV file

        Args:
            csv_file: Path to CSV file with sequences
            use_local: Use local ESMFold instead of API
            max_sequences: Maximum number of sequences to process (None = all)
        """
        print("=" * 80)
        print("STRUCTURE PREDICTION USING ESMFOLD")
        print("=" * 80)
        print(f"Input file: {csv_file}")
        print(f"Method: {'Local ESMFold' if use_local else 'ESMFold API'}")
        print("=" * 80)

        # Read sequences
        df = pd.read_csv(csv_file)

        if max_sequences:
            df = df.head(max_sequences)
            print(f"Processing first {max_sequences} sequences")

        print(f"Total sequences: {len(df)}")

        results = []
        success_count = 0
        failed_count = 0

        for idx, row in df.iterrows():
            sequence = row['sequence']
            protease_name = row['protease_name']
            merops_id = row['merops_id']

            # Create unique sequence ID
            sequence_id = f"{merops_id}_seq_{idx}"

            print(f"\n[{idx+1}/{len(df)}] {protease_name} - {sequence_id}")
            print(f"  Sequence: {sequence}")

            # Predict structure
            if use_local:
                result = self.predict_structure_local(sequence, sequence_id)
            else:
                result = self.predict_structure_esmfold(sequence, sequence_id)

            # Add metadata
            result['protease_name'] = protease_name
            result['merops_id'] = merops_id
            result['index'] = idx

            results.append(result)

            if result['status'] in ['success', 'cached']:
                success_count += 1
            else:
                failed_count += 1

            # Delay to avoid rate limiting (API only)
            if not use_local and result['status'] == 'success':
                time.sleep(DELAY_BETWEEN_REQUESTS)

        # Save results
        results_df = pd.DataFrame(results)
        results_file = self.output_dir / f"prediction_results_{Path(csv_file).stem}.csv"
        results_df.to_csv(results_file, index=False)

        print("\n" + "=" * 80)
        print("PREDICTION SUMMARY")
        print("=" * 80)
        print(f"Total sequences: {len(results)}")
        print(f"Successful: {success_count}")
        print(f"Failed: {failed_count}")
        print(f"Success rate: {success_count/len(results)*100:.1f}%")
        print(f"\nResults saved to: {results_file}")
        print(f"PDB files saved to: {self.pdb_dir}")
        print("=" * 80)

        return results_df

    def batch_predict_from_fasta(self, fasta_file: str, use_local: bool = False):
        """
        Predict structures from FASTA file

        Args:
            fasta_file: Path to FASTA file
            use_local: Use local ESMFold instead of API
        """
        print("=" * 80)
        print("STRUCTURE PREDICTION FROM FASTA")
        print("=" * 80)
        print(f"Input file: {fasta_file}")
        print("=" * 80)

        # Parse FASTA
        sequences = []
        with open(fasta_file, 'r') as f:
            current_id = None
            current_seq = []

            for line in f:
                line = line.strip()
                if line.startswith('>'):
                    if current_id:
                        sequences.append({
                            'id': current_id,
                            'sequence': ''.join(current_seq)
                        })
                    current_id = line[1:]  # Remove '>'
                    current_seq = []
                else:
                    current_seq.append(line)

            # Add last sequence
            if current_id:
                sequences.append({
                    'id': current_id,
                    'sequence': ''.join(current_seq)
                })

        print(f"Found {len(sequences)} sequences")

        results = []
        for idx, seq_data in enumerate(sequences):
            seq_id = seq_data['id'].replace('|', '_').replace(' ', '_')
            sequence = seq_data['sequence']

            print(f"\n[{idx+1}/{len(sequences)}] {seq_id}")
            print(f"  Sequence: {sequence}")

            if use_local:
                result = self.predict_structure_local(sequence, seq_id)
            else:
                result = self.predict_structure_esmfold(sequence, seq_id)

            results.append(result)

            if not use_local and result['status'] == 'success':
                time.sleep(DELAY_BETWEEN_REQUESTS)

        # Save results
        results_df = pd.DataFrame(results)
        results_file = self.output_dir / f"prediction_results_{Path(fasta_file).stem}.csv"
        results_df.to_csv(results_file, index=False)

        print(f"\nResults saved to: {results_file}")

        return results_df


def main():
    """Main execution"""
    import argparse

    parser = argparse.ArgumentParser(description='Predict structures using ESMFold')
    parser.add_argument('--input', type=str, required=True, help='Input CSV or FASTA file')
    parser.add_argument('--local', action='store_true', help='Use local ESMFold instead of API')
    parser.add_argument('--max', type=int, help='Maximum sequences to process')

    args = parser.parse_args()

    predictor = StructurePredictor()

    if args.input.endswith('.csv'):
        predictor.predict_from_csv(args.input, use_local=args.local, max_sequences=args.max)
    elif args.input.endswith('.fasta'):
        predictor.batch_predict_from_fasta(args.input, use_local=args.local)
    else:
        print("ERROR: Input must be .csv or .fasta file")


if __name__ == "__main__":
    # Example usage without command line args
    import sys

    if len(sys.argv) == 1:
        print("=" * 80)
        print("EXAMPLE USAGE:")
        print("=" * 80)
        print("From CSV:")
        print("  python predict_structures.py --input generated_sequences/supremegan_sequences.csv")
        print("\nFrom FASTA:")
        print("  python predict_structures.py --input generated_sequences/supremegan_sequences.fasta")
        print("\nUsing local ESMFold:")
        print("  python predict_structures.py --input file.csv --local")
        print("\nLimit sequences:")
        print("  python predict_structures.py --input file.csv --max 10")
        print("=" * 80)
    else:
        main()
