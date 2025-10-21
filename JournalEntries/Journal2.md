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

# \hfill Journal Report
## \hfill Pranav Divichenchu
\vspace{-0.5em}
\hfill October 13, 2025

\vspace{1em}
\hrule
\vspace{0.5em}

**Research Topic:** Design a Generative Adverserial Network (GAN) to design novel protein sequences that are able to predict and enhance model clevage. 

**Mid October Goal:** (What will you have done by 10/15-ish)

Annotate articles on novel usage of GAN that I could potentially use for my own. I also want to develop an initial baselines GANs, potentially one from class, and a few others from open source websites (Hugging Face or Github)


I want to begin collecting and downloading the cleavage and molecule data from Merops mainly through web scraping, but also looking through the website. (If possible - I’ve looked and haven't been able to find any trustworthy sources) I also want to download external data, other than Merops that I could potentially use to make the dataset bigger. I also NEED to download molecules that do NOT result in a cleavage


Analyze the data and see what specific strands in the sequence may hint at success during cleavage  (something to highlight as an input when training the GAN).

**October Goal:** (And by 10/30-ish)

Develop my own novel GAN using a variety of techniques I have found through research.

Begin training my GAN + the other baseline GANs over a few days.


Compare the results of the GAN and see whether improvements can be made to my own personal GAN or just to pick up one of the baselines to go forward with the process.
Also potentially find and choose a fluorescence attachment that would latch onto the molecules, but that likely would have to wait for after the “best” protein sequence had been created.
  
If the model is spitting out good results, then potentially choose a target protein sequence 


\vspace{1em}
\hrule
\vspace{1em}

## Daily Log (10/5/25-10/12/25)


### Tuesday October 14

- Began to develop a Conditional GAN - ConditionalGAN.py
    - Added protease-specific conditioning using label embeddings
    - Architecture: 3-layer networks with BatchNorm1d
    - Trained for 300 epochs with lr=0.001
    - Generated protease-specific cleavage sequences
- Annotated and went through GitHub looking for projects that utilize GANs, noting down what they do specifically. 
  - Wasserstein Distance 
  - Graident Penalty
  - Self-Attention mechanisms
  - Spectral normalization
  - Batch Normalization
  - Multi-class classification - one of the most important for this project because there are various proteseases in the training data, to specifiying which one specifically is essential.


### Thursday October 16

  1. WGAN-GP - WGAN_GP.py
    - Implemented Wasserstein GAN with Gradient Penalty for improved
  training stability
    - Replaced Discriminator with Critic (no sigmoid activation)
    - Used Wasserstein loss instead of BCE
    - Configured with 5 critic updates per generator update (n_critic=5)
    - Included gradient penalty (lambda_gp=10) for Lipschitz constraint
  enforcement

  1. SupremeGAN - SupremeGAN.py
    - Developed my own novel advanced GAN incorporating cutting-edge
  techniques:
        - Self-attention mechanism (from SA-GAN) for long-range dependencies
      - Spectral normalization throughout the network
      - Conditional Batch Normalization (from BigGAN)
      - Residual connections with conditional normalization
      - Multi-task learning: Real/fake discrimination + protease
  classification
      - Diversity loss to prevent mode collapse
      - Consistency regularization for robustness
    - Larger architecture: latent_dim=128, hidden_dim=256, batch_size=64
    - Trained for 400 epochs with learning rate schedulers
    - Generated comprehensive metrics: Wasserstein distance, auxiliary
  accuracy, diversity scores



## Timeline

\begin{longtable}{|p{3cm}|p{6cm}|p{6cm}|}
\hline
\textbf{Date} & \textbf{Goal} & \textbf{Met?} \\
\hline
9/25/2025 & Finish annotating GAN-related research papers and finalize which architectures to replicate & Done \\
\hline
10/06/2025 & Begin collecting cleavage data from Merops and test basic scraping scripts & Done \\
\hline
10/06/2025 & Finish dataset preprocessing + Download and Create initial GANs for testing & Done \\
\hline
10/15/2025 & Develop the structure for my own novel GAN and begin first round of training & Done \\
\hline
10/31/2025 & Compare results across GANs and refine input data or architecture for best performance & Not Started \\
\hline
\end{longtable}


## Reflection

Over the past two weeks, I believe I have met my mid-October goals by laying a solid foundation for my GAN-based protein cleavage research. I annotated several research papers and GitHub repositories on advanced GAN architectures, identifying useful techniques such as gradient penalties, self-attention, and spectral normalization to incorporate into my own design. I also began collecting and analyzing cleavage data from Merops, experimenting with basic web scraping scripts and verifying data quality. I implemented multiple baseline models—including a Conditional GAN and WGAN-GP—and designed my own advanced model, SupremeGAN, which integrates multi-task learning and conditional normalization. Overall, I met my objectives by developing and training initial GANs while gaining a clearer understanding of which architectures and loss functions best suit my dataset.

