function [] = visualize_reconstruction(YPred,YTest,pacing_name,electrode)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% VISUALIZE_RECONSTRUCTION plots reconstructed EGM and true EGM in the same plot
% Inputs
%   - YPred [1x1]: cell array that contains the array of reconstructed EGMs
%     in shape of [num_signals,num_samples].
%   - YTest [1x1]: cell array that contains the array of true EGMs
%     in shape of [num_signals,num_samples].
%   - pacing_name (str): name of the pacing
%   - electrode (int): the ith electrode to plot
% Returns
%   - plots of reconstructed EGM and true EGM
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
addpath('../');
p1 = plot(YPred{1}(electrode,:),'r');
hold on;
p2 = plot(YTest{1}(electrode,:),'k');
cc = corr(transpose(YPred{1}(electrode,:)),transpose(YTest{1}(electrode,:)),'Type','Pearson');
p1.LineWidth = 2.5;
p2.LineWidth = 2.5;
legend('Predicted EGM','True EGM');
title([pacing_name ' - electrode ' num2str(electrode+1) ' - Correlation: ' num2str(cc)]);
end

