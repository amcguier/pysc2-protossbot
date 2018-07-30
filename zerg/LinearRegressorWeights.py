# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 15:41:48 2018

@author: vineethv
"""

import math
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn import metrics # machine learning lib, we will use for evaluation metrics

# TensorFlow libs
import tensorflow as tf

tf.logging.set_verbosity(tf.logging.ERROR)

# Libs for displaying graphs
from IPython import display
from matplotlib import cm
#from matplotlib import gridspec
from matplotlib import pyplot as plt

training_data = pd.read_csv("", sep=",")

#subset the dataframe where pokemon win percent is not NaN. (remove the pokemon that did not battle)

my_feature = training_data.loc[:,['Nexus', 'Gateway', 'CC', 'StarGate', 'FleetBeacon', 'RoboticsFacility', 'RoboticsBay', 'TwilightCouncil', 'TemplarArchives', 'DarkShrine', 'PC']]

# tf features
#'Number', 'HP','Attack','Defense','Sp. Atk', 'Sp. Def', 'Speed'
nexus = tf.feature_column.numeric_column('Nexus')
gateway = tf.feature_column.numeric_column('Gateway')
cc = tf.feature_column.numeric_column('CC')
stargate = tf.feature_column.numeric_column('StarGate')
fleetbeacon = tf.feature_column.numeric_column('FleetBeacon')
roboticsfacility = tf.feature_column.numeric_column('RoboticsFacility')
roboticsbay = tf.feature_column.numeric_column('RoboticsBay')
twilightcouncil = tf.feature_column.numeric_column('TwilightCouncil')
templararchives = tf.feature_column.numeric_column('TemplarArchives')
darkshrine = tf.feature_column.numeric_column('DarkShrine')
pc = tf.feature_column.numeric_column('PC')

feature_columns=[nexus, gateway, cc, stargate, fleetbeacon, roboticsfacility, roboticsbay, twilightcouncil, templararchives, darkshrine, pc]


def my_input_fn(features, targets, batch_size=1, shuffle=True, num_epochs=None):
    """Trains a linear regression model of one feature.
  
    Args:
      features: pandas DataFrame of features
      targets: pandas DataFrame of targets
      batch_size: Size of batches to be passed to the model
      shuffle: True or False. Whether to shuffle the data.
      num_epochs: Number of epochs for which data should be repeated. None = repeat indefinitely
    Returns:
      Tuple of (features, labels) for next data batch
    """
  
    # Convert pandas data into a dict of np arrays.
    features = {key:np.array(value) for key,value in dict(features).items()}                                           
 
    # Construct a dataset, and configure batching/repeating.
    ds = tf.data.Dataset.from_tensor_slices((features,targets)) # warning: 2GB limit
    ds = ds.batch(batch_size).repeat(num_epochs)
    
    # Shuffle the data, if specified.
    if shuffle:
      ds = ds.shuffle(buffer_size=10000)
    
    # Return the next batch of data.
    features, labels = ds.make_one_shot_iterator().get_next()
    return features, labels

def train_model(learning_rate, steps, batch_size, input_feature):
  """Trains a linear regression model of one feature.
  
  Args:
    learning_rate: A `float`, the learning rate.
    steps: A non-zero `int`, the total number of training steps. A training step
      consists of a forward and backward pass using a single batch.
    batch_size: A non-zero `int`, the batch size.
    input_feature: A `string` specifying a column from `pokemon_dataframe`
      to use as input feature.
  """
  
  periods = 10
  steps_per_period = steps / periods

  my_feature = input_feature
  my_feature_data = training_data[[my_feature]]
  my_label = "Win Percentage"
  targets = training_data[my_label]

  # Create feature columns.
  feature_columns = [tf.feature_column.numeric_column(my_feature)]
  
  # Create input functions.
  training_input_fn = lambda:my_input_fn(my_feature_data, targets, batch_size=batch_size)
  prediction_input_fn = lambda: my_input_fn(my_feature_data, targets, num_epochs=1, shuffle=False)
  
  # Create a linear regressor object.
  my_optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate)
  my_optimizer = tf.contrib.estimator.clip_gradients_by_norm(my_optimizer, 5.0)
  linear_regressor = tf.estimator.LinearRegressor(
      feature_columns=feature_columns,
      optimizer=my_optimizer
  )

  # Set up to plot the state of our model's line each period.
  plt.figure(figsize=(15, 6))
  plt.subplot(1, 2, 1)
  plt.title("Learned Line by Period")
  plt.ylabel(my_label)
  plt.xlabel(my_feature)
  sample = training_data.sample(n=300)
  plt.scatter(sample[my_feature], sample[my_label])
  colors = [cm.coolwarm(x) for x in np.linspace(-1, 1, periods)]

  # Train the model, but do so inside a loop so that we can periodically assess
  # loss metrics.
  print("Training model...")
  print("RMSE (on training data):")
  root_mean_squared_errors = []
  for period in range (0, periods):
    # Train the model, starting from the prior state.
    linear_regressor.train(
        input_fn=training_input_fn,
        steps=steps_per_period
    )
    # Take a break and compute predictions.
    predictions = linear_regressor.predict(input_fn=prediction_input_fn)
    predictions = np.array([item['predictions'][0] for item in predictions])
    
    # Compute loss.
    root_mean_squared_error = math.sqrt(
        metrics.mean_squared_error(predictions, targets))
    # Occasionally print the current loss.
    print("  period %02d : %0.2f" % (period, root_mean_squared_error))
    # Add the loss metrics from this period to our list.
    root_mean_squared_errors.append(root_mean_squared_error)
    # Finally, track the weights and biases over time.
    # Apply some math to ensure that the data and line are plotted neatly.
    y_extents = np.array([0, sample[my_label].max()])
    
    weight = linear_regressor.get_variable_value('linear/linear_model/%s/weights' % input_feature)[0]
    bias = linear_regressor.get_variable_value('linear/linear_model/bias_weights')

    x_extents = (y_extents - bias) / weight
    x_extents = np.maximum(np.minimum(x_extents,
                                      sample[my_feature].max()),
                           sample[my_feature].min())
    y_extents = weight * x_extents + bias
    plt.plot(x_extents, y_extents, color=colors[period]) 
  print("Model training finished.")
  print(input_feature)
  print("Weight:", weight)
  print("Bias:", bias)

  # Output a graph of loss metrics over periods.
  plt.subplot(1, 2, 2)
  plt.ylabel('RMSE')
  plt.xlabel('Periods')
  plt.title("Root Mean Squared Error vs. Periods")
  plt.tight_layout()
  plt.plot(root_mean_squared_errors)

  # Output a table with calibration data.
  calibration_data = pd.DataFrame()
  calibration_data["predictions"] = pd.Series(predictions)
  calibration_data["targets"] = pd.Series(np.array(targets))
  display.display(calibration_data.describe())

  print("Final RMSE (on training data): %0.2f" % root_mean_squared_error)
  
for input_feature in feature_columns:
    train_model(
    learning_rate=0.002,
    steps=15,
    batch_size=10,
    input_feature)