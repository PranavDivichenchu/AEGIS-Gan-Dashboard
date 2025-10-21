"""
Molecular docking pipeline using AutoDock Vina
"""
import os
import subprocess
from pathlib import Path
import pandas as pd
import json
from typing import Dict, List, Tuple
import tempfile


class MolecularDocking:
    """
    Perform molecular docking using AutoDock Vina
    Requires: AutoDock Vina and AutoDock Tools installed
    """

    def __init__(self, protease_dir="protease_structures", ligand_dir="predicted_structures/pdb_files", output_dir="docking_results"):
        self.protease_dir = Path(protease_dir)
        self.ligand_dir = Path(ligand_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Create subdirectories
        self.pdbqt_dir = self.output_dir / "pdbqt_files"
        self.results_dir = self.output_dir / "vina_results"
        self.pdbqt_dir.mkdir(exist_ok=True)
        self.results_dir.mkdir(exist_ok=True)

        self.check_dependencies()

    def check_dependencies(self):
        """Check if required tools are installed"""
        print("Checking dependencies...")

        # Check for Vina
        try:
            result = subprocess.run(['vina', '--version'], capture_output=True, text=True)
            print(f"  ✓ AutoDock Vina found: {result.stdout.strip()}")
        except FileNotFoundError:
            print("  ✗ AutoDock Vina not found")
            print("    Install: conda install -c conda-forge vina")

        # Check for prepare_receptor/prepare_ligand (AutoDock Tools)
        try:
            result = subprocess.run(['which', 'prepare_receptor4.py'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"  ✓ AutoDock Tools found")
            else:
                print("  ✗ AutoDock Tools not found")
                print("    Install: conda install -c bioconda mgltools")
        except Exception:
            print("  ✗ AutoDock Tools not found")

    def pdb_to_pdbqt(self, pdb_file: str, output_file: str, is_receptor: bool = False) -> bool:
        """
        Convert PDB to PDBQT format using AutoDock Tools

        Args:
            pdb_file: Input PDB file
            output_file: Output PDBQT file
            is_receptor: True if this is a receptor (protease), False for ligand (peptide)
        """
        try:
            if is_receptor:
                # Prepare receptor
                cmd = [
                    'prepare_receptor4.py',
                    '-r', pdb_file,
                    '-o', output_file,
                    '-A', 'hydrogens',  # Add hydrogens
                    '-U', 'nphs_lps_waters'  # Remove non-polar hydrogens, lone pairs, waters
                ]
            else:
                # Prepare ligand
                cmd = [
                    'prepare_ligand4.py',
                    '-l', pdb_file,
                    '-o', output_file,
                    '-A', 'hydrogens'
                ]

            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return True

        except subprocess.CalledProcessError as e:
            print(f"    Error converting {pdb_file}: {e.stderr}")
            return False
        except FileNotFoundError:
            # Fallback: Use OpenBabel if AutoDock Tools not available
            print("    AutoDock Tools not found, trying OpenBabel...")
            return self.pdb_to_pdbqt_obabel(pdb_file, output_file)

    def pdb_to_pdbqt_obabel(self, pdb_file: str, output_file: str) -> bool:
        """
        Fallback: Convert PDB to PDBQT using OpenBabel

        Args:
            pdb_file: Input PDB file
            output_file: Output PDBQT file
        """
        try:
            cmd = [
                'obabel',
                pdb_file,
                '-O', output_file,
                '-h'  # Add hydrogens
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return True

        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"    Error with OpenBabel: {e}")
            return False

    def calculate_binding_box(self, receptor_pdb: str, ligand_pdb: str = None) -> Dict:
        """
        Calculate binding box dimensions and center

        Args:
            receptor_pdb: Receptor PDB file
            ligand_pdb: Optional ligand PDB for centering (uses receptor center if None)

        Returns:
            Dictionary with center_x, center_y, center_z, size_x, size_y, size_z
        """
        try:
            # Read receptor coordinates
            coords = []
            with open(receptor_pdb, 'r') as f:
                for line in f:
                    if line.startswith('ATOM') or line.startswith('HETATM'):
                        x = float(line[30:38].strip())
                        y = float(line[38:46].strip())
                        z = float(line[46:54].strip())
                        coords.append([x, y, z])

            if not coords:
                raise ValueError(f"No atoms found in {receptor_pdb}")

            import numpy as np
            coords = np.array(coords)

            # Calculate center and size
            center = coords.mean(axis=0)
            mins = coords.min(axis=0)
            maxs = coords.max(axis=0)
            size = maxs - mins

            # Add padding (10 Angstroms on each side)
            padding = 10.0
            size = size + 2 * padding

            return {
                'center_x': float(center[0]),
                'center_y': float(center[1]),
                'center_z': float(center[2]),
                'size_x': float(size[0]),
                'size_y': float(size[1]),
                'size_z': float(size[2])
            }

        except Exception as e:
            print(f"    Error calculating binding box: {e}")
            # Return default box
            return {
                'center_x': 0.0,
                'center_y': 0.0,
                'center_z': 0.0,
                'size_x': 25.0,
                'size_y': 25.0,
                'size_z': 25.0
            }

    def run_vina(self, receptor_pdbqt: str, ligand_pdbqt: str, output_pdbqt: str, box: Dict, exhaustiveness: int = 8) -> Tuple[bool, float]:
        """
        Run AutoDock Vina docking

        Args:
            receptor_pdbqt: Receptor PDBQT file
            ligand_pdbqt: Ligand PDBQT file
            output_pdbqt: Output PDBQT file for docked poses
            box: Binding box parameters
            exhaustiveness: Exhaustiveness parameter (higher = more thorough)

        Returns:
            (success, binding_affinity)
        """
        try:
            # Create config file
            config_file = output_pdbqt.replace('.pdbqt', '_config.txt')
            with open(config_file, 'w') as f:
                f.write(f"receptor = {receptor_pdbqt}\n")
                f.write(f"ligand = {ligand_pdbqt}\n")
                f.write(f"out = {output_pdbqt}\n")
                f.write(f"center_x = {box['center_x']}\n")
                f.write(f"center_y = {box['center_y']}\n")
                f.write(f"center_z = {box['center_z']}\n")
                f.write(f"size_x = {box['size_x']}\n")
                f.write(f"size_y = {box['size_y']}\n")
                f.write(f"size_z = {box['size_z']}\n")
                f.write(f"exhaustiveness = {exhaustiveness}\n")

            # Run Vina
            cmd = ['vina', '--config', config_file]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            # Parse binding affinity from output
            binding_affinity = None
            for line in result.stdout.split('\n'):
                if 'REMARK VINA RESULT:' in line:
                    parts = line.split()
                    if len(parts) >= 4:
                        binding_affinity = float(parts[3])
                        break

            if binding_affinity is None:
                # Try to read from output file
                with open(output_pdbqt, 'r') as f:
                    for line in f:
                        if 'REMARK VINA RESULT:' in line:
                            parts = line.split()
                            if len(parts) >= 4:
                                binding_affinity = float(parts[3])
                                break

            print(f"    Binding affinity: {binding_affinity} kcal/mol")
            return True, binding_affinity if binding_affinity else 0.0

        except subprocess.CalledProcessError as e:
            print(f"    Vina error: {e.stderr}")
            return False, 0.0
        except Exception as e:
            print(f"    Error running Vina: {e}")
            return False, 0.0

    def dock_peptide_to_protease(self, peptide_pdb: str, protease_pdb: str, protease_name: str, peptide_id: str) -> Dict:
        """
        Dock a single peptide to a protease

        Args:
            peptide_pdb: Peptide PDB file
            protease_pdb: Protease PDB file
            protease_name: Name of protease
            peptide_id: ID of peptide

        Returns:
            Dictionary with docking results
        """
        print(f"\n  Docking {peptide_id} to {protease_name}...")

        # Convert to PDBQT
        receptor_pdbqt = self.pdbqt_dir / f"{Path(protease_pdb).stem}_receptor.pdbqt"
        ligand_pdbqt = self.pdbqt_dir / f"{peptide_id}_ligand.pdbqt"

        # Convert receptor (if not already done)
        if not receptor_pdbqt.exists():
            print(f"    Converting receptor to PDBQT...")
            if not self.pdb_to_pdbqt(protease_pdb, str(receptor_pdbqt), is_receptor=True):
                return self._create_error_result(peptide_id, protease_name, "Receptor conversion failed")

        # Convert ligand
        print(f"    Converting ligand to PDBQT...")
        if not self.pdb_to_pdbqt(peptide_pdb, str(ligand_pdbqt), is_receptor=False):
            return self._create_error_result(peptide_id, protease_name, "Ligand conversion failed")

        # Calculate binding box
        print(f"    Calculating binding box...")
        box = self.calculate_binding_box(protease_pdb)

        # Run docking
        print(f"    Running AutoDock Vina...")
        output_pdbqt = self.results_dir / f"{peptide_id}_{Path(protease_pdb).stem}_docked.pdbqt"

        success, affinity = self.run_vina(
            str(receptor_pdbqt),
            str(ligand_pdbqt),
            str(output_pdbqt),
            box
        )

        if success:
            return {
                'peptide_id': peptide_id,
                'protease_name': protease_name,
                'binding_affinity': affinity,
                'receptor_pdbqt': str(receptor_pdbqt),
                'ligand_pdbqt': str(ligand_pdbqt),
                'output_pdbqt': str(output_pdbqt),
                'box': box,
                'status': 'success',
                'error': None
            }
        else:
            return self._create_error_result(peptide_id, protease_name, "Docking failed")

    def _create_error_result(self, peptide_id: str, protease_name: str, error: str) -> Dict:
        """Create error result dictionary"""
        return {
            'peptide_id': peptide_id,
            'protease_name': protease_name,
            'binding_affinity': None,
            'receptor_pdbqt': None,
            'ligand_pdbqt': None,
            'output_pdbqt': None,
            'box': None,
            'status': 'failed',
            'error': error
        }

    def batch_dock(self, prediction_results_csv: str, protease_structures_csv: str, max_dockings: int = None):
        """
        Perform batch docking

        Args:
            prediction_results_csv: CSV with predicted peptide structures
            protease_structures_csv: CSV with protease structures
            max_dockings: Maximum number of dockings to perform
        """
        print("=" * 80)
        print("BATCH MOLECULAR DOCKING")
        print("=" * 80)

        # Load data
        peptides_df = pd.read_csv(prediction_results_csv)
        peptides_df = peptides_df[peptides_df['status'] == 'success']  # Only successful predictions

        proteases_df = pd.read_csv(protease_structures_csv)
        proteases_df = proteases_df[proteases_df['status'] == 'success']  # Only successful downloads

        print(f"Peptides: {len(peptides_df)}")
        print(f"Proteases: {len(proteases_df)}")

        # Match peptides to proteases
        results = []
        docking_count = 0

        for _, peptide_row in peptides_df.iterrows():
            peptide_id = peptide_row['sequence_id']
            merops_id = peptide_row['merops_id']
            peptide_pdb = peptide_row['pdb_file']
            protease_name = peptide_row['protease_name']

            # Find matching protease structure
            protease_match = proteases_df[proteases_df['protease_name'] == protease_name]

            if len(protease_match) == 0:
                print(f"\nNo protease structure found for {protease_name}, skipping...")
                continue

            protease_pdb = protease_match.iloc[0]['prepared_file']

            # Dock
            result = self.dock_peptide_to_protease(peptide_pdb, protease_pdb, protease_name, peptide_id)
            result['peptide_sequence'] = peptide_row['sequence']
            result['merops_id'] = merops_id

            results.append(result)

            docking_count += 1
            if max_dockings and docking_count >= max_dockings:
                print(f"\nReached maximum dockings ({max_dockings}), stopping...")
                break

        # Save results
        results_df = pd.DataFrame(results)
        results_file = self.output_dir / "docking_results.csv"
        results_df.to_csv(results_file, index=False)

        # Summary
        successful = len(results_df[results_df['status'] == 'success'])
        failed = len(results_df[results_df['status'] == 'failed'])

        print("\n" + "=" * 80)
        print("DOCKING SUMMARY")
        print("=" * 80)
        print(f"Total dockings: {len(results)}")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        print(f"\nResults saved to: {results_file}")
        print("=" * 80)

        return results_df


def main():
    """Main execution"""
    import argparse

    parser = argparse.ArgumentParser(description='Molecular docking with AutoDock Vina')
    parser.add_argument('--peptides', type=str, required=True, help='CSV with predicted peptide structures')
    parser.add_argument('--proteases', type=str, required=True, help='CSV with protease structures')
    parser.add_argument('--max', type=int, help='Maximum dockings to perform')
    parser.add_argument('--output', type=str, default='docking_results', help='Output directory')

    args = parser.parse_args()

    docker = MolecularDocking(output_dir=args.output)
    docker.batch_dock(args.peptides, args.proteases, max_dockings=args.max)


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1:
        print("=" * 80)
        print("EXAMPLE USAGE:")
        print("=" * 80)
        print("python molecular_docking.py \\")
        print("  --peptides predicted_structures/prediction_results_supremegan_sequences.csv \\")
        print("  --proteases protease_structures/structure_summary.csv")
        print("\nLimit dockings:")
        print("python molecular_docking.py --peptides file.csv --proteases proteases.csv --max 10")
        print("=" * 80)
    else:
        main()
