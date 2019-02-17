# **EXPERIMENT 4**
**Still being updated**

This experiment looks to find the most useful ECGs for reconstructing EGMs. The methodology is based on gradient-based Class Activation Mapping, which is to find the flowing gradients the output back to the input. These flowing gradients show the activation of the input with respect to the output. In other words, they show at which input the output shall look the most for reconstruction. The gradients obtained is then multiplied with the input to see which parts of the input is highly activated.\
For the sake of time, this experiment is made for only **BiV pacing sock 106**.\
To test which ECG is important, the experiment is conducted by dropping each ECG (setting to 0) from the set. The order of dropping is done in 4 cases:
+ Case 1: drop only positive ones from the less positive ones to the most positive ones.
+ Case 2: drop only positive ones from most positive ones to less positive ones.
+ Case 3: drop only negative ones from most negative ones to less negative ones.
+ Case 4: drop only negative ones from less negative ones to most postive ones.

## **Directory**
```bash
|----code
|----result
|    |----case
|    |    |----figures
|    |    |----pcc.mat
|    |    |----socks.mat
|----README.md
```
The `code` folder contains my python code in keras library for finding the gradients of outputs wrt inputs.(At least for now, Matlab does not support finding gradients using backprop). In order to use this code, the weights from Matlab model must be extracted and loaded to a Python model. The weights in this folder are extracted from `experiment_3`, which is the best model on Matlab so far. Before using the code, install the packages in `requirements.txt`.

The `result` folder contains the result in each `case`. The `figures` folder shows reconstructed EGMs each at every drop of a ECG in the input. The names of files, for example `1_123.png` and `2_63.png` refer to the first drop of only the 123rd ECG and the second drop of both the 123rd and 63rd ECG. The `socks.mat` show the order of ECGs to drop in each case and `pcc.mat` is the Pearson Correlation Coefficient at each drop.

## **Layer Configuration and Parameters**
Same as experiment 3

## **Result**
See `result` in each case.

### **Quick observation**

When no drop is perform, the PCC of sock 106 is 0.9558.


In case 1, the drop starts with ECGs of which gradients are positively near 0 and the PCCs do not change much (~0.95) because these small gradients contribute not much to the reconstruction. However, approximately after the 15th drop, PCCs start to drop in faster rate, indicating those later ECGs are of higher importance. To confirm this, case 2 examines the drop but from the ECGs with most positive gradients and the PCCs drop quickly from the 4th drop showing again the ones with most positive gradients are important.

However, when it comes to the negative case, the results look quite confusing as in both cases (dropping from less negative or most negative gradients) the PCCs do not change much. Even when all dropping all negative gradient ECGs, the PCC is ~0.96, refering those ECGs may not be usefull like those with gradients positively near 0 in case 1 and 2.
