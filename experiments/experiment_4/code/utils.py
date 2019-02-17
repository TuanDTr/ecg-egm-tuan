import os
import numpy as np 
import random
import keras.backend as K
import matplotlib.pyplot as plt
from scipy.io import loadmat
from sklearn.preprocessing import MinMaxScaler

def data_loader(pacing_text,data_dir,transpose=True,normalize=True):
	"""
	Load data from .mat file
	Inputs:
		pacing_text: name of the pacing
		data_dir: path to the data directory
		transpose: whether or not to transpose the data (for keras model only)
		normalize: whether or not to normalize the data
	Returns:
		X: the data in shape of [num_examples,num_ECGs,time_steps] or [num_examples,time_steps,num_ECGs] if transpose
		y: the target data in shape of [num_examples,num_EGMs,time_steps] or [num_examples,time_steps,num_EGMs] if transpose
	"""
	X = []
	y = []

	for pacing in pacing_text:
		body_signals = loadmat(os.path.join(data_dir,pacing + '_bodySignals.mat'))['bodySignals']
		sock_signals = loadmat(os.path.join(data_dir,pacing + '_sockSignals.mat'))['sockSignals']
		# body_signals = np.delete(body_signals,body_broken_leads,0)
		# sock_signals = np.delete(sock_signals,sock_broken_leads,0)
		if transpose:
			X.append(np.transpose(body_signals))
			y.append(np.transpose(sock_signals))
		else:
			X.append(body_signals)
			y.append(sock_signals)

	X = np.array(X)
	y = np.array(y)
	if normalize:
		X,y = normalize_data(X,y)

	return X,y

def normalize_data(X,y,feature_range=(-1,1)):
	"""
	Normalize data in samples
	Inputs:
		X [num_samples x sequence_length x num_features]
		y [num_samples x sequence_length x num_features]
		feature_range: range to be normalized within
	Outputs:
		X,y after being normalized in the feature range
	"""
	scaler = MinMaxScaler(feature_range=feature_range)
	for sample in range(X.shape[0]):
		for signal in range(X.shape[2]):
			scaler.fit(np.expand_dims(X[sample,:,signal],axis=1))
			X[sample,:,signal] = np.squeeze(scaler.transform(np.expand_dims(X[sample,:,signal],axis=1)))

	for sample in range(y.shape[0]):
		for signal in range(y.shape[2]):
			scaler.fit(np.expand_dims(y[sample,:,signal],axis=1))
			y[sample,:,signal] = np.squeeze(scaler.transform(np.expand_dims(y[sample,:,signal],axis=1)))

	return X,y

def denormalize_data(X_fit,X,feature_range=(-1,1)):
	""" Denormalize data back to the original scale """
	scaler = MinMaxScaler(feature_range=feature_range)
	for signal in range(X.shape[1]):
		scaler.fit(np.expand_dims(X_fit[:,signal],axis=1))
		X[:,signal] = np.squeeze(scaler.inverse_transform(np.expand_dims(X[:,signal],axis=1)))
	return X

def attention(model,X):
	"""
	This is based on the algorithm of Grad-CAM to compute the flowing gradients from the last layers to the
	input layers. This gradient indicates the importance of each ECG to to the EGM.
	"""
	# compute the gradient
	dense_outputs = model.get_layer('dense_1').output
	inputs = model.get_layer('input_1').output
	maps = []
	for i in range(104,105):
		grads = K.gradients(dense_outputs[:,:,i],inputs)
		iterate = K.function([model.input],[grads[0]])
		[np_grads] = iterate([X])
		a = np.mean(np.squeeze(np_grads),axis=0)
		maps.append(a)
	
	return np.array(maps)

def load_weight(model,weight):
	"""
	Load weights to the model
	Inputs:
		model: keras model
		weight: a list of weight tensors
	Returns:
		model that has been loaded weights
	"""
	assert len(model.layers) == len(weight)+1, 'Layers must be the same'
	for i in range(len(model.layers)-1):
		model.layers[i+1].set_weights(weight[i])

	return model

def process_weights(matfiles):
	"""
	Process the weights in a structure that can be loaded into keras model
	Inputs:
		matfiles: path to .mat file which stores the weights from the model
	Outputs:
		[lstm,dense]: a list of weights that are ready to be loaded into keras model
	"""
	lstm_input_weights = read_matfiles(matfiles,'lstm_input_weights')
	lstm_recurrent_weights = read_matfiles(matfiles,'lstm_recurrent_weights')
	lstm_bias = read_matfiles(matfiles,'lstm_bias')
	lstm = [np.transpose(lstm_input_weights),np.transpose(lstm_recurrent_weights),np.squeeze(lstm_bias)]
	dense_weights = read_matfiles(matfiles,'dense_weights')
	dense_bias = read_matfiles(matfiles,'dense_bias')
	dense = [np.transpose(dense_weights),np.squeeze(dense_bias)]

	return [lstm,dense]

def read_matfiles(matfiles,array_name):
	"""
	Read matfiles into numpy arrays
	Inputs:
		matfiles: path the to matfiles
		array_name: name of the array in the matfile
	"""
	files = loadmat(matfiles)[array_name]

	return files