# **EXPERIMENT 2**
As this is a small size dataset, training with leave-one-out cross-validation is expected not to cause a significant change in weight distribution between folds. However, when switching to validation on a pacing that has been included in the training set of the previous trained fold, the average coefficient of reconstructed EGMs of that pacing drops by almost half. This fact suggests the weights between two different trainings might not be the same. To investigate this possibility, a small-scale experiment is conducted to map 123 ECGs to only the first 10 EGMs. After training, the weights in the LSTM layer is visualized in a scatter plot to see if there exists correlation between 2 sets of weights. In this experiment, LBBB is included during both training and validation.

## **Directory**
**being updated**
```bash
|----figures
|----README.md
```

## **Layer Configuration**
1. Input Layer [123 x 700]
2. LSTM Layer with 70 hidden units
3. Fully-connected layer with 107 units (Linear Activation)
4. Output Layer [10 x 700]

## **Parameters**
1. Learning rate: 0.05
2. Max Epoch: 500
3. L2 Regularization: 0.0001
4. Batch Size: 3 
5. Gradient threshold: 1

## **Cross-Validation**
|**Fold** |**Training Set**|**Validation Set**|
|:-------:|:--------------:|:----------------:|
|1        |RV, BiV, LBBB   |LV                |
|2        |LV, BiV, LBBB   |RV                |
|3        |LV, RV, LBBB    |BiV               |
|4        |LV, RV, BiV     |LBBB
In this experiment, LBBB is included in the training and validation.

## **Result**

It can be clearly seen that the weights after two trainings are not correlated, confirming the possibility of significant weight change. To ensure what actually changes, a histogram is plotted for weight distribution. Even though the range of values in those weight does not vary much, the number of values in the middle, especially near 0 changes a lot between 2 trainings. The change in the number of 0s can damage the learning of such network as it indicates many neurons are unusable.
