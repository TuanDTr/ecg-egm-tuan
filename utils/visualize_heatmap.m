function [] = visualize_heatmap(coeff,heatmap_title)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% VISUALIZE_HEATMAP visualizes the coefficients of reconstructed EGMs as
%                   heat map
% Inputs:
%   - coeff: a matrix of shape [1 x 107] containing coefficients of
%   reconstructed EGMs (there is 107 signals as the first one is a broken
%   lead)
%   - title: (str) title of the heatmap
% Returns:
%   - The heat map of coefficients in shape of [9 x 12], which is the same as
%     the way socks are arranged in INRIA dataset.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

addpath('../');
temp = ones(1,128);
temp = coeff;
% temp([1,12,82]) = 0; % bacause the first one is broken
% temp(2:11) = coeff(1:10);
% temp(13:81) = coeff(11:79);
% temp(83:108) = coeff(80:105);
for n= 0:11
    new_temp(:,n+1) = temp(n*9 + 1:(n+1)*9);
end
heatmap(new_temp);
colormap autumn;
title(heatmap_title);

end

