import os
import numpy as np 
import random
import keras.backend as K
import matplotlib.pyplot as plt
from scipy.io import loadmat
from sklearn.preprocessing import MinMaxScaler

def data_loader(pacing_text,data_dir,transpose=True,normalize=True):
	X = []
	y = []
	sock_broken_leads = [0]
	body_broken_leads = [43,60,61,123,124]
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
	X [num_samples x sequence_length x num_features]
	y [num_samples x sequence_length x num_features]

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

	scaler = MinMaxScaler(feature_range=feature_range)
	for signal in range(X.shape[1]):
		scaler.fit(np.expand_dims(X_fit[:,signal],axis=1))
		X[:,signal] = np.squeeze(scaler.inverse_transform(np.expand_dims(X[:,signal],axis=1)))
	return X


def data_generator(X,y,max_length=700):

	sample_length = [400,500]
	while True:
		random_length = random.choice(sample_length)
		beginning_point = np.random.randint(0,max_length-random_length)
		small_X = X[:,beginning_point:beginning_point+random_length,:]
		small_y = y[:,beginning_point:beginning_point+random_length,:]
		# small_y = small_y[::-1]
		# decoder_input_data = small_X[::-1]
		decoder_input_data = np.zeros(small_y.shape)
		for sample in range(small_y.shape[0]):
			for egm in range(small_y.shape[2]):
				if beginning_point == 0:
					decoder_input_data[sample,0,egm] = 0
					decoder_input_data[sample,:,egm] = np.roll(small_y[sample,:,egm],1)
				else:
					decoder_input_data[sample,:,egm] = y[sample,beginning_point-1:beginning_point-1+random_length,egm]


		yield ([small_X,decoder_input_data],small_y)

def attention(model,X):
	"""
	This is based on the algorithm of Grad-CAM to compute the flowing gradients from the last layers to the
	input layers. This gradient indicates the importance of each ECG to to the EGM.
	"""
	# compute the gradient
	dense_outputs = model.get_layer('dense_1').output
	inputs = model.get_layer('input_1').output
	maps = []
	for i in range(107):
		grads = K.gradients(dense_outputs[:,:,i],inputs)
		iterate = K.function([model.input],[grads[0]])
		[np_grads] = iterate([X])
		a = np.mean(np.squeeze(np_grads),axis=0)
		maps.append(a)
	
	return np.array(maps)

def heatmap_attention(X):
	num_egms = X.shape[0]
	num_ecgs = X.shape[1]
	egms = range(num_egms)
	ecgs = range(num_ecgs)
	fig,ax = plt.subplots()
	im = ax.imshow(X)
	ax.set_xticklabels(ecgs)
	ax.set_yticklabels(egms)
	plt.setp(ax.get_xticklabels(),rotation=45,ha='right',rotation_mode='anchor')

	for i in range(num_egms):
		for j in range(num_ecgs):
			text = ax.text(j,i,X[i,j],ha='center',va='center')

	ax.set_title('Heat Map')
	fig.tight_layout()
	plt.show()

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