from keras.models import Model 
from keras.layers import Input,LSTM,Dense
from load_data import data_loader,data_generator
import numpy as np 
import keras

neurons = 50
num_input_features = 123
num_output_features = 107
lambda_regularizer = 0.00001
lr = 0.008
decay = 0
regularizer = keras.regularizers.l2(lambda_regularizer)
optimizer = keras.optimizers.Adam(lr=lr)
loss = 'mse'
batch_size = 3

encoder_inputs = Input(shape=(None,num_input_features))
encoder = LSTM(neurons,return_state=True)
encoder_outputs,state_h,state_c = encoder(encoder_inputs)
encoder_states = [state_h,state_c]

decoder_inputs = Input(shape=(None,num_output_features))
decoder_lstm = LSTM(neurons,return_sequences=True,return_state=True)
decoder_outputs,_,_ = decoder_lstm(decoder_inputs,initial_state=encoder_states)
decoder_dense = Dense(num_output_features,activation='linear')
decoder_outputs = decoder_dense(decoder_outputs)

model = Model([encoder_inputs,decoder_inputs],decoder_outputs)
model.compile(optimizer=optimizer,loss=loss)

pacing_text = ['LV','RV','BiV','LBBB']
data_dir = '../parse_data'
X,y = data_loader(pacing_text,data_dir,normalize=True)
X_train = X[[0,2,3],:,:]
y_train = y[[0,2,3],:,:]
X_test = np.expand_dims(X[1,:,:],axis=0)
y_test = np.expand_dims(y[1,:,:],axis=0)
train_data = data_generator(X_train,y_train)
val_data = data_generator(X_test,y_test)
model.fit_generator(train_data,epochs=50,steps_per_epoch=8,validation_data=val_data,validation_steps=1)

encoder_model = Model(encoder_inputs,encoder_states)
decoder_state_input_h = Input(shape=(neurons,))
decoder_state_input_c = Input(shape=(neurons,))
decoder_state_inputs = [decoder_state_input_h,decoder_state_input_c]
decoder_outputs,state_h,state_c = decoder_lstm(decoder_inputs,initial_state=decoder_state_inputs)
decoder_states = [state_h,state_c]
decoder_outputs = decoder_dense(decoder_outputs)
decoder_model = Model([decoder_inputs]+decoder_state_inputs,[decoder_outputs]+decoder_states)

def decoder_seq(input_seq,num_step_to_predict):
	states_value = encoder_model.predict(input_seq)
	target_seq = np.zeros((1,1,num_output_features))
	y_pred = []

	for step in range(num_step_to_predict):
		decoder_outputs,h,c = decoder_model.predict([target_seq]+states_value)
		y_pred.append(np.squeeze(decoder_outputs))

		target_seq = np.zeros((1,1,num_output_features))
		target_seq = decoder_outputs

		states_value = [h,c]

	return np.array(y_pred)

y_val_pred = decoder_seq(X_test,700)
print(y_val_pred.shape)
np.save('y_val_test',y_val_pred)