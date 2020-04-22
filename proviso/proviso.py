import json

import proviso.utils.NetworkUtils as nu
import proviso.utils.DataUtils as du
import numpy as np
from sklearn.preprocessing import MinMaxScaler


# use this to normalize all values between 0 and 1 (to train the model)
scaler = MinMaxScaler(feature_range=(0, 1))

class ModelData():
	def __init__(self, ticker, model, train_x, test_x, train_y, test_y, dataset, look_back, column):
		self.ticker = ticker
		self.model = model
		self.train_x = train_x
		self.test_x = test_x
		self.train_y = train_y
		self.test_y = test_y
		self.dataset = dataset
		self.look_back = look_back
		self.column = column

def calculatePerasonCorrelationCoefficient(days, array_one, array_two):
	# get last data points 'days' from both arrays
	array_one_slice = array_one[-days:]
	array_two_slice = array_two[-days:]

def getOrTrainModel(ticker, dataframe, cache_path, attribute, model_path, weights_path,
					epochs=100, batch_size=32, look_back=31):
	'''

	If cached data is found, then use the cached price data and weights to compile the trained model

	:param ticker: The stock ticker
	:param dataframe: stock data
    :param cache_path: The path to cached stock data
	:param attribute: The column to predict. This can be 'open', 'close', or 'volume'
	:param model_path: The path to a model, or path to where a model should be saved
	:param weights_path: The path to model weights, or path to where weights should be saved
	:param epochs: The epochs used to train the model
	:param batch_size: The batch_size used to train the model
	:param look_back: The look_back value used to train the model
	:return: The model
	'''
	
	train_x, test_x, train_y, test_y, dataset = du.prepareTrainingData(dataframe, attribute, scaler, look_back)
	# create and fit the LSTM network
	model = nu.getModel(train_x, train_y, test_x, test_y, model_path, weights_path,
						epochs=epochs, batch_size=batch_size, look_back=look_back)
	return ModelData(ticker, model, train_x, test_x, train_y, test_y, dataset, look_back, attribute)


def predictFuture(model_data, num_days_to_predict, output_type, showPlot=False, savePlot=False, savePath=''):
	'''
	Predict the model output num_days_to_predict days in the future
	:param model_data: The model_data holds the model, test data, training data, and look back value
	:param num_days_to_predict: The number of days to predict in the future
	:param output_type: The output type can be either 'plot' or 'json'
	:return: JSON if output type is 'json', show plot if output type is 'plot'
	'''
	# make predictions
	model = model_data.model
	train_predict = model.predict(model_data.train_x)
	test_predict = model.predict(model_data.test_x)
	# for testing purposes only.
	# lets look at what would have predicted last look back period
	future_predict = nu.predictFuture(model, np.asarray(model_data.test_x[-1:]), num_days_to_predict, scaler)
	# future_predict = nu.predictFuture(model, np.asarray(model_data.test_x[-1:]), num_days_to_predict, scaler)

	train_predict, test_predict, train_y, test_y =\
		nu.invert_predictions(train_predict, test_predict, model_data.train_y, model_data.test_y, scaler)

	# nu.scorePrediction(train_predict, test_predict, train_y, test_y)
	if output_type == 'plot':
		du.plotData(model_data.dataset, model_data.look_back, train_predict, test_predict,
					np.asarray(future_predict), scaler, model_data.column + ' - ' + model_data.ticker, savePlot, savePath, showPlot)
		return
	elif output_type == 'json':
		lastPredictedPrice= future_predict[-1:][0]
		todaysPrice = scaler.inverse_transform(model_data.dataset)[-1:][0]
		percentChange = (lastPredictedPrice / todaysPrice)[0]
		return toJson(future_predict, model_data.ticker, model_data.column, percentChange)
	else:
		return future_predict


def toJson(future_predict, ticker, column, percentChange):
	'''
	Convert the future_predict list to json
	:param future_predict: The future predictions
	:return: the json representation of the future predictions
	'''
	json_strings = {}
	json_strings['ticker'] = ticker
	json_strings['column'] = column
	json_strings['percent change'] = percentChange

	datas = []
	i = 1
	for future in future_predict:
		val = future[0]
		data = {
			'day':str(i),
			'price': str(val)
		}
		datas.append(data)
		i += 1

	json_strings['predictions'] = datas
	return json.dumps(json_strings)