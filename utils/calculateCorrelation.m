function [coeffAvg,coeffStd] = calculateCorrelation(YPred,YTest)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% CALCULATECORRELATION computes the Pearson correlation coefficients between YPred and
%   YTest and returns the mean and std across different electrodes
% Inputs:
%   - YPred [num_EMGs x num_samples] predictions from the trained model
%   - YTest [num_EMGs x num_samples] ground truth from test set
% Returns:
%   - coeffAvg: the mean of Pearson correlation across num_ECGs
%   - coeffStd: the std of Pearson correlation across num_ECGs
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

coeff = sum(corr(transpose(YPred),transpose(YTest),'Type','Pearson').*eye(size(YPred,1)),1);
coeffAvg = mean(coeff);
coeffStd = std(coeff);
end

