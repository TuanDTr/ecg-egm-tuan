function [] = visualize_histogram_distribution(weights,legends,plot_title)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% VISUALIZE_HISTOGRAM_DISTRIBUTION visualizes the weight distribution in histogram.
%   This function can visualize up to 3 sets of weights (i.e. weights from
%   different pacings for comparison)
% Inputs:
%   - weights: a cell array containing all sets of weights to be visualized
%   - legends: a cell array containg legends corresponding to each set of
%              weight in 'weights' array
%   - plot_title (str): title of the plot
% Returns:
%   - histogram displaying the weight distribution
% Notes: 'weights' and 'legends' must have the same length
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if length(weights) ~= length(legends)
    error('Length mismatch. Check dimension of weights and titles');
else
    edgecolor = {'b','r','g'};
    for i=1:length(weights)
        weight_h = size(weights{i},1);
        weight_w = size(weights{i},2);
        weight = reshape(weights{i},[1,weight_h*weight_w]);
        histogram(weight,'FaceColor','None','EdgeColor',edgecolor{i});
        hold on;
    end
    legend(legends);
    title(plot_title);
end
end

