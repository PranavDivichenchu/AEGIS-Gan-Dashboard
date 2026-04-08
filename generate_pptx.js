const pptxgen = require('pptxgenjs');
const path = require('path');

async function createPoster() {
    let pptx = new pptxgen();
    pptx.defineLayout({ name: 'POSTER', width: 48, height: 36 });
    pptx.layout = 'POSTER';

    // ==========================================
    // SLIDE 1: POSTER
    // ==========================================
    let slide = pptx.addSlide();

    // Better color scheme: Clean White background with Medical Teal and Navy Blue accents
    slide.background = { color: "ffffff" };

    // Header Banner
    slide.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: 48, h: 4.5, fill: { color: "0b192c" } });

    // Header text
    slide.addText(
        "First Multi-Architecture GAN Pipeline for Computational Design and Chemical Optimization of Sepsis Protease Inhibitors", {
        x: 1, y: 0.5, w: 46, h: 2,
        align: 'center', fontSize: 44, bold: true, color: '14b8a6', fontFace: 'Helvetica'
    });

    slide.addText("Pranav Divichenchu", {
        x: 1, y: 2.2, w: 46, h: 1,
        align: 'center', fontSize: 32, bold: true, color: 'ffffff', fontFace: 'Helvetica'
    });

    slide.addText("Academy of Engineering and Technology, Loudoun County Public Schools", {
        x: 1, y: 3.0, w: 46, h: 1,
        align: 'center', fontSize: 24, color: 'e2e8f0', fontFace: 'Helvetica'
    });

    // Layout configuration
    const colWidth = 14.5;
    const col1X = 1.5;
    const col2X = 16.75;
    const col3X = 32.0;

    const boxBg = { color: "f8fafc" };
    const titleBg = { color: '8b2f3d' }; // Using the original dark maroon/crimson for section headers as per original poster request, or a better color? User asked for "Make the color scheme better", so let's use a nice Navy Blue "0b192c" or Teal "14b8a6" for section headers. I'll use Deep Navy "0b192c" for main headers, and Teal "14b8a6" for accents.
    const titleColor = 'ffffff';
    const accentFill = { color: 'e0f2fe' }; // Light medical blue instead of sage green

    // ==========================================
    // COLUMN 1: PURPOSE
    // ==========================================
    slide.addShape(pptx.ShapeType.rect, { x: col1X, y: 5.0, w: colWidth, h: 1.2, fill: { color: "0b192c" } });
    slide.addText("PURPOSE", { x: col1X, y: 5.0, w: colWidth, h: 1.2, align: 'center', bold: true, fontSize: 32, color: titleColor, fontFace: 'Helvetica' });

    let p1Y = 6.4;
    slide.addText([
        { text: "Sepsis has a staggering mortality rate of 40–60%, resulting in over 11 million lives lost annually. In the US alone, sepsis accounts for $62 billion in annual healthcare expenditures.\n\n", options: { fontSize: 18, color: '0f172a', fontFace: 'Helvetica' } },
        { text: "This systemic crisis is driven by the simultaneous collapse of 4 proteolytic axes: caspase apoptosis, MMP tissue destruction, serine cascade amplification, and cysteine cytotoxicity.\n\n", options: { fontSize: 18, color: '0f172a', fontFace: 'Helvetica' } },
        { text: "Traditional high-throughput screening is highly inefficient, testing 10,000–100,000 compounds over 3–5 years at a cost of $10–50 million per target. With 27 simultaneous protease targets implicated in sepsis, a unified drug-discovery pipeline is necessary.", options: { fontSize: 18, color: '0f172a', fontFace: 'Helvetica' } }
    ], { x: col1X, y: p1Y, w: colWidth, h: 6.5, valign: 'top', fill: boxBg });

    p1Y += 7.0;
    // Current Solutions box (Accent 1)
    slide.addShape(pptx.ShapeType.rect, { x: col1X, y: p1Y, w: colWidth, h: 3, fill: accentFill });
    slide.addText("Current solutions for Sepsis Drug Discovery are vastly inadequate:\nHigh Cost and Low Throughput", { x: col1X + 0.5, y: p1Y + 0.2, w: colWidth - 1, h: 1.2, align: 'center', bold: true, fontSize: 20, color: '0f172a', fontFace: 'Helvetica' });
    slide.addText("Traditional in-vitro synthesis cannot rapidly generate or evaluate the millions of potential sequence geometries needed to discover highly specific inhibitors for rapidly evolving systemic conditions.", { x: col1X + 0.5, y: p1Y + 1.2, w: colWidth - 1, h: 1.5, align: 'left', fontSize: 16, color: '0f172a', fontFace: 'Helvetica' });

    p1Y += 3.5;
    // Research Question (Accent 2)
    slide.addShape(pptx.ShapeType.rect, { x: col1X, y: p1Y, w: colWidth, h: 3, fill: accentFill });
    slide.addText("Research Question", { x: col1X + 0.5, y: p1Y + 0.2, w: colWidth - 1, h: 0.8, align: 'center', bold: true, fontSize: 22, color: '0f172a', fontFace: 'Helvetica' });
    slide.addText("How can a multi-architecture Generative Adversarial Network pipeline (PrismGAN, CGAN, WGAN-GP) trained on 11,551 MEROPS cleavage events accelerate the design of novel, provably equivalent peptide inhibitors across all 27 target sepsis-related proteases?", { x: col1X + 0.5, y: p1Y + 1.0, w: colWidth - 1, h: 1.8, align: 'center', fontSize: 17, italic: true, color: '0f172a', fontFace: 'Helvetica' });

    p1Y += 3.5;
    // Framework (Accent 3)
    slide.addShape(pptx.ShapeType.rect, { x: col1X, y: p1Y, w: colWidth, h: 10, fill: accentFill });
    slide.addText("AI-Driven Sepsis Protease Inhibitor Framework", { x: col1X + 0.5, y: p1Y + 0.2, w: colWidth - 1, h: 0.8, align: 'center', bold: true, fontSize: 22, color: '0f172a', fontFace: 'Helvetica' });
    try {
        slide.addImage({ path: path.join(__dirname, 'rsef_figures/fig0_pipeline.png'), x: col1X + 0.5, y: p1Y + 1.2, w: colWidth - 1, h: 7, sizing: { type: 'contain', w: colWidth - 1, h: 7 } });
        slide.addText("Diagram created by Finalist using Lucidchart/BioRender.", { x: col1X + 0.5, y: p1Y + 8.3, w: colWidth - 1, h: 0.5, fontSize: 12, italic: true, color: '475569', align: 'center' });
    } catch (e) { }

    // Add SDG graphic placeholder
    /*
    try {
        slide.addImage({ path: path.join(__dirname, 'presentation_images/UN_SDG3.png'), x: col1X, y: 14.5, w: 4, h: 4, sizing: { type: 'contain' } }); // Mock position
    } catch(e) {}
    */

    // ==========================================
    // COLUMN 2: DATASETS / METHODOLOGY / ARCHITECTURE
    // ==========================================
    slide.addShape(pptx.ShapeType.rect, { x: col2X, y: 5.0, w: colWidth, h: 1.2, fill: { color: "0b192c" } });
    slide.addText("DATASETS & BASELINE PREPROCESSING", { x: col2X, y: 5.0, w: colWidth, h: 1.2, align: 'center', bold: true, fontSize: 32, color: titleColor, fontFace: 'Helvetica' });

    // Split box for Datasets and Baseline
    let p2Y = 6.4;
    slide.addShape(pptx.ShapeType.rect, { x: col2X, y: p2Y, w: colWidth / 2 - 0.2, h: 6, fill: boxBg });
    slide.addText("Data Sources", { x: col2X + 0.2, y: p2Y + 0.2, w: colWidth / 2 - 0.6, h: 0.8, bold: true, fontSize: 20, align: 'center', fontFace: 'Helvetica' });
    slide.addText("The predictive architecture was constructed using the MEROPS database. 11,551 confirmed cleavage events were extracted across 27 targets. PDB structures for the 27 target proteases were sourced from the RCSB PDB database and grids defined at 0.375 Å.", { x: col2X + 0.2, y: p2Y + 1.2, w: colWidth / 2 - 0.6, h: 4.5, fontSize: 16, fontFace: 'Helvetica', align: 'left', valign: 'top' });

    slide.addShape(pptx.ShapeType.rect, { x: col2X + colWidth / 2 + 0.2, y: p2Y, w: colWidth / 2 - 0.2, h: 6, fill: boxBg });
    slide.addText("Methodology & Preprocessing", { x: col2X + colWidth / 2 + 0.4, y: p2Y + 0.2, w: colWidth / 2 - 0.6, h: 0.8, bold: true, fontSize: 20, align: 'center', fontFace: 'Helvetica' });
    slide.addText("P4–P4′ 8-mer windows extracted. Generated sequences were folded natively using Meta AI’s ESMFold API, requiring an average of 10-15 seconds per structure before molecular docking simulations in AutoDock Vina.", { x: col2X + colWidth / 2 + 0.4, y: p2Y + 1.2, w: colWidth / 2 - 0.6, h: 4.5, fontSize: 16, fontFace: 'Helvetica', align: 'left', valign: 'top' });

    p2Y += 6.5;
    slide.addShape(pptx.ShapeType.rect, { x: col2X, y: p2Y, w: colWidth, h: 1.2, fill: { color: "0b192c" } });
    slide.addText("MODEL DEVELOPMENT & ARCHITECTURE", { x: col2X, y: p2Y, w: colWidth, h: 1.2, align: 'center', bold: true, fontSize: 32, color: titleColor, fontFace: 'Helvetica' });

    p2Y += 1.4;
    slide.addShape(pptx.ShapeType.rect, { x: col2X, y: p2Y, w: colWidth, h: 6, fill: boxBg });
    slide.addText([
        { text: "PrismGAN Architecture: ", options: { bold: true, fontSize: 18, color: '14b8a6' } },
        { text: "Novel structure incorporating Spectral Normalization, Multi-Head Self-Attention (4 heads, d_model = 256) to capture long-range dependencies, and Conditional Batch Normalization for protease-specific generation.\n", options: { fontSize: 18, color: '0f172a' } },
        { text: "Ensemble Pipeline: ", options: { bold: true, fontSize: 18, color: '14b8a6' } },
        { text: "Integrated Conditional GANs (protease-conditioned generation) and WGAN-GPs alongside PrismGAN to ensure robust sequence diversification across 1,000 epochs.", options: { fontSize: 18, color: '0f172a' } }
    ], { x: col2X + 0.5, y: p2Y + 0.2, w: colWidth - 1, h: 5.5, valign: 'top', fontFace: 'Helvetica' });

    p2Y += 6.5;
    slide.addShape(pptx.ShapeType.rect, { x: col2X, y: p2Y, w: colWidth, h: 1.2, fill: { color: "0b192c" } });
    slide.addText("MODEL PERFORMANCE & VALIDATION", { x: col2X, y: p2Y, w: colWidth, h: 1.2, align: 'center', bold: true, fontSize: 32, color: titleColor, fontFace: 'Helvetica' });

    p2Y += 1.4;
    slide.addShape(pptx.ShapeType.rect, { x: col2X, y: p2Y, w: colWidth, h: 11, fill: boxBg });
    slide.addText([
        { text: "Extensive computational screening executed 781 docking simulations. The 27-peptide final panel yielded affinities from −4.93 to −11.88 kcal/mol, yielding 28 'excellent binders'.\n\n", options: { fontSize: 17, color: '0f172a' } },
        { text: "TOST Equivalence Validation: ", options: { bold: true, fontSize: 17 } },
        { text: "Two One-Sided Tests (TOST) against the FDA-standard margin (±0.75 kcal/mol) proved the GAN distributions are formally equivalent to MEROPS biology (Combined GAN vs. MEROPS: +0.19 kcal/mol mean diff; p_lower < 0.001, p_upper = 0.011).", options: { fontSize: 17, color: '0f172a' } }
    ], { x: col2X + 0.5, y: p2Y + 0.2, w: colWidth - 1, h: 5, valign: 'top', fontFace: 'Helvetica' });

    try {
        slide.addImage({ path: path.join(__dirname, 'rsef_figures/fig1_baseline_comparison.png'), x: col2X + 0.5, y: p2Y + 5.5, w: (colWidth - 1) / 2 - 0.2, h: 4.5, sizing: { type: 'contain' } });
        slide.addText("Graph created by Finalist using Python/Matplotlib/Seaborn.", { x: col2X + 0.5, y: p2Y + 10.1, w: (colWidth - 1) / 2 - 0.2, h: 0.5, fontSize: 10, italic: true, color: '475569', align: 'center' });

        slide.addImage({ path: path.join(__dirname, 'rsef_figures/fig2_all27_vs_merops.png'), x: col2X + (colWidth - 1) / 2 + 0.7, y: p2Y + 5.5, w: (colWidth - 1) / 2 - 0.2, h: 4.5, sizing: { type: 'contain' } });
        slide.addText("Graph created by Finalist using Python/Matplotlib/Seaborn.", { x: col2X + (colWidth - 1) / 2 + 0.7, y: p2Y + 10.1, w: (colWidth - 1) / 2 - 0.2, h: 0.5, fontSize: 10, italic: true, color: '475569', align: 'center' });
    } catch (e) { }

    // ==========================================
    // COLUMN 3: DISCUSSION / CONCLUSION
    // ==========================================
    slide.addShape(pptx.ShapeType.rect, { x: col3X, y: 5.0, w: colWidth, h: 1.2, fill: { color: "0b192c" } });
    slide.addText("DISCUSSION", { x: col3X, y: 5.0, w: colWidth, h: 1.2, align: 'center', bold: true, fontSize: 32, color: titleColor, fontFace: 'Helvetica' });

    let p3Y = 6.4;
    slide.addShape(pptx.ShapeType.rect, { x: col3X, y: p3Y, w: colWidth, h: 11, fill: boxBg });
    slide.addText([
        { text: "Performance Analysis: ", options: { bold: true, fontSize: 18, color: '14b8a6' } },
        { text: "In direct comparisons across 7 proteases, our AI generative models outperformed the absolute best natural biological MEROPS substrate directly in 5 out of 7 targets (71%) with binding improvements averaging up to +1.30 kcal/mol.\n\n", options: { fontSize: 18, color: '0f172a' } },
        { text: "Druglikeness & ADMET Profiling: ", options: { bold: true, fontSize: 18, color: '14b8a6' } },
        { text: "Comprehensive ADMET analysis proved that 67% of generated peptides possess highly favorable druglikeness scores (≥60/100 scale), maintaining ideal molecular weights (689-1167 Da), hydrophobicity balance, and net charge considerations.\n\n", options: { fontSize: 18, color: '0f172a' } },
        { text: "Inhibitor Modifications: ", options: { bold: true, fontSize: 18, color: '14b8a6' } },
        { text: "The 27 panel candidates were computationally extended into 3 distinct covalent warhead variants—yielding 81 total inhibitor designs tailored per class (Aldehyde for Serine, Boronic Acid for stability, Hydroxamate for MMPs).", options: { fontSize: 18, color: '0f172a' } }
    ], { x: col3X + 0.5, y: p3Y + 0.2, w: colWidth - 1, h: 10, valign: 'top', fontFace: 'Helvetica' });

    p3Y += 11.5;
    slide.addShape(pptx.ShapeType.rect, { x: col3X, y: p3Y, w: colWidth, h: 1.2, fill: { color: "0b192c" } });
    slide.addText("FUTURE DEVELOPMENT", { x: col3X, y: p3Y, w: colWidth, h: 1.2, align: 'center', bold: true, fontSize: 32, color: titleColor, fontFace: 'Helvetica' });

    p3Y += 1.4;
    slide.addShape(pptx.ShapeType.rect, { x: col3X, y: p3Y, w: colWidth, h: 4.5, fill: accentFill });
    slide.addText([
        { text: "• Wet-Lab Validation: ", options: { bold: true, fontSize: 18, color: '0369a1' } },
        { text: "Execution of a $949 Proof-of-Concept synthesis targeting Panel #13 (Kallikrein 2, sequence: EGSCYGTE, -9.72 kcal/mol) using competitive fluorescence-based inhibition assays.\n", options: { fontSize: 18, color: '0f172a' } },
        { text: "• Molecular Dynamics Simulations: ", options: { bold: true, fontSize: 18, color: '0369a1' } },
        { text: "Integrate GROMACS MD to validate physical binding pocket stability over temporal 100ns durations.", options: { fontSize: 18, color: '0f172a' } }
    ], { x: col3X + 0.5, y: p3Y + 0.2, w: colWidth - 1, h: 4, valign: 'top', fontFace: 'Helvetica' });

    p3Y += 5;
    slide.addShape(pptx.ShapeType.rect, { x: col3X, y: p3Y, w: colWidth, h: 1.2, fill: { color: "0b192c" } });
    slide.addText("CONCLUSION", { x: col3X, y: p3Y, w: colWidth, h: 1.2, align: 'center', bold: true, fontSize: 32, color: titleColor, fontFace: 'Helvetica' });

    p3Y += 1.4;
    slide.addShape(pptx.ShapeType.rect, { x: col3X, y: p3Y, w: colWidth, h: 7, fill: boxBg });
    slide.addText([
        { text: "This pipeline is the first study to successfully execute a highly coordinated 3-stage computational generative sequence on all 27 distinct, critical human sepsis proteases simultaneously. Utilizing PrismGAN we screened nearly 800 geometric combinations—producing a diverse, stable 27-peptide panel optimized for future clinical synthesis.", options: { fontSize: 18, color: '0f172a', bold: true } }
    ], { x: col3X + 0.5, y: p3Y + 0.2, w: colWidth - 1, h: 2.5, valign: 'top', fontFace: 'Helvetica' });

    try {
        slide.addImage({ path: path.join(__dirname, 'presentation_images/11_multi_protease_panel.png'), x: col3X + 0.5, y: p3Y + 2.8, w: colWidth - 1, h: 3.5, sizing: { type: 'contain' } });
        slide.addText("Image created by Finalist using PyMOL.", { x: col3X + 0.5, y: p3Y + 6.3, w: colWidth - 1, h: 0.5, fontSize: 10, italic: true, color: '475569', align: 'center' });
    } catch (e) { }


    // ==========================================
    // SLIDE 2: REFERENCES
    // ==========================================
    let slide2 = pptx.addSlide();
    slide2.background = { color: "ffffff" };
    slide2.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: 48, h: 4.5, fill: { color: "0b192c" } });
    slide2.addText("REFERENCES", { x: 1, y: 0.5, w: 46, h: 3.5, align: 'center', fontSize: 50, bold: true, color: '14b8a6', fontFace: 'Helvetica' });

    slide2.addText([
        { text: "1. Goodfellow, I., Pouget-Abadie, J., Mirza, M., et al. (2014). Generative adversarial nets. Advances in Neural Information Processing Systems, 27.\n", options: { fontSize: 20 } },
        { text: "2. Rawlings, N.D., Barrett, A.J., Thomas, P.D., et al. (2018). The MEROPS database of proteolytic enzymes, their substrates and inhibitors in 2017. Nucleic Acids Research, 46(D1), D624–D632.\n", options: { fontSize: 20 } },
        { text: "3. Trott, O., & Olson, A.J. (2010). AutoDock Vina: Improving the speed and accuracy of docking with a new scoring function. Journal of Computational Chemistry, 31(2), 455–461.\n", options: { fontSize: 20 } },
        { text: "4. Lin, Z., Akin, H., Rao, R., et al. (2023). Evolutionary-scale prediction of atomic-level protein structure with a language model. Science, 379(6637), 1123–1130.\n", options: { fontSize: 20 } },
        { text: "5. Schechter, I., & Berger, A. (1967). On the size of the active site in proteases. I. Papain. Biochemical and Biophysical Research Communications, 27(2), 157–162.\n", options: { fontSize: 20 } },
        { text: "6. Miyato, T., Kataoka, T., Koyama, M., & Yoshida, Y. (2018). Spectral normalization for generative adversarial networks. ICLR 2018.\n", options: { fontSize: 20 } },
        { text: "7. Singer, M., Deutschman, C.S., Seymour, C.W., et al. (2016). The Third International Consensus Definitions for Sepsis and Septic Shock (Sepsis-3). JAMA, 315(8), 801–810.", options: { fontSize: 20 } }
    ], { x: 2, y: 6, w: 44, h: 25, valign: 'top', color: '0f172a', fontFace: 'Helvetica', align: 'left' });

    let fileOut = path.join(__dirname, 'RSEF_Sepsis_Poster.pptx');
    await pptx.writeFile({ fileName: fileOut });
    console.log("Successfully created Canva-ready pptx:", fileOut);
}

createPoster().catch(console.error);
