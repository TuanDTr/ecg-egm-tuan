# **EXPERIMENT 1**
**being updated**
This experiment is a parameter search to find the optimized choice of parameters for the network. The parameters being tuned include the number of neurons of LSTM layer and learning rate. The model is evaluated using cross-validation (leave-one-out) such that 3 sets of data will be used for training set and the last one is saved for validation (testing). The optimized parameters are chosen in the end if they result in the highest PCCs and the difference of PCCs between validation folds is not big.\
**Note: LBBB is included in both training and validation set**

## **Directory**
```bash
|----figures
|----result.csv
|----README.md
```
## **Layer Configuration**
1. Input Layer [123 x 700]
2. LSTM Layer with hidden units in range of [10:10:100]
3. Fully-connected layer with 107 units (Linear Activation)
4. Output layer [107 x 700]

## **Parameters**
1. Learning rate: in range of [0.001,0.005,0.01,0.05]
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
|4        |LV, RV, BiV     |LBBB              |

## **Result**
See `result.csv`\
From the result, the hidden unit of 70 and a learning rate of 0.005 are chosen parameter.