from keras.layers import Lambda
from keras import backend as K
from load_data import data_loader
import numpy as np 
import os
import keras

# Define parameters for the model
hidden_neurons = 150
num_input_features = 123
num_output_features = 107
lambda_regularizer = 0.00001
max_decoder_length = 300
lr = 0.001
decay = 0
regularizer = None #keras.regularizers.l2(lambda_regularizer)
optimizer = keras.optimizers.Nadam(lr=lr)
loss = 'mse'
batch_size = 3

# Define the data here
pacing_text = ['LV','RV','BiV','LBBB']
data_dir = '../parse_data'
X,y = data_loader(pacing_text,data_dir,normalize=True)
X_train = X[[0,2,3],:300,:]
y_train = y[[0,2,3],:300,:]
decoder_input_data = np.zeros((y_train.shape[0],1,num_output_features))
X_test = np.expand_dims(X[1,:300,:],axis=0)
y_test = np.expand_dims(y[1,:300,:],axis=0)
val_decoder_input_data = np.zeros((y_test.shape[0],1,num_output_features))

print('Shape of X_train:',X_train.shape)
print('Shape of y_train:',y_train.shape)
print('Shape of X_test:',X_test.shape)
print('Shape of y_test:',y_test.shape)

X_input = [X_train,decoder_input_data]


# Define conder part
encoder_inputs = keras.layers.Input(shape=(None,num_input_features))
encoder = keras.layers.LSTM(hidden_neurons,return_state=True)
encoder_outputs,state_h,state_c = encoder(encoder_inputs)
states = [state_h,state_c]

# Set up decoder
decoder_inputs = keras.layers.Input(shape=(1,num_output_features))
decoder_lstm = keras.layers.LSTM(hidden_neurons,return_sequences=True,return_state=True)
decoder_dense = keras.layers.Dense(num_output_features,activation='linear')

all_outputs = []
inputs = decoder_inputs
for _ in range(max_decoder_length):
	# run decoder at one time step
	outputs,state_h,state_c = decoder_lstm(inputs,initial_state=states)
	outputs = decoder_dense(outputs)
	all_outputs.append(outputs)
	# reinject the outputs as inputs for the next time step
	inputs = outputs
	states = [state_h,state_c]


# Concatenate all predictions
decoder_outputs = Lambda(lambda x: K.concatenate(x,axis=1))(all_outputs)

# Define and compile the model
model = keras.models.Model([encoder_inputs,decoder_inputs],decoder_outputs)
model.compile(optimizer=optimizer,loss=loss)



model.fit(X_input,y_train,batch_size=batch_size,epochs=200,validation_data=([X_test,val_decoder_input_data],y_test))