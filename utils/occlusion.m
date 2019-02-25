function [usefulness] = occlusion(net,X,y,grads)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% OCCLUSION monitors the change in Pearson Correlation Coefficient by
% set some ecg satisfying some condition value 0
% Input
%   - net: the trained network
%   - X: input data, a cell array of 1x1
%   - y: target data, a cell array of 1x1
%   - grads: the gradients ob output wrt input. It should have the shape of
%           [num_ecg x num_egm]
% Output
%   - usefullness: the PCC of each predicted EGM when ECG satisfying the
%   condition is set to 0
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
for egm=1:size(y{1},1)
    X_hat = X;
    grad = grads(egm,:);
    %%%%%%%% set the condition here %%%%%%%%
    grad_con = find(grad>=-0.2 & grad<=0.2);
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    X_hat{1}(grad_con,:) = zeros(length(grad_con),size(X_hat{1},2));
    predicts = predict(net,X_hat);
    y_pred(egm) = predicts;
    [avg,std] = calculateCorrelation(predicts{1}(egm,:),y{1}(egm,:));
    usefulness(egm) = avg;
end
end

