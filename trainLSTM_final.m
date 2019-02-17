clear all;
close all;
clc;
addpath('./utils');
% This script trains a LSTM model to reconstruct HSPs to BSPs
% Option includes in the preprocessing:
%   PCA: whether or not to use PCA

% THIS SCRIPT IS FOR TIME SERIES ONLY

%%%%%%%%%%%%% Define the path to signals %%%%%%%%%%%%%%
pacingText = {'LVpacing','RVpacing','BiVpacing','Sinus-LBBB'};
rootDir = 'data/INRIA/';
signalType = {'AvgBeatVe'};% [AvgBeatVe,singleBeatVe,singleBeatFilt50,rawVe]

%%%%%%%%%%%%% Load and Preprocess signals %%%%%%%%%%%%%
usePCA = 1;
numSignals = 0;
for pacing=1:length(pacingText)
    for type=1:length(signalType)
        numSignals = numSignals + 1;
        fileDir = [rootDir 'Signals_' pacingText{pacing} '.mat'];
        [sockSignals,bodySignals,sockLogical,bodyLogical] = load_data(fileDir,signalType{type});

        sockSignals = preprocess_data(sockSignals,sockLogical,~usePCA);
        bodySignals = preprocess_data(bodySignals,bodyLogical,~usePCA);
        data{numSignals} = bodySignals(:,:);
        target{numSignals} = sockSignals(:,:);
    end
end
indices = [1,2,3,4];
count = 0;
%%%%%%%%%%%%% Create the train and test set %%%%%%%%%%%%%%

for i=1:length(pacingText)
test = i == indices;
train = ~test;
X = data(train);
Y = target(train);
fprintf(['Using ' pacingText{test} ' as test set \n']);

%%%%%%%%%%%%% Define  parameters for the network %%%%%%%%%%%%%
numOutputs = size(Y{1},1); fprintf('NumOutputs: %d \n',numOutputs);
numHiddens = [70];
numFeatures = size(X{1},1); fprintf('NumFeatures: %d \n',numFeatures);
maxEpochs = 500;
miniBatchSize = 3;
learningRate = [0.005];

%%%%%%%%%%%% Start the training loop %%%%%%%%%%%%
for num =1:length(numHiddens)
    for lr= 1:length(learningRate)
        count = count + 1;
        cache(count,1) = find(test);
        cache(count,2) = numHiddens(num);
        cache(count,3) = learningRate(lr);
        fprintf('Using %d hidden units \n',numHiddens(num));
        fprintf('Using learning rate of %f \n',learningRate(lr));
        %%%%%%%% Config network layer and initial weights %%%%%%%
        layers = [ ...
                sequenceInputLayer(numFeatures)
                lstmLayer(numHiddens(num),'OutputMode','sequence')
                fullyConnectedLayer(numOutputs)
                regressionLayer];

        seed = [1,2,3,4,5,6,7,8];
        rng(seed(1));layers(2).InputWeights = randn([4*numHiddens(num) numFeatures])*0.01;
        rng(seed(2));layers(2).RecurrentWeights = randn([4*numHiddens(num) numHiddens(num)])*0.01;
        rng(seed(3));layers(2).Bias = randn([4*numHiddens(num) 1]);
        rng(seed(7));layers(3).Weights = randn([numOutputs numHiddens(num)]);
        rng(seed(8));layers(3).Bias = randn([numOutputs 1]);
        
        %%%%%%%%% Define training options %%%%%%%%%%
        options = trainingOptions('adam', ...
            'MaxEpochs',maxEpochs, ...
            'InitialLearnRate',learningRate(lr), ...
            'Shuffle','once', ...
            'Plots','None',...
            'Verbose',0,...
            'GradientThreshold',1, ...
            'VerboseFrequency',1,...
            'MiniBatchSize',miniBatchSize,...
            'L2Regularization',0.0001);

        %%%%%%%%%% Train the network %%%%%%%%%%%
        net = trainNetwork(X,Y,layers,options);
        % save(['experiments/experiment_17/net_' pacingText{test} '.mat'],'net')
        
        %%%%%%%%%% Evaluate the network %%%%%%%%%%
        % Evaluate on train set. Print PCC mean and std of all 3 training examples.
        YPred = predict( net,X);
        for i=1:length(YPred)
            [trainCoeffAvg,trainCoeffStd] = calculateCorrelation(YPred{i},Y{i});
            fprintf('******Training Pearson CCs mean %f and std %f \n',trainCoeffAvg,trainCoeffStd);
            s_train(i) = trainCoeffAvg;
        end 
        cache(count,4) = mean(s_train);
        cache(count,5) = std(s_train);
        % Evaluate on test set. Print PCC mean and std of the test example
        YPred = predict(net,data(test));
        for i=1:size(target{test},1)
            [testCoeffAvg,testCoeffStd] = calculateCorrelation(YPred{1}(i,:),target{test}(i,:));
            %fprintf('******Test Pearson correlation mean %f and std %f \n',testCoeffAvg,testCoeffStd);
            s(i) = testCoeffAvg;
        end
        cache(count,6) = mean(s);
        cache(count,7) = std(s);
        fprintf('****** Test Pearson CCs mean %f and std %f \n',mean(s),std(s));
    end
end
end
% save('cache_new_data.mat','cache');