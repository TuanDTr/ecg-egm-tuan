function [] = plot_weights(weight_1,weight_2,x_label,y_label,plot_title)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
% PLOT_WEIGHTS plots 2 matrix weights in a scatter plot. This function aims
%              to see how weights from two different training or from
%              differnt pacings look like (whether they are correlated or
%              not).
% Inputs
%   - weight_1: the first weight array (will be reshaped to 1D array in the
%               function)
%   - weight_2: the second weight array (will be reshaped to 1D array in
%               the function)
%   - x_label: name for the xlabel (the first weight matrix)
%   - y_label: name for the ylabel (the second weight matrix)
%   - plot_title: title of the plot
% Returns
%   - scatter plot of two weight matrices
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

h = size(weight_1,1);
w = size(weight_1,2);
% reshape into 1D array
weight_1 = reshape(weight_1,[1,w*h]);
weight_2 = reshape(weight_2,[1,w*h]);
scatter(weight_1,weight_2);
xlabel(x_label);
ylabel(y_label);
title(plot_title);
axis([-2 2 -2 2]);
one_to_one = refline(1,0);
one_to_one.Color='k';
end

