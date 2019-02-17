function [at] = compute_AT(X,visualize,name)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% COMPUTE_AT computes the activation time of reconstructed EGMs by
%            evaluating the most negative dV/dt of the signal.
% Inputs
% - X [num_signals,num_samples]: The reconstructed signal. This should have
%   the shape of [107,700] in order to be visualized as heat map. If the
%   the number of signals is different from 107, please modify the
%   'visualize_heatmap' function
% - visualize (logical): whether or not to visualize the activation time as
%   heat map. 1 for visualizing and 0 otherwise.
% - name (str): the name of heat map in case of visualizing. If the visualize
%   is 0, specify name as ''.
% Returns
% - at [1,num_signals]: array of activation time
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

for signal=1:size(X,1)
        idx = find(gradient(X(signal,10:300)) == min(gradient(X(signal,10:300))));
        at(signal) = (idx/2000)*1000;
end
if visualize
    visualize_heatmap(at,name);
end
end

