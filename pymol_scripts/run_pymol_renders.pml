# PyMOL Script for ORSEF Presentation Images
# ===========================================

# ============================================
# IMAGE 1: TITLE SLIDE - MMP1 Hero Image
# ============================================
reinitialize
bg_color white
set ray_trace_mode, 1
set ray_shadows, 1
set antialias, 2
set orthoscopic, 1

load /Users/pranavdivichenchu/Documents/AET Senior Research/protease_structures/prepared/1CGL_prepared.pdb, MMP1

hide everything
show surface, MMP1
color white, MMP1
color marine, MMP1 and resn ARG+LYS+HIS
color firebrick, MMP1 and resn ASP+GLU
color palegreen, MMP1 and resn ALA+VAL+LEU+ILE+MET+PHE+TRP+PRO
set surface_quality, 2
set transparency, 0.1

orient
turn y, 30
turn x, -20
zoom all, 1.2

ray 3000, 2000
png /Users/pranavdivichenchu/Documents/AET Senior Research/presentation_images/01_title_MMP1_hero.png

# ============================================
# IMAGE 2: TOP BINDER #1 - MMP1 Cartoon
# ============================================
reinitialize
bg_color white
set ray_trace_mode, 1
set antialias, 2

load /Users/pranavdivichenchu/Documents/AET Senior Research/protease_structures/prepared/1CGL_prepared.pdb, MMP1

hide everything
show cartoon, MMP1
color gold, MMP1
set cartoon_fancy_helices, 1

select active_site, MMP1 and resn HIS+GLU+ASP and name CA
show spheres, active_site
color firebrick, active_site
set sphere_scale, 0.5

show surface, MMP1
set transparency, 0.75

orient
zoom all, 1.2

ray 1500, 1500
png /Users/pranavdivichenchu/Documents/AET Senior Research/presentation_images/02_top1_MMP1_gold.png

# ============================================
# IMAGE 3: TOP BINDER #2 - Proteinase 3
# ============================================
reinitialize
bg_color white
set ray_trace_mode, 1
set antialias, 2

load /Users/pranavdivichenchu/Documents/AET Senior Research/protease_structures/prepared/1FUJ_prepared.pdb, PRTN3

hide everything
show cartoon, PRTN3
color silver, PRTN3
set cartoon_fancy_helices, 1

show surface, PRTN3
set transparency, 0.75

orient
zoom all, 1.2

ray 1500, 1500
png /Users/pranavdivichenchu/Documents/AET Senior Research/presentation_images/03_top2_Proteinase3_silver.png

# ============================================
# IMAGE 4: TOP BINDER #3 - Kallikrein-2
# ============================================
reinitialize
bg_color white
set ray_trace_mode, 1
set antialias, 2

load /Users/pranavdivichenchu/Documents/AET Senior Research/protease_structures/prepared/2PSV_prepared.pdb, KLK2

hide everything
show cartoon, KLK2
color orange, KLK2
set cartoon_fancy_helices, 1

select catalytic, KLK2 and resn HIS+ASP+SER and name CA
show spheres, catalytic
color magenta, catalytic
set sphere_scale, 0.5

show surface, KLK2
set transparency, 0.7

orient
zoom all, 1.2

ray 1500, 1500
png /Users/pranavdivichenchu/Documents/AET Senior Research/presentation_images/04_top3_Kallikrein2_orange.png

# ============================================
# IMAGE 5: KALLIKREIN-2 WET LAB TARGET
# ============================================
reinitialize
bg_color white
set ray_trace_mode, 1
set antialias, 2
set spec_reflect, 0.5

load /Users/pranavdivichenchu/Documents/AET Senior Research/protease_structures/prepared/2PSV_prepared.pdb, KLK2

hide everything
show cartoon, KLK2
color palegreen, KLK2
set cartoon_transparency, 0.2

show surface, KLK2
set transparency, 0.7
set surface_color, palegreen, KLK2

orient
turn y, 45
zoom all, 1.1

ray 2400, 1800
png /Users/pranavdivichenchu/Documents/AET Senior Research/presentation_images/05_wetlab_Kallikrein2_detailed.png

# ============================================
# IMAGE 6: CASPASE-1
# ============================================
reinitialize
bg_color white
set ray_trace_mode, 1
set antialias, 2

load /Users/pranavdivichenchu/Documents/AET Senior Research/protease_structures/prepared/1ICE_prepared.pdb, CASP1

hide everything
show cartoon, CASP1
color salmon, CASP1
set cartoon_fancy_helices, 1

show surface, CASP1
set transparency, 0.7

orient
zoom all, 1.3

ray 1200, 1200
png /Users/pranavdivichenchu/Documents/AET Senior Research/presentation_images/06_class_Caspase1.png

# ============================================
# IMAGE 7: THROMBIN
# ============================================
reinitialize
bg_color white
set ray_trace_mode, 1
set antialias, 2

load /Users/pranavdivichenchu/Documents/AET Senior Research/protease_structures/prepared/1PPB_prepared.pdb, Thrombin

hide everything
show cartoon, Thrombin
color purple, Thrombin
set cartoon_fancy_helices, 1

show surface, Thrombin
set transparency, 0.7

orient
zoom all, 1.3

ray 1200, 1200
png /Users/pranavdivichenchu/Documents/AET Senior Research/presentation_images/07_class_Thrombin.png

# ============================================
# IMAGE 8: MMP9
# ============================================
reinitialize
bg_color white
set ray_trace_mode, 1
set antialias, 2

load /Users/pranavdivichenchu/Documents/AET Senior Research/protease_structures/prepared/1GKC_prepared.pdb, MMP9

hide everything
show cartoon, MMP9
color marine, MMP9
set cartoon_fancy_helices, 1

select zinc, MMP9 and resn ZN
show spheres, zinc
color gray50, zinc
set sphere_scale, 1.0

show surface, MMP9
set transparency, 0.7

orient
zoom all, 1.3

ray 1200, 1200
png /Users/pranavdivichenchu/Documents/AET Senior Research/presentation_images/08_class_MMP9.png

# ============================================
# IMAGE 9: NEUTROPHIL ELASTASE
# ============================================
reinitialize
bg_color white
set ray_trace_mode, 1
set antialias, 2

load /Users/pranavdivichenchu/Documents/AET Senior Research/protease_structures/prepared/1HNE_prepared.pdb, NE

hide everything
show cartoon, NE
color forest, NE
set cartoon_fancy_helices, 1

show surface, NE
set transparency, 0.7

orient
zoom all, 1.3

ray 1200, 1200
png /Users/pranavdivichenchu/Documents/AET Senior Research/presentation_images/09_class_NeutrophilElastase.png

# ============================================
# IMAGE 10: MMP1 BINDING POCKET CLOSEUP
# ============================================
reinitialize
bg_color white
set ray_trace_mode, 1
set antialias, 2
set spec_reflect, 0.3

load /Users/pranavdivichenchu/Documents/AET Senior Research/protease_structures/prepared/1CGL_prepared.pdb, MMP1

hide everything
show cartoon, MMP1
color gray80, MMP1

select cat_his, MMP1 and resn HIS
show sticks, cat_his
color marine, cat_his

select zinc, MMP1 and resn ZN
show spheres, zinc
color gray50, zinc
set sphere_scale, 0.8

select pocket, MMP1 within 12 of zinc
show surface, pocket
set transparency, 0.6
color palecyan, pocket

center zinc
zoom pocket, 2

ray 2000, 1500
png /Users/pranavdivichenchu/Documents/AET Senior Research/presentation_images/10_MMP1_binding_pocket.png

# ============================================
# IMAGE 11: MULTI-STRUCTURE PANEL
# ============================================
reinitialize
bg_color white
set ray_trace_mode, 1
set antialias, 2

load /Users/pranavdivichenchu/Documents/AET Senior Research/protease_structures/prepared/1CGL_prepared.pdb, MMP1
load /Users/pranavdivichenchu/Documents/AET Senior Research/protease_structures/prepared/1ICE_prepared.pdb, Caspase1
load /Users/pranavdivichenchu/Documents/AET Senior Research/protease_structures/prepared/1PPB_prepared.pdb, Thrombin

hide everything

show cartoon, MMP1
show cartoon, Caspase1
show cartoon, Thrombin

color gold, MMP1
color salmon, Caspase1
color purple, Thrombin

translate [-30, 0, 0], MMP1
translate [0, 0, 0], Caspase1
translate [30, 0, 0], Thrombin

orient
zoom all, 0.8

ray 3000, 1200
png /Users/pranavdivichenchu/Documents/AET Senior Research/presentation_images/11_multi_protease_panel.png

quit
