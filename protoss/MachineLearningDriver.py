#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 22:53:59 2018

@author: EvanTroop

Sources : 
        Evan's Sources : 
            https://colab.research.google.com/drive/1HN7vgxBFfuZioyHiHTD5Noh2rNY_WbmH?authuser=2#scrollTo=2I8E2qhyKNd4
            http://blog.teamtreehouse.com/python-single-line-loops
            https://stackoverflow.com/questions/15891038/change-data-type-of-columns-in-pandas
            https://stackoverflow.com/questions/29576430/shuffle-dataframe-rows
            https://stackoverflow.com/questions/48208128/uninstalling-tensorflow-from-anaconda-environment
            https://www.tensorflow.org/versions/r1.5/api_docs/python/tf/contrib/data/Dataset
            
            
            Q - Learning
            https://github.com/MorvanZhou/Reinforcement-learning-with-tensorflow/blob/master/contents/1_command_line_reinforcement_learning/treasure_on_right.py
            https://www.youtube.com/watch?v=79pmNdyxEGo
            https://www.youtube.com/watch?v=A5eihauRQvo
            
    Questions : 
        how do hidden layers work?
        does the hidden[0] specify input nodes? or how does that work
"""
from __future__ import print_function
import math

from IPython import display
from matplotlib import cm
from matplotlib import gridspec
from matplotlib import pyplot as plt
from sklearn import metrics
from sklearn import utils

import pandas as pd
import tensorflow as tf
import numpy as np


from tensorflow.contrib.data import Dataset




def main(raw_data, sel_features, target_output):
    """
    INFO
        type_of_learning : what type of learning is desired
        
        data : a pandas data frame of all data that must be processed
        
        sel_features : an array of the headers of what should be sorted
        
        target output : what you want to predict, should be a string and the name of prediction header
        
        split : how you want to split training data, test data, validation data
    """
    percent_training = 0.8
    percent_validation = 0.1
    percent_test = 0.1
    

    
    
    print("Input Data Recieved :")
    print(raw_data)
    raw_data.describe()
    
    data = raw_data[raw_data[target_output].notnull()]
    data = utils.shuffle(data)#Fixed
    data.describe()
    
    number_training = int(len(data) * percent_training)
    number_validation = int(len(data) * percent_validation)
    number_test = int(len(data) - number_training - number_validation)
    
    training_examples = get_required_features(data.iloc[:number_training], sel_features)#Fixed
    training_targets = get_target_data(data.iloc[:number_training], target_output)
    
    validation_examples = get_required_features(data.iloc[number_training : number_validation], 
                                                sel_features)
    validation_targets = get_target_data(data.iloc[number_training : len(data) - number_validation], 
                                         target_output)
    
    print(number_training)
    print(number_validation)
    
    print("dhghsjshsjshdjsgs")
    #print(validation_targets)
    
    test_examples = get_required_features(data.iloc[-1 * number_test:], 
                                          sel_features)
    test_targets = get_target_data(data.iloc[ -1 * number_test:], 
                                   target_output)
    
    neural_network = train_neural_network(learning_rate = 0.0001,
                                          steps = 10,
                                          batch_size = 1,
                                          hidden_units = [3,10,10],
                                          target_output = target_output,
                                          training_examples = training_examples,
                                          training_targets = training_targets,
                                          validation_examples = validation_examples,
                                          validation_targets = validation_targets)
   
    
    
    
    #This will make sure that the target output has data that it can use to learn 
    """
    if len(target_output_data.isnull()) == 0:
        print("Error: No known ouputs, cannot learn")
        return
        
    """
    
    
    
    
    
    
    
    
    
def get_required_features(data, sel_features):
    
    """
    INFO:
        data is a pandas data frame of all data that must be processed
        
        sel_features is a the an array of the headers of what should be sorted
        
        will return a copy of the data frame of selected features
    """
    temp = True
    for feat in sel_features:
        if feat not in data.columns :
            temp = False
    
    if temp:
        print("Getting Features : contain successful")
        
        req_features = data[sel_features]
        return req_features.copy()
 
    
def get_target_data(data, output_target_header):
    """
    INFO :
        data is all data(or after wanted features )
    """
    
            
    if output_target_header in data.columns:
        print("Preparing Data : contain successful")
        output = pd.DataFrame()
        output[output_target_header] = data[output_target_header]
        
        return output


def get_TensorFlow_features(training_data_headers):
    """
    Construct the Tensor Flow Features, doent take data
    
    """
    return set([tf.feature_column.numeric_column(f) for f in training_data_headers])



def pretrain_neural_net(features, targets, batch_size = 1, shuffle = True, num_epochs = None):
    """
    INFO:
        features : pandas data frame of data used for prediction
        targets : pandas DataFrame, target output infomation
        batch_size: defualt 1, size of batches to be passed to model
        shuffle : defualt True, whether to shuffle given data
        num_epochs : number of epochs for when data should be repreated(none is defualt, means repeat indefinately)
        returns a tuple of featurs, labels for next batch data
    """
    
    features = {key : np.array(value) for key, value in dict(features).items()}
    
#THIS IS CAUSING AN ERROR AND IDK WHY?<DDUKS>DSJAUIFGHSUIAG
    ds = Dataset.from_tensor_slices((features, targets))
    ds = ds.batch(batch_size).repeat(num_epochs)
    
    if shuffle :
       ds = ds.shuffle(10000)
        
    features, labels = ds.make_one_shot_iterator().get_next()
    return features,labels


def train_neural_network(learning_rate, #learning rate(float))
                         steps, #total number of training steps(int)
                         batch_size, #batch size(int)
                         hidden_units, #list of int values that declares the #of hidden layers besides input
                         target_output,
                         training_examples, #Dataframe containing multiple columns from origional data
                         training_targets, #Dataframe which must be exacly one column
                         validation_examples, #Validation equivalent of the training examples
                         validation_targets#Validation equivalent to training targets
                         ):
    
    """
    Train the neural network on the given training_examples, with actual labels as the training_targets, 
    Validation targets and examples used to determine accuracy so not to overfit
    INFO:
        
        
        returns the trained neural net regressor object
    """
    
    print("ENTER\n\n\n\n\n")
    periods = 30 # arbitrary, i can send in later also not really nescessary
    steps_per_period = steps / periods
    
    optimizer = tf.train.GradientDescentOptimizer(learning_rate = learning_rate)
    
    #THIS IS WHERE CLIPPING WOULD OCCUR : NOT WORKING PROPERLY
    #gradients, _ = tf.clip_by_
    
    
    
    #optimizer = tf.estimator.clip_gradients_by_norm(optimizer, 5.0)
    
    neural_net_regressor = tf.estimator.DNNRegressor(
            feature_columns = get_TensorFlow_features(training_examples),
            hidden_units = hidden_units,
            optimizer = optimizer)
    
    training_input_fn = lambda : pretrain_neural_net(training_examples, 
                                                     training_targets[target_output],
                                                     batch_size = batch_size)
    predict_training_input_fn = lambda : pretrain_neural_net(training_examples,
                                                              training_targets[target_output],
                                                              num_epochs = 1,
                                                              shuffle = False)
    predict_validation_input_fn = lambda : pretrain_neural_net(training_examples, 
                                                               training_targets[target_output],
                                                               num_epochs = 1,
                                                               shuffle = False)
    print("NEXT 1\n\n\n\n")
    
    training_rmse = []
    validation_rmse = []
    print(type(periods))
    for period in range(0, periods):
        print("NEXT2 \n\n\n")
        neural_net_regressor.train(
                input_fn = training_input_fn,
                steps = steps_per_period)
        
        print()
        training_predictions = neural_net_regressor.predict(input_fn = predict_training_input_fn)
        training_predictions = np.array([item['predictions'][0] for item in training_predictions])
        
        validation_predictions = neural_net_regressor.predict(input_fn = predict_validation_input_fn)
        validation_predictions =  np.array([item['predictions'][0] for item in validation_predictions])
        
        # Compute Loss
        training_sq_error = math.sqrt(metrics.mean_squared_error(training_predictions, training_targets))
        
        print("PREDICTIONS")
        print(validation_predictions)
        print(len(validation_predictions))
        print("Targets")
        print(type(validation_targets))
        
        validation_sq_error = 2 #math.sqrt(metrics.mean_squared_error(validation_predictions, validation_targets))
        
        print("Period : " + str(period) + " : ")
        print("Loss : " + str(training_sq_error))
    
        training_rmse.append(training_sq_error)
        validation_rmse.append(validation_sq_error)
    print("Finished Training")
    
    plt.ylabel("Square Error")
    plt.xlabel("Periods")
    plt.title("Square Error vs Periods")
    plt.tight_layout()
    plt.plot(training_rmse, label = "Training")
    plt.plot(validation_rmse, label = "Validation")
    plt.legend()
    
    print('final squared error for trainitg: ' + training_sq_error)
    print('final squared error for validation' + validation_sq_error)
    return neural_net_regressor


""" ==================== """

x = []
print(type(x))
for i in range(1000):
    x.append(i)
y = []
for i in range(1000):
    y.append(i * 2.6)
z = [] 
for i in range(1000):
    z.append(i ** 2)

data = pd.DataFrame(data = {'x' : x, 'y' : y, 'z' : z})

main(data, ['x', 'y'], 'z')