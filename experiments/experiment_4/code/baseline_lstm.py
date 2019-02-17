from keras import layers
from keras import models
from utils import *
import numpy as np 
import os
import keras

"""
Author: Tuan Truong

This is the python version of the model implemented in Matlab. Details for the architecture of the model,
please check the README in experiment 3. The first part of this script loads the data and defines the network.
In case you only want to load the weight and not to train the entire model again, comment all the lines that
load the data and set 'load_weight' to True. The weights are then loaded and saved in a .h5 file.

"""
# Define parameters for the model
hidden_neurons = 70
num_input_features = 123
num_output_features = 107
lambda_regularizer = 0.0001
lr = 0.001
decay = 0
regularizer = keras.regularizers.l2(lambda_regularizer)
optimizer = keras.optimizers.Adam(lr=lr)
loss = 'mse'
batch_size = 3

# Define the model
inputs = layers.Input(shape=(None,num_input_features))
x = layers.LSTM(hidden_neurons,return_sequences=True)(inputs)
x = layers.Dense(num_output_features,activation='linear')(x)

# create model and compile
model = models.Model(inputs=inputs,outputs=x)
model.compile(optimizer=optimizer,loss=loss)
print(model.summary())

# Load the data here
pacing_text = ['LV','RV','BiV','LBBB']
data_dir = '../parse_data'
X,y = data_loader(pacing_text,data_dir,normalize=False)
X_train = X[[0,2,3],:700,:]
y_train = y[[0,2,3],:700,:]
X_test = np.expand_dims(X[1,:700,:],axis=0)
y_test = np.expand_dims(y[1,:700,:],axis=0)

print('Shape of X_train:',X_train.shape)
print('Shape of y_train:',y_train.shape)
print('Shape of X_test:',X_test.shape)
print('Shape of y_test:',y_test.shape)

# training
# load weights
load_weights = True
if load_weights:
	weights = process_weights('weights/Exp16/BiV_weights_exp16.mat')
	model = load_weight(model,weights)
	model.save('BiV_attention_model.h5')
else:
	early_stopping = keras.callbacks.EarlyStopping(patience=20)
	model_checkpoint = keras.callbacks.ModelCheckpoint('test_baseline_model.h5',save_best_only=True,verbose=1)
	model.fit(X_train,y_train,epochs=200,batch_size=batch_size,validation_data=(X_test,y_test),callbacks=[model_checkpoint])
	model = keras.models.load_model('test_baseline_model.h5')
y_pred = model.predict(X_test)
# np.save('RV_weight_load_pred',y_pred)

