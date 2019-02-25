# **EXPERIMENT 5**
**Still being updated**

This experiment aims to compute the activation time for the new dataset. Initialy the EGM prediction of the new dataset is supposed to use the trained model from the old dataset. However, the broken leads and time steps in the new one are different and thus the old trained model cannot be applied to predict this new one . As a result, a new model has to be trained on the old dataset but preprocessed in the same setting with the new one for prediction and computing the activation time.

## **Directory**
```bash
|----figures
|    |----ECGi_AT_Laura_data_exp16
|    |----predicted_EGM_AT_exp16
|    |----sock_AT_Laura_data_exp16
|    |----sock_AT_my_technique_exp16
|----net
|    |----net_LVpacing.mat
|    |----net_RVpacing.mat
|    |----net_BiVpacing.mat
|----README.md
```
The `net` folder contains all the models trained on 4 pacings as cross-validation. The `figures` contains the following folders:
+ `ECGi_AT_Laura_data_exp16`: Activation time heat map of ECGi from Laura's data 
+ `predicted_EGM_AT_exp16`: Predicted Activation Time heat map on the new data of Exp 16. The net used for prediction has been trained on the old data (exp20) but with modification in order to be validated on new data (exp16)
+ `sock_AT_Laura_data_exp16`: Activation time heat map of average beat data from Laura's activation data 
+ `sock_AT_my_technique_exp16`: Activation time heat map of average beat data using my technique to estimate

## **Layer Configuration**
1. Input Layer [122 x 700]
2. LSTM Layer with 70 hidden units
3. Fully-connected layer with 107 units (Linear Activation)
4. Output Layer [105 x 700]

The same architecture as `experiment_3` is kept except the dimension of input and output is changed due to the difference in broken leads. In addition, the length of time steps is now 600 instead of 700 samples.

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
See the `figures` folder for activation time.

### **Quick observation**
The net screwed up in predicting from the new dataset. The PCCs are low, suggesting weak capability in reconstructing the EGMs. Therefore, the activation time calculated is also confusing.