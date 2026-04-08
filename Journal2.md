---
geometry: margin=0.5in, letterpaper
header-includes:
  - \usepackage{booktabs}
  - \usepackage{longtable}
  - \usepackage{array}
  - \usepackage{graphicx}
  - \usepackage{float}
  - \usepackage{setspace}
  - \usepackage{fancyhdr}
  - \pagestyle{empty}
output: pdf_document
---

# \hfill Journal #23
## \hfill Pranav Divichenchu
\vspace{-0.5em}
\hfill March 15, 2026

\vspace{1em}
\hrule
\vspace{0.5em}

**Research Topic:** Design a Generative Adverserial Network (GAN) to design novel protein sequences that are able to predict and enhance model cleavage.

## Daily Log (2/21/26-3/15/26)

**Week of 2/21/26 - 2/28/26:**
Successfully completed RSEF poster presentation and competition. The presentation went well, with judges particularly interested in the three-stage GAN architecture and the experimental validation plan. Received positive feedback on the clarity of the biological motivation and the novelty of using ensemble GAN methods for protease substrate design. Post-competition, began planning the development of an interactive web platform to showcase the research and make the GAN models accessible for demonstration purposes.

**Week of 3/1/26 - 3/8/26:**
Started development of AegisGAN Dashboard, a full-stack web application to serve as the final research product. Built the backend API using FastAPI with endpoints for sequence generation, protease listing, and health monitoring. Integrated the three trained GAN models (SupremeGAN, Conditional GAN, and WGAN-GP) with the backend to enable real-time peptide generation through a REST API. Set up CORS middleware to enable communication between the frontend and backend servers.

**Week of 3/9/26 - 3/15/26:**
Completed the frontend implementation using Next.js 16 with React 19 and TypeScript. Implemented a modern, polished dark-themed UI with custom animations using Framer Motion and Tailwind CSS 4. Key features developed include:

- **Protein Generator Module:** Interactive sequence generation interface with real-time backend status monitoring, support for all three GAN architectures, configurable batch sizes, and export functionality (JSON, FASTA, CSV formats)
- **Performance Dashboard:** Real-time metrics visualization using Recharts with area and bar charts showing generation trends and protease distribution
- **ESMFold 3D Visualization Modal:** Interactive modal for viewing generated sequences with links to ESMFold structure prediction API
- **Sequence Comparison Tool:** Side-by-side peptide comparison with similarity analysis and biophysical property prediction (hydrophobicity, net charge)
- **ADMET Profiler:** Pharmacokinetics prediction interface with Lipinski's Rule of Five validation and toxicology screening
- **Training Studio:** Simulated GAN training interface with progress tracking
- **Sequence History Tracking:** Automatic logging of all generation sessions with timestamps and model metadata

Enhanced the user experience with custom scrollbar styling, gradient animations, backend connectivity status indicators, and comprehensive error handling with detailed troubleshooting instructions. The final product demonstrates all aspects of the research in an accessible, interactive format suitable for presentation and demonstration purposes.

## Timeline Update

\begin{longtable}{|p{3cm}|p{6cm}|p{6cm}|}
\hline
\textbf{Date} & \textbf{Goal} & \textbf{Met?} \\
\hline
1/6/2026 & Design comprehensive experimental validation protocol for EGSCYGTR peptide & Done \\
\hline
1/6/2026 & Submit experimental design to Dr. Hanson for approval & Done \\
\hline
1/15/2026 & Receive approval and finalize equipment access & Done \\
\hline
1/21/2026 & Submit inquiry for custom AMC-labeled protease reagent & Done \\
\hline
1/23/2026 & Receive quote and evaluate feasibility for RSEF timeline & Done \\
\hline
1/27/2026 & Begin developing RSEF presentation materials & Done \\
\hline
1/30/2026 & Continue refining presentation design and content & Done \\
\hline
2/7/2026 & Finalize all RSEF submission materials (presentation, abstract, summary) & Done \\
\hline
2/10/2026 & Deliver class presentation and collect feedback & Done \\
\hline
2/15/2026 & Incorporate presentation feedback and refine for RSEF & Done \\
\hline
2/23/2026 & Complete RSEF poster presentation and competition & Done \\
\hline
3/1/2026 & Begin development of AegisGAN web platform & Done \\
\hline
3/5/2026 & Complete backend API implementation with FastAPI & Done \\
\hline
3/8/2026 & Integrate all three GAN models with REST API endpoints & Done \\
\hline
3/10/2026 & Complete frontend framework setup with Next.js and React & Done \\
\hline
3/12/2026 & Implement core features: generator, dashboard, visualizations & Done \\
\hline
3/14/2026 & Add advanced features: ESMFold modal, sequence comparison, ADMET profiler & Done \\
\hline
3/15/2026 & Finalize UI/UX enhancements and complete web platform & Done \\
\hline
\end{longtable}

## Reflection

This period marked the transition from research presentation to final product development. The RSEF competition provided valuable experience in communicating complex computational biology research to a diverse scientific audience, and the positive reception confirmed the novelty and potential impact of the ensemble GAN approach for substrate design. The decision to develop the AegisGAN Dashboard as the final research product was motivated by a desire to make the work more accessible and interactive beyond static figures and presentations.

The web platform development required integrating multiple technical domains—backend API design with FastAPI, frontend development with modern React frameworks, real-time data visualization, and seamless integration with the trained GAN models. The most challenging aspect was ensuring smooth communication between the Next.js frontend and the Python backend while maintaining clean state management for features like sequence history tracking and real-time status monitoring. The implementation of the ESMFold visualization modal and sequence comparison tool extended the platform beyond simple generation, providing users with tools for structural analysis and peptide characterization.

The final AegisGAN Dashboard successfully demonstrates the entire research pipeline in an interactive format: from GAN-based sequence generation across three architectures, to performance metrics visualization, to pharmacokinetics profiling with ADMET predictions. This platform serves as both a demonstration of the research outcomes and a potential foundation for future experimental work, as it provides easy access to the trained models for generating candidate peptides for wet-lab validation. The development process also reinforced the importance of user experience design in scientific software—features like the backend status indicator, detailed error messages, and export functionality make the platform practical for actual use rather than just demonstration.
