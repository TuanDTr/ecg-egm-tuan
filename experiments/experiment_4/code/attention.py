from keras.models import load_model
from utils import *
from scipy.stats import pearsonr

"""
Author: Tuan Truong
This script finds the gradients of the outputs wrt the inputs by using backprop
The variable grads stores the gradients. For the current implementation, the grads variable should have the shape of [123,700]
Please find the data to load in folder 'data'. This is the data being parsed and preprocessed in Matlab.

"""
pacing_text = ['LV','RV','BiV','LBBB']
data_dir = '../data'
X_ori,y_ori = data_loader(pacing_text,data_dir,normalize=False)

y_test = np.expand_dims(y_ori[2],0)
X_test = np.expand_dims(X_ori[2],0)
model = load_model('BiV_attention_model.h5')
grads = attention(model,X_test)

