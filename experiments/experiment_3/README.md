# **EXPERIMENT 3**
This experiment aims to reconstruct 107 EGMs from 123 ECGs. The number here is 107 EGMs (instead of 108) and 123 ECGs (instead of 128) because there are some broken leads as specified in the dataset description. Therefore, all broken leads are excluded from both training and test set. The performance of model will be evaluated by cross-validation (leave-one-out) such that 3 sets of data will be used for training set and the last one is saved for validation (testing).

## **Directory**
```bash
|----figures
|    |----reconstructed_EGMs
|    |----PCC_heatmap
|----net
|    |----net_LVpacing.mat
|    |----net_RVpacing.mat
|    |----net_BiVpacing.mat
|    |----net_Sinus-LBBB.mat
|----README.md
```
The `net` folder contains all the models trained on 4 pacings as cross-validation. The `figures` folder contrains 2 folders of reconstructed EGMs and the heatmap of predicted Pearson Correlation Coefficients.

## **Layer Configuration**
1. Input Layer [123 x 700]
2. LSTM Layer with 70 hidden units
3. Fully-connected layer with 107 units (Linear Activation)
4. Output Layer [107 x 700]

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

In this experiment, LBBB is included in the training set but is excluded during validation.

## **Result**
### **Training**
|**Fold** |**Training Set Average**|**Training Set Std**|
|:-------:|:--------------:|:----------------:|
|1        |0.9268          |0.0921            |
|2        |0.9054          |0.1035            |
|3        |0.9138          |0.0964            |

### **Validation**
|**Fold** |**Validation Set Average**|**Validation Set Std**|
|:-------:|:--------------:|:----------------:|
|1 (LV)        |0.5321          |0.3329            |
|2 (RV)        |0.6140          |0.2626            |
|3 (BiV)       |0.6561          |0.2596            |