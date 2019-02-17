function [cleanSignals] = preprocess_data(signals,badleadsPosition,dimReduce)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
% PREPROCESS_DATA preprocesses the signals as input for the network
% Inputs:
%   - signals: [num_signals x num_samples] matrix of original signals
%   - badleadsPosition: [1 x num_signals] matrix of logical bad leads position
%   - dimReduce: (boolean) whether or not to reduce dimension using PCA
% Returns:
%   - cleanSignals: [new_num_ECGs x num_samples] new clean signals
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

badIdx = find(badleadsPosition);

signals(badIdx,:) = [];

for idx=1:size(signals,1)
    signals(idx,:) = transpose(detrend(smooth(signals(idx,:))));

end

if dimReduce == 1
    signals= computePCA(signals);
end
    
cleanSignals = signals(:,1:700);

end

