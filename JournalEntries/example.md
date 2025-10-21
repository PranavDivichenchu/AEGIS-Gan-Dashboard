---
geometry: margin=0.5in, letterpaper
header-includes:
  - \usepackage{booktabs}
  - \usepackage{longtable}
  - \thispagestyle{empty}
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


### Tuesday October 7

- Started to develop a super basic model for **synthetic biomarker generation** to see if a model could return a potential clevaging protease generation.
  
- Loaded and preprocessed the expanded MEROPS dataset containing encoded peptide cleavage sequences.  
  
- Applied label encoding to amino acid positions (**P4 to P4′**) and standardized feature scales for GAN input.  
  
- Built and trained a **GAN** using PyTorch with the following key details:  
  - **Generator** and **Discriminator** both implemented with **three hidden layers (500 neurons each)** and *LeakyReLU* activations.  
  - Used **latent dimension = 16**, **learning rate = 0.0001**, and **1,000 epochs** for stable training.  
  - Employed **BCELoss** and **Adam optimizers** for adversarial training.  
- The generator successfully began producing a clevage sequence, but I still need to implement the Molecular Docking to see how well the protease can be cleaved.
  

### Thursday October 9

- I was intially training my model in Google Colab, however I realized how inefficent that was. I created a virtual environment with Visual Studio and retrained my model in class. 
  
- At home that day, I trained 2 models that I found on GitHub: the Conditional GAN and MolGAN and began to compare the results.

- I annotated and read a few more articles on additions to the GAN that could potentially help improve the loss on the discriminator and generator because the current models were struggling with the losses plateuing after hundreds of epochs. 

- I found a couple stratgies that could help with this problem including changing the loss function, learning rate, or even taking another look at the data.  


## Timeline

(in latex, use double backslash to separate rows and ampersand for columns. )
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
10/15/2025 & Develop the structure for my own novel GAN and begin first round of training & Started \\
\hline
10/31/2025 & Compare results across GANs and refine input data or architecture for best performance & Not Started \\
\hline
\end{longtable}


## Reflection

On Tuesday, I successfully developed and trained my first GAN for synthetic biomarker generation using the MEROPS dataset. I encoded peptide cleavage sequences, standardized the data, and implemented a three-layer Generator and Discriminator. The model began producing cleavage sequences, marking a strong start, though I still need to test molecular docking to evaluate biological validity.

By Thursday, I improved my workflow by moving training from Google Colab to a local Visual Studio environment, allowing faster and more stable experiments. I also trained Conditional GAN and MolGAN models for comparison and reviewed literature on stabilizing GAN training, identifying potential improvements like adjusting the loss function and learning rate to reduce plateauing.


