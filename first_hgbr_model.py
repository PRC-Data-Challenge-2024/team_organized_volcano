# Imports required packages and functions
from pyopensky.s3 import S3Client # used to download data from the S3 bucket
import pandas as pd
import numpy as np
import os
from sklearn.ensemble import HistGradientBoostingRegressor as HGBR
from sklearn.preprocessing import LabelEncoder
import joblib

def data_manipulation(df):

  '''
  Input: pandas dataframe of either challenge_set or submission set
  Output: pandas dataframe with manipulated data for training and prediction
  '''
  # Drop duplicate columns (information is already in the adep / ades columns)
  df.drop(columns = ['name_adep', 'country_code_adep','name_ades', 'country_code_ades' ] )

  # Encode categorical variables as new columns in the df
  callsign_encoder = LabelEncoder()
  df['callsign_en'] = callsign_encoder.fit_transform(df['callsign']).astype(np.int32)
  aircraft_encoder = LabelEncoder()
  df['aircraft_type_en'] = aircraft_encoder.fit_transform(df['aircraft_type']).astype(np.int32)
  wtc_encoder = LabelEncoder()
  df['wtc_en'] = wtc_encoder.fit_transform(df['wtc']).astype(np.int32)
  airline_encoder = LabelEncoder()
  df['airline_en'] = airline_encoder.fit_transform(df['airline']).astype(np.int32)

  # Transform dates into datetime objects
  df['date'] = pd.to_datetime(df['date'])
  df['actual_offblock_time'] = pd.to_datetime(df['actual_offblock_time'])
  df['arrival_time'] = pd.to_datetime(df['arrival_time'])
  df['weekday'] = df['date'].dt.weekday

  # Convert datetime to Unix time (seconds since the epoch)
  df['date_unix'] = df['date'].view('int64') // 10**9
  df['actual_offblock_time'] = df['actual_offblock_time'].view('int64') // 10**9
  df['arrival_time'] = df['arrival_time'].view('int64') // 10**9

  # Transform date signals into periodical signals

  day = 24*60*60
  week = 7*day
  year = (365.2425)*day

  df['date sin'] = np.sin(df['date_unix'] * (2 * np.pi / day))
  df['year sin'] = np.sin(df['date_unix'] * (2 * np.pi / year))

  return(df)


def train_tow_hgbr(challenge_df):
  '''
  Input: Challenge dataframe (flightlist only)
  Output: Trained ML model
  '''

  # Data manipulation
  challenge_df = data_manipulation(challenge_df)

  # Define feature and target column
  feature_cols = ['aircraft_type_en', 'weekday', 'airline_en', 'wtc_en', 'year sin', 'arrival day sin', 'flight_duration', 'taxiout_time', 'flown_distance']
  target_col = 'tow'

  # Assuming 'target_variable' is the name of your target variable column
  X = challenge_df[feature_cols]
  y = challenge_df[target_col]

  # Create and fit the HistGradientBoostingRegressor model

  hgbr = HGBR(random_state = 42,
              loss = 'squared_error',
              min_samples_leaf = 20,
              categorical_features=[0,1,2,3],
              max_iter = 2000,
              l2_regularization=0.2)
  hgbr.fit(X, y)

  # Save the model to a file
  joblib.dump(hgbr, 'hgbr_model.joblib')


def predict_tow_hgbr(model_path, submission_df):

  '''
  Input: path to the saved model, submission dataset
  Output: sumbmission with predicted tow
  '''

  model = joblib.load('hgbr_model.joblib')

  # Data manipulation
  submission_df = data_manipulation(submission_df)

  # Define feature and target column
  feature_cols = ['aircraft_type_en', 'weekday', 'airline_en', 'wtc_en', 'year sin', 'arrival day sin', 'flight_duration', 'taxiout_time', 'flown_distance']

  # Assuming 'target_variable' is the name of your target variable column
  X = df[feature_cols]

  # Predict the tow
  y = model.predict(X)

  df['tow'] = y
  df = df[["flight_id", "tow"]]

  return(df)