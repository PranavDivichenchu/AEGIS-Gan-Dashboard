import os
import requests
from pathlib import Path
import subprocess


PROTEASE_PDB_MAP = {
    "Neutrophil elastase (ELANE)": "1HNE",  # Human neutrophil elastase
    "Proteinase 3 (PRTN3)": "1FUJ",  # Proteinase 3
    "Cathepsin G (CTSG)": "1AU8",  # Cathepsin G
    "MMP8 (Collagenase-2)": "1MMB",  # MMP-8
    "MMP9 (Gelatinase B)": "1GKC",  # MMP-9
    "Thrombin (F2, coagulation factor IIa)": "1PPB",  # Thrombin
    "Plasmin": "4DUR",  # Plasmin
    "Caspase-1": "1ICE",  # Caspase-1
    "NSP1": "7K3N",  # SARS-CoV-2 NSP1 (placeholder - verify)
    "NSP2": "7MSX",  # SARS-CoV-2 NSP2 (placeholder - verify)
    "Granzyme B": "1FQ3",  # Granzyme B
    "Kallikrein 1": "2ANY",  # Kallikrein 1
    "Kallikrein 2": "2PSV",  # Kallikrein 2
    "MMP1 (Collagenase-1)": "1CGL",  # MMP-1
    "MMP2 (Gelatinase A)": "1QIB",  # MMP-2
    "MMP7 (Matrilysin)": "1MMP",  # MMP-7
    "MMP12 (Macrophage metalloelastase)": "1JK3",  # MMP-12
    "Factor VIIa": "1DAN",  # Factor VIIa
    "Factor IXa": "1RFN",  # Factor IXa
    "Factor Xa": "1FAX",  # Factor Xa
    "tPA": "1RTF",  # tPA
    "Urokinase": "1F5L",  # Urokinase
    "Caspase-3": "1CP3",  # Caspase-3
    "Caspase-6": "2WDP",  # Caspase-6
    "Caspase-7": "1F1J",  # Caspase-7
    "Caspase-8": "1QTN",  # Caspase-8
    "Caspase-9": "1JXQ",  # Caspase-9
}

OUTPUT_DIR = "protease_structures"
PDB_DOWNLOAD_URL = "https://files.rcsb.org/download/{pdb_id}.pdb"


class ProteaseStructureManager:
    def __init__(self, output_dir=OUTPUT_DIR):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Create subdirectories
        self.raw_dir = self.output_dir / "raw"
        self.prepared_dir = self.output_dir / "prepared"
        self.raw_dir.mkdir(exist_ok=True)
        self.prepared_dir.mkdir(exist_ok=True)

    def download_structure(self, pdb_id, protease_name):
        """Download PDB structure from RCSB"""
        output_file = self.raw_dir / f"{pdb_id}.pdb"

        if output_file.exists():
            print(f"  Structure {pdb_id} already downloaded")
            return str(output_file)

        url = PDB_DOWNLOAD_URL.format(pdb_id=pdb_id)
        print(f"  Downloading {pdb_id} from {url}...")

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            with open(output_file, 'w') as f:
                f.write(response.text)

            print(f"  Successfully downloaded {pdb_id}")
            return str(output_file)

        except Exception as e:
            print(f"  ERROR downloading {pdb_id}: {e}")
            return None

    def prepare_structure(self, pdb_file, pdb_id, protease_name):
        output_file = self.prepared_dir / f"{pdb_id}_prepared.pdb"

        if output_file.exists():
            print(f"  Structure {pdb_id} already prepared")
            return str(output_file)

        try:
            # Read PDB file
            with open(pdb_file, 'r') as f:
                lines = f.readlines()

            # Filter out water and unwanted heteroatoms
            prepared_lines = []
            for line in lines:
                # Keep ATOM records (protein atoms)
                if line.startswith('ATOM'):
                    prepared_lines.append(line)
                # Keep HETATM for important cofactors (ZN, CA, MG, etc.)
                elif line.startswith('HETATM'):
                    atom_name = line[17:20].strip()
                    # Keep important metal ions and cofactors
                    if atom_name in ['ZN', 'CA', 'MG', 'MN', 'FE', 'CU', 'NAG', 'NAD', 'FAD']:
                        prepared_lines.append(line)
                # Keep structure metadata
                elif line.startswith(('HEADER', 'TITLE', 'COMPND', 'SOURCE', 'REMARK', 'SEQRES')):
                    prepared_lines.append(line)
                # Keep END
                elif line.startswith('END'):
                    prepared_lines.append(line)

            # Write prepared structure
            with open(output_file, 'w') as f:
                f.writelines(prepared_lines)

            print(f"  Prepared structure saved to {output_file}")

            # Try to add hydrogens using reduce if available
            self.add_hydrogens(output_file)

            return str(output_file)

        except Exception as e:
            print(f"  ERROR preparing {pdb_id}: {e}")
            return None

    def add_hydrogens(self, pdb_file):
        """Add hydrogens using reduce if available"""
        try:
            # Check if reduce is installed
            result = subprocess.run(['which', 'reduce'], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"    (reduce not installed, skipping hydrogen addition)")
                return False

            output_file = str(pdb_file).replace('.pdb', '_H.pdb')
            cmd = ['reduce', '-build', str(pdb_file)]

            with open(output_file, 'w') as f:
                subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, check=True)

            print(f"    Added hydrogens: {output_file}")
            return True

        except Exception as e:
            print(f"    Could not add hydrogens: {e}")
            return False

    def download_all_structures(self):
        print("=" * 80)
        print("DOWNLOADING PROTEASE STRUCTURES FROM PDB")
        print("=" * 80)
        print(f"Output directory: {self.output_dir}")
        print(f"Total proteases: {len(PROTEASE_PDB_MAP)}")
        print("=" * 80)

        results = []

        for protease_name, pdb_id in PROTEASE_PDB_MAP.items():
            print(f"\n{protease_name} ({pdb_id}):")

            # Download
            pdb_file = self.download_structure(pdb_id, protease_name)
            if not pdb_file:
                results.append({
                    'protease_name': protease_name,
                    'pdb_id': pdb_id,
                    'status': 'download_failed',
                    'pdb_file': None,
                    'prepared_file': None
                })
                continue

            # Prepare
            prepared_file = self.prepare_structure(pdb_file, pdb_id, protease_name)
            if not prepared_file:
                results.append({
                    'protease_name': protease_name,
                    'pdb_id': pdb_id,
                    'status': 'preparation_failed',
                    'pdb_file': pdb_file,
                    'prepared_file': None
                })
                continue

            results.append({
                'protease_name': protease_name,
                'pdb_id': pdb_id,
                'status': 'success',
                'pdb_file': pdb_file,
                'prepared_file': prepared_file
            })

        import pandas as pd
        df = pd.DataFrame(results)
        summary_file = self.output_dir / "structure_summary.csv"
        df.to_csv(summary_file, index=False)

        print("\n" + "=" * 80)
        print("DOWNLOAD SUMMARY")
        print("=" * 80)
        print(f"Total: {len(results)}")
        print(f"Success: {len(df[df['status'] == 'success'])}")
        print(f"Failed: {len(df[df['status'] != 'success'])}")
        print(f"\nSummary saved to: {summary_file}")
        print("=" * 80)

        return df

    def create_binding_site_info(self):
        binding_sites = {
            "1HNE": {"chain": "A", "residues": [57, 102, 195, 214, 216, 226]},  # Elastase active site
            "1PPB": {"chain": "H", "residues": [57, 102, 195, 214, 216, 226]},  # Thrombin active site
            # Add more as needed
        }

        import json
        binding_site_file = self.output_dir / "binding_sites.json"
        with open(binding_site_file, 'w') as f:
            json.dump(binding_sites, f, indent=2)

        print(f"\nBinding site template created: {binding_site_file}")
        print("NOTE: Please verify and update binding site residues for accurate docking!")

        return binding_sites


def main():
    manager = ProteaseStructureManager()
    df = manager.download_all_structures()
    manager.create_binding_site_info()

    print("\n" + "=" * 80)
    print("NEXT STEPS:")
    print("=" * 80)
    print("1. Verify downloaded structures in:", manager.prepared_dir)
    print("2. Update binding_sites.json with accurate active site residues")
    print("3. Consider installing:")
    print("   - reduce (for adding hydrogens)")
    print("   - AutoDock Tools (for PDBQT conversion)")
    print("   - PyMOL or Chimera (for visualization)")
    print("=" * 80)


if __name__ == "__main__":
    main()
