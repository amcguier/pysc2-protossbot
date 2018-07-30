    # -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 15:41:51 2018

@author: User
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor
This is a temporary script file.
"""
#import os 
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
import math
import numpy as np
import pandas as pd
from sklearn import metrics
#import tensorflow.data as Dataset
import matplotlib.pyplot as plt



training_data = pd.read_csv("testOutput1")
training_data = training_data.reindex(np.random.permutation(training_data.index))
test_data = training_data[45001:50000]
training_data.drop(training_data.index[45000:49999])




def preprocess_features(training_data):
    #selected_features = pd.DataFrame()

    selected_features = training_data[['Nexus', 'Gateway', 'CC', 'StarGate', 'FleetBeacon', 'RoboticsFacility', 'RoboticsBay', 'TwilightCouncil', 'TemplarArchives', 'DarkShrine', 'PC']]
    processed_features = selected_features.copy()
    return processed_features

def preprocess_targets(training_data):
    target_strat = pd.DataFrame()
    target_strat = training_data['Strat']
    return target_strat

training_examples = preprocess_features(training_data.head(40000))
training_targets = preprocess_targets(training_data.head(40000))

validation_examples = preprocess_features(training_data.tail(5000))
validation_targets = preprocess_targets(training_data.tail(5000))

def construct_feature_columns(input_features):
    return set([tf.feature_column.numeric_column(my_feature)
                for my_feature in input_features])
        
def my_input_fn(features, targets, batch_size=1, shuffle=True, num_epochs=None):
    features = {key:np.array(value) for key, value in dict(features).items()}
    ds = tf.data.Dataset.from_tensor_slices((features, targets))
    ds = ds.batch(batch_size).repeat(num_epochs)
    
    if shuffle:
        ds = ds.shuffle(10000)
        
    features, labels = ds.make_one_shot_iterator().get_next()
    return features, labels

def train_linear_regressor_model(learning_rate, steps, batch_size, training_examples, training_targets, validation_examples, validation_targets):
    periods = 10
    steps_per_period = steps/periods
    
    my_optimizer = tf.train.GradientDescentOptimizer(learning_rate = learning_rate)
    my_optimizer = tf.contrib.estimator.clip_gradients_by_norm(my_optimizer, 5.0)
    linear_regressor = tf.estimator.LinearRegressor(feature_columns=construct_feature_columns(training_examples), optimizer = my_optimizer)
    
    training_input_fn = lambda: my_input_fn(training_examples, training_targets, batch_size = batch_size)
    predict_training_input_fn = lambda: my_input_fn(training_examples, training_targets, num_epochs = 1, shuffle=False)
    predict_validation_input_fn = lambda: my_input_fn(validation_examples, validation_targets, num_epochs = 1, shuffle=False)
    
    print("Training model...")
    print("RMSE (on training data):")
    training_rmse = []
    validation_rmse = []
    for period in range (0, periods):
        linear_regressor.train(input_fn = training_input_fn, steps = steps_per_period)
        
        training_predictions = linear_regressor.predict(input_fn = predict_training_input_fn)
        training_predictions = np.array([item['predictions'][0] for item in training_predictions])
        
        validation_predictions = linear_regressor.predict(input_fn = predict_validation_input_fn)
        validation_predictions = np.array([item['predictions'][0] for item in validation_predictions])
        
        training_root_mean_squared_error = math.sqrt(metrics.mean_squared_error(training_predictions, training_targets))
        validation_root_mean_squared_error = math.sqrt(metrics.mean_squared_error(validation_predictions, validation_targets))
        
        print("period %02d : %0.2f" % (period, training_root_mean_squared_error))
        
        training_rmse.append(training_root_mean_squared_error)
        validation_rmse.append(validation_root_mean_squared_error)
        
    print("Model Training Finished.")
    
    plt.ylabel("RSME")
    plt.xlabel("Periods")
    plt.title("Root Mean Squared Error vs. Periods")
    plt.plot(training_rmse, label="training")
    plt.plot(validation_rmse, label="validation")
    plt.legend()
    
    return linear_regressor

with tf.Session() as sess:  
    sess.run(train_linear_regressor_model(learning_rate=0.002, steps=1, batch_size=1, 
                                                training_examples=training_examples, training_targets=training_targets,
                                                validation_examples=validation_examples, validation_targets=validation_targets))
#hyperparameters    .002   500    50  
    linear_regressor = train_linear_regressor_model(learning_rate=0.002, steps=1, batch_size=1, 
                                                training_examples=training_examples, training_targets=training_targets,
                                                validation_examples=validation_examples, validation_targets=validation_targets)        
    
    
    meta_graph_def = tf.train.write_graph(sess.graph, 'C:/Users/User', "Training_Meta_Graph.txt")
    sess.run(meta_graph_def)
    sess.close()
   
