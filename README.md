# **ECG-EGM RECONSTRUCTION USING NEURAL NETWORK**
This repo is part of the summer research program at the University of Auckland - New Zealand. The research project aims to investigate the reconstruction of EGMs from ECGs and their relationship. All important codes as well results are saved in this repo. The structure of this repo is as the following:
```bash
|----trainLSTM_final.m
|----load_data.m
|----preprocess_data.m
|----utils
|     |----compute_AT.m
|     |----visualize_heatmap.m
|     |----visualize_reconstruction.m
|     |----plot_weights.m
|     |----visualize_histogram_distribution.m
|     |----calculateCorrelation.m
|     |----computePCA.m
|----experiments
|     |----figures
|     |----README.md
|----keras
|----report.pdf
|----README.md
```
## **Details**
1. `trainLSTM_final.m` the main script for training and validation
2. `load_data.m` function to load data from raw structure in INRIA dataset
3. `preprocess_data.m` function to preprocess data by removing and broken leads and smoothing the signals
4. `utils` folder containing functions for visualizing results and further analysis
+ `compute_AT.m` function computing the activation time of signals
+ `visualize_heatmap.m` function to visualize the PCCs (or activation time,etc) in a heatmap with the same arrangement as the sock map
+ `visualize_reconstruction.m` function to plot predicted EGM and true EGM in the same plot
+ `plot_weights.m` function to plot 2 matrix weights in a scatter plot
+ `visualize_histogram_distribution.m` function to visualize the weight distribution in histogram
+ `calculateCorrelation.m` function to calculate the Pearson Correlation Coefficient (PCC) between the true and predicted EGM
+ `computePCA.m` function to reduce the dimension (here: the number of ECGs) to ones that best explain the ECG set

5. `experiment` folder containing details of important experiments with figures and results. There will be subfolders for each experiment:
+ `experiment_1`: parameter search for constructing LSTM model
+ `experiment_2`: findings about weight correlation and distribution when examining the network
+ `experiment_3`: training with the best parameters obtained from `experiment_1` and visualizing the reconstructed PCCs in a heatmap
+ `experiment_4`: looking for the useful ECGs in reconstructing EGM
+ `experiment_5`: computing the activation time for the new dataset.

6. `keras` folder containing code in python. This set of codes is intended for the encoder-decoder solution to solve the sequence to sequence solution. The code includes encoder-decoder script with and without teacher forcing. Read the README inside this folder for more insights.
7. `report.pdf` the final report

