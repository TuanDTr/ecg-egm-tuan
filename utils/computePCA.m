function [new_data] = computePCA(inputSignal)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% COMPUTEPCA reduces the dimensions (here the number of electrodes) to 4
%   ones that best explains the n electrodes
% Inputs:
%   - inputSignal [num_signals x num_samples] array of input signals
% Returns:
%   new_data [4 x num_samples] array of 4 new constructed electrodes
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

[coeff,new_data,latent,tsquared,explained]=pca(inputSignal');
new_data = new_data(:,1:4)';
end

