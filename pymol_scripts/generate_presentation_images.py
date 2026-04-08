"""
PyMOL Visualization Scripts for ORSEF Presentation
===================================================
Generates publication-quality images of protease structures and docking complexes.

Usage:
    1. Open PyMOL
    2. Run: run /path/to/generate_presentation_images.py
    3. Or execute individual functions

Author: Generated for ORSEF Presentation
"""

from pymol import cmd, util
import os

# Output directory for images
OUTPUT_DIR = "/Users/pranavdivichenchu/Documents/AET Senior Research/presentation_images"
STRUCTURE_DIR = "/Users/pranavdivichenchu/Documents/AET Senior Research/protease_structures/prepared"
DOCKING_DIR = "/Users/pranavdivichenchu/Documents/AET Senior Research/docking_results/vina_results"

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def setup_publication_quality():
    """Configure PyMOL for publication-quality rendering"""
    cmd.set("ray_trace_mode", 1)
    cmd.set("ray_shadows", 1)
    cmd.set("ray_trace_fog", 0)
    cmd.set("antialias", 2)
    cmd.set("ambient", 0.4)
    cmd.set("spec_reflect", 0.5)
    cmd.set("spec_power", 200)
    cmd.set("depth_cue", 0)
    cmd.set("ray_opaque_background", 1)
    cmd.bg_color("white")
    cmd.set("orthoscopic", 1)

def render_and_save(filename, width=2400, height=1800):
    """Render and save high-resolution image"""
    filepath = os.path.join(OUTPUT_DIR, filename)
    cmd.ray(width, height)
    cmd.png(filepath, dpi=300)
    print(f"Saved: {filepath}")

# =============================================================================
# SLIDE 1: TITLE SLIDE - Hero Protein Image
# =============================================================================

def generate_title_slide_image():
    """
    Generate a dramatic hero image for the title slide
    Features MMP1 (best binder) with surface representation
    """
    cmd.delete("all")
    setup_publication_quality()

    # Load MMP1 structure (best binder: -11.88 kcal/mol)
    cmd.load(f"{STRUCTURE_DIR}/1CGL_prepared.pdb", "MMP1")

    # Create dramatic surface representation
    cmd.hide("everything")
    cmd.show("surface", "MMP1")

    # Color by electrostatic potential (approximation using residue type)
    cmd.color("white", "MMP1")
    cmd.color("marine", "MMP1 and resn ARG+LYS+HIS")  # Positive (blue)
    cmd.color("firebrick", "MMP1 and resn ASP+GLU")    # Negative (red)
    cmd.color("palegreen", "MMP1 and resn ALA+VAL+LEU+ILE+MET+PHE+TRP+PRO")  # Hydrophobic

    # Set surface transparency for depth
    cmd.set("surface_quality", 2)
    cmd.set("transparency", 0.1)

    # Optimal viewing angle
    cmd.orient()
    cmd.turn("y", 30)
    cmd.turn("x", -20)
    cmd.zoom("all", 1.2)

    render_and_save("01_title_slide_MMP1_hero.png", 3000, 2000)
    print("Generated: Title slide hero image (MMP1)")

# =============================================================================
# SLIDE 4: GAN ARCHITECTURE - Protein Variety
# =============================================================================

def generate_protease_classes_panel():
    """
    Generate a 2x2 panel showing different protease classes
    - Caspase (C14)
    - MMP (M10)
    - Serine Protease (S01)
    - Coagulation Factor
    """
    # Generate individual images for each class
    structures = [
        ("1ICE_prepared.pdb", "Caspase1", "Caspase-1", "salmon"),
        ("1CGL_prepared.pdb", "MMP1", "MMP-1", "marine"),
        ("1FUJ_prepared.pdb", "Proteinase3", "Proteinase 3", "forest"),
        ("1PPB_prepared.pdb", "Thrombin", "Thrombin", "purple"),
    ]

    for pdb_file, obj_name, label, color in structures:
        cmd.delete("all")
        setup_publication_quality()

        cmd.load(f"{STRUCTURE_DIR}/{pdb_file}", obj_name)

        # Cartoon representation with surface overlay
        cmd.hide("everything")
        cmd.show("cartoon", obj_name)
        cmd.color(color, obj_name)

        # Color secondary structure
        cmd.set("cartoon_fancy_helices", 1)
        cmd.set("cartoon_highlight_color", "white")

        # Add transparent surface
        cmd.show("surface", obj_name)
        cmd.set("transparency", 0.7, obj_name)
        cmd.set("surface_color", color, obj_name)

        cmd.orient()
        cmd.zoom("all", 1.3)

        render_and_save(f"02_protease_class_{obj_name}.png", 1200, 1200)

    print("Generated: 4 protease class images for panel")

# =============================================================================
# SLIDE 7: TOP 3 BINDERS
# =============================================================================

def generate_top_binders():
    """
    Generate images for the top 3 binding peptides
    1. MMP1: -11.88 kcal/mol (1CGL)
    2. Proteinase 3: -11.137 kcal/mol (1FUJ)
    3. Kallikrein 2: -9.717 kcal/mol (2PSV) - Validation target
    """
    top_binders = [
        {
            "name": "MMP1",
            "pdb": "1CGL_prepared.pdb",
            "affinity": "-11.88",
            "rank": "1",
            "color": "gold"
        },
        {
            "name": "Proteinase3",
            "pdb": "1FUJ_prepared.pdb",
            "affinity": "-11.14",
            "rank": "2",
            "color": "silver"
        },
        {
            "name": "Kallikrein2",
            "pdb": "2PSV_prepared.pdb",
            "affinity": "-9.72",
            "rank": "3",
            "color": "orange"
        },
    ]

    for binder in top_binders:
        cmd.delete("all")
        setup_publication_quality()

        cmd.load(f"{STRUCTURE_DIR}/{binder['pdb']}", binder['name'])

        # Sophisticated visualization
        cmd.hide("everything")

        # Show cartoon for backbone
        cmd.show("cartoon", binder['name'])
        cmd.color(binder['color'], binder['name'])

        # Highlight active site residues (catalytic residues)
        cmd.select("active_site", f"{binder['name']} and (resn HIS+GLU+ASP+SER+CYS) and name CA")
        cmd.show("spheres", "active_site")
        cmd.color("firebrick", "active_site")
        cmd.set("sphere_scale", 0.4, "active_site")

        # Add surface for binding pocket
        cmd.show("surface", binder['name'])
        cmd.set("transparency", 0.75, binder['name'])

        cmd.orient()
        cmd.zoom("all", 1.2)

        render_and_save(f"03_top_binder_{binder['rank']}_{binder['name']}.png", 1500, 1500)

    print("Generated: Top 3 binder images")

# =============================================================================
# SLIDE 10/11: WET LAB - Kallikrein 2 with Docked Peptide
# =============================================================================

def generate_docking_complex():
    """
    Generate visualization of Kallikrein-2 with docked EGSCYGTE peptide
    This is the validation target for wet lab experiments
    """
    cmd.delete("all")
    setup_publication_quality()

    # Load receptor
    cmd.load(f"{STRUCTURE_DIR}/2PSV_prepared.pdb", "Kallikrein2")

    # Try to load docked peptide if available
    docked_file = f"{DOCKING_DIR}/S01.071_seq_141_2PSV_prepared_docked.pdbqt"
    if os.path.exists(docked_file):
        cmd.load(docked_file, "peptide")

    # Receptor visualization
    cmd.hide("everything")
    cmd.show("cartoon", "Kallikrein2")
    cmd.color("palegreen", "Kallikrein2")
    cmd.set("cartoon_transparency", 0.3, "Kallikrein2")

    # Show receptor surface
    cmd.show("surface", "Kallikrein2")
    cmd.set("transparency", 0.8, "Kallikrein2")
    cmd.set("surface_color", "palegreen", "Kallikrein2")

    # Peptide visualization (if loaded)
    if "peptide" in cmd.get_names():
        cmd.show("sticks", "peptide")
        cmd.color("magenta", "peptide")
        cmd.set("stick_radius", 0.25, "peptide")

        # Show peptide surface
        cmd.show("surface", "peptide")
        cmd.set("transparency", 0.5, "peptide")
        cmd.set("surface_color", "magenta", "peptide")

    # Highlight binding interface
    cmd.select("interface", "Kallikrein2 within 5 of peptide")
    cmd.color("marine", "interface")

    cmd.orient()
    cmd.turn("y", 45)
    cmd.zoom("all", 1.1)

    render_and_save("04_docking_complex_Kallikrein2_EGSCYGTE.png", 2400, 1800)
    print("Generated: Kallikrein-2 docking complex (validation target)")

# =============================================================================
# SLIDE 5: PIPELINE - Structure Prediction Visualization
# =============================================================================

def generate_sequence_to_structure():
    """
    Generate before/after visualization showing sequence to 3D structure
    """
    cmd.delete("all")
    setup_publication_quality()

    # Load the peptide structure
    peptide_file = "/Users/pranavdivichenchu/Documents/AET Senior Research/predicted_structures/pdb_files/S01.071_seq_141.pdb"

    # Check if exists, if not use alternative
    if not os.path.exists(peptide_file):
        # Use any available predicted structure
        peptide_file = "/Users/pranavdivichenchu/Documents/AET Senior Research/predicted_structures/pdb_files/S01.131_seq_0.pdb"

    if os.path.exists(peptide_file):
        cmd.load(peptide_file, "GAN_peptide")

        cmd.hide("everything")

        # Show as sticks with cartoon backbone
        cmd.show("cartoon", "GAN_peptide")
        cmd.show("sticks", "GAN_peptide")
        cmd.color("cyan", "GAN_peptide")

        # Color by atom type
        util.cbag("GAN_peptide")  # Color by atom (green carbons)
        cmd.color("cyan", "GAN_peptide and name C*")

        # Show surface
        cmd.show("surface", "GAN_peptide")
        cmd.set("transparency", 0.6, "GAN_peptide")

        cmd.orient()
        cmd.zoom("all", 1.5)

        render_and_save("05_GAN_generated_peptide_structure.png", 1500, 1500)
        print("Generated: GAN peptide 3D structure")
    else:
        print("Warning: No predicted peptide structure found")

# =============================================================================
# SLIDE: BINDING POCKET CLOSEUP
# =============================================================================

def generate_binding_pocket_closeup():
    """
    Generate closeup of MMP1 binding pocket with key residues labeled
    """
    cmd.delete("all")
    setup_publication_quality()

    cmd.load(f"{STRUCTURE_DIR}/1CGL_prepared.pdb", "MMP1")

    cmd.hide("everything")

    # Show cartoon backbone
    cmd.show("cartoon", "MMP1")
    cmd.color("gray80", "MMP1")

    # Identify and show catalytic zinc and coordinating residues (for MMPs)
    # MMP1 has a catalytic zinc coordinated by 3 histidines
    cmd.select("catalytic", "MMP1 and resn HIS and (resi 218+222+228)")  # Approximate residues
    cmd.show("sticks", "catalytic")
    cmd.color("marine", "catalytic")

    # Show zinc if present
    cmd.select("zinc", "MMP1 and resn ZN")
    cmd.show("spheres", "zinc")
    cmd.color("gray50", "zinc")
    cmd.set("sphere_scale", 0.8, "zinc")

    # Show binding pocket surface
    cmd.select("pocket", "MMP1 within 12 of zinc")
    cmd.show("surface", "pocket")
    cmd.set("transparency", 0.7, "pocket")
    cmd.color("palecyan", "pocket")

    # Focus on binding pocket
    cmd.center("zinc")
    cmd.zoom("pocket", 2)

    render_and_save("06_MMP1_binding_pocket_closeup.png", 2000, 1500)
    print("Generated: MMP1 binding pocket closeup")

# =============================================================================
# COMPREHENSIVE PANEL - All 27 Proteases (Thumbnail Grid)
# =============================================================================

def generate_protease_grid():
    """
    Generate a grid showing all 27 target proteases
    Creates individual thumbnails that can be combined into a grid
    """
    proteases = [
        ("1ICE", "Caspase-1"), ("1CP3", "Caspase-3"), ("2WDP", "Caspase-6"),
        ("1F1J", "Caspase-7"), ("1QTN", "Caspase-8"), ("1JXQ", "Caspase-9"),
        ("1AU8", "Cathepsin_G"), ("1RFN", "Factor_IXa"), ("1DAN", "Factor_VIIa"),
        ("1FAX", "Factor_Xa"), ("1FQ3", "Granzyme_B"), ("2ANY", "Kallikrein1"),
        ("2PSV", "Kallikrein2"), ("1CGL", "MMP1"), ("1JK3", "MMP12"),
        ("1QIB", "MMP2"), ("1MMP", "MMP7"), ("1MMB", "MMP8"),
        ("1GKC", "MMP9"), ("7K3N", "NSP1"), ("7MSX", "NSP2"),
        ("1HNE", "Neutrophil_Elastase"), ("4DUR", "Plasmin"), ("1FUJ", "Proteinase3"),
        ("1PPB", "Thrombin"), ("1F5L", "Urokinase"), ("1RTF", "tPA"),
    ]

    # Color scheme by protease class
    colors = {
        "Caspase": "salmon",
        "MMP": "marine",
        "Factor": "purple",
        "Kallikrein": "orange",
        "Default": "teal"
    }

    for pdb_id, name in proteases:
        cmd.delete("all")
        setup_publication_quality()

        pdb_file = f"{STRUCTURE_DIR}/{pdb_id}_prepared.pdb"
        if os.path.exists(pdb_file):
            cmd.load(pdb_file, name)

            cmd.hide("everything")
            cmd.show("cartoon", name)

            # Determine color by class
            color = colors["Default"]
            for class_name, class_color in colors.items():
                if class_name in name:
                    color = class_color
                    break
            if "MMP" in name:
                color = colors["MMP"]
            elif "Caspase" in name:
                color = colors["Caspase"]
            elif "Factor" in name:
                color = colors["Factor"]
            elif "Kallikrein" in name:
                color = colors["Kallikrein"]

            cmd.color(color, name)
            cmd.orient()
            cmd.zoom("all", 1.5)

            render_and_save(f"grid_{pdb_id}_{name}.png", 600, 600)

    print("Generated: 27 protease thumbnails for grid")

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def generate_all_images():
    """Generate all presentation images"""
    print("=" * 60)
    print("Generating ORSEF Presentation Images")
    print("=" * 60)

    generate_title_slide_image()
    generate_protease_classes_panel()
    generate_top_binders()
    generate_docking_complex()
    generate_sequence_to_structure()
    generate_binding_pocket_closeup()

    print("=" * 60)
    print(f"All images saved to: {OUTPUT_DIR}")
    print("=" * 60)

# Quick commands for interactive use
print("""
PyMOL Presentation Image Generator Loaded!
==========================================

Quick Commands:
  generate_all_images()          - Generate all presentation images
  generate_title_slide_image()   - Title slide hero image
  generate_protease_classes_panel() - 4 protease class examples
  generate_top_binders()         - Top 3 binding candidates
  generate_docking_complex()     - Kallikrein-2 + peptide (wet lab target)
  generate_binding_pocket_closeup() - MMP1 active site detail
  generate_protease_grid()       - All 27 protease thumbnails

Output directory: {OUTPUT_DIR}
""".format(OUTPUT_DIR=OUTPUT_DIR))
