# Imports required packages and functions
import pandas as pd
import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor as HGBR
from sklearn.preprocessing import LabelEncoder
import joblib
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.inspection import permutation_importance


def create_city_categories(challenge_df, submission_df):

    '''
    This function takes the challenge and submission df and creates a dictionary for adep and ades cities. 
    The cities are categorized to create less than 255 categories, so the column can be processed by the HGBR later on.
    For each country at least on category exists. All cities with a count less than a threshold in one country are assigned to the same category. 

    Input: challenge and submission dataframe
    Output: dictionary that maps adep & ades to categories
    '''

    all_flights = pd.concat([challenge_df, submission_df])
    all_flights = all_flights[['adep', 'ades', 'country_code_adep', 'country_code_ades']]

    all_flights = pd.melt(all_flights, id_vars=[], value_vars=['adep', 'ades', 'country_code_adep', 'country_code_ades'], var_name='Variable', 
                        value_name='Value')

    # Create separate DataFrames for countries and cities
    countries = all_flights[all_flights['Variable'].str.contains('country')]
    cities = all_flights[all_flights['Variable'].isin(['adep', 'ades'])]

    # Combine into a single DataFrame
    all_flights = pd.DataFrame({
        'Country': countries['Value'].values,
        'City': cities['Value'].values
    })
    city_counts_final = all_flights.groupby('Country')['City'].value_counts().reset_index(name='Count')

    # assign index number as category number
    city_counts_final['Category'] = city_counts_final.index

    # assign zero to marker column
    city_counts_final['Marker'] = 0

    # if count is smaller than threshold marker is set to 1
    city_thresh = 440
    city_counts_final.loc[city_counts_final['Count'] < city_thresh, 'Marker'] = 1

    country_list = city_counts_final['Country'].unique()


    for country in country_list:
        condition1 = city_counts_final['Country'] == country
        condition2 = city_counts_final['Marker'] == 1
        first_index = city_counts_final.loc[condition1 & condition2].first_valid_index()
        city_counts_final.loc[condition1 & condition2, 'Category'] = first_index

    category_mapping = city_counts_final.set_index('City')['Category'].astype(int).to_dict()

    return(category_mapping)


def data_manipulation(challenge_df,
                      submission_df):
    """
    Input: pandas dataframe of challenge and submission set
    Output: pandas dataframe with manipulated data for training and prediction
    """

    df1 = challenge_df.copy()
    df2 = submission_df.copy()

    # Import list of icao codes and mtow
    icao_list = pd.read_csv('icao_code-mtow.csv')
    df1 = df1.merge(icao_list, on='aircraft_type', how='left')
    df2 = df2.merge(icao_list, on='aircraft_type', how='left')

    # Create categories for adep and ades
    city_mapping = create_city_categories(df1, df2)

    # Add new category columns to both dfs
    df1['adep_cat'] = df1['adep'].map(city_mapping)
    df1['ades_cat'] = df1['ades'].map(city_mapping)
    df2['adep_cat'] = df2['adep'].map(city_mapping)
    df2['ades_cat'] = df1['ades'].map(city_mapping)

    # Import trajectory feature list
    traj_list = pd.read_csv("trajectory_features.csv")
    # flight_id,actual_offblock_time,arrival_time,calculated_flight_time,sum_vertical_rate_ascending,sum_vertical_rate_descending,average_altitude_cruising,total_duration_cruising,average_groundspeed_cruising,kpi
    traj_cols = ["flight_id", "sum_vertical_rate_ascending", "sum_vertical_rate_descending",
                 "average_altitude_cruising", "total_duration_cruising", "average_groundspeed_cruising", "kpi"]
    traj_list = traj_list[traj_cols]
    traj_list["kpi"].fillna(0, inplace=True)

    df1 = df1.merge(traj_list, on='flight_id', how='left')
    df2 = df2.merge(traj_list, on='flight_id', how='left')

    columns_to_encode = ['aircraft_type', 'wtc', 'airline', 'country_code_adep', 'country_code_ades', 'adep_cat', 'ades_cat']

    for col in columns_to_encode:
        # Combine datasets for current column
        combined_data = pd.concat([df1[col], df2[col]], axis=0)

        # Initialize LabelEncoder
        encoder = LabelEncoder()

        # Fit the encoder on the combined data
        encoder.fit(combined_data)

        # Transform original dataset
        df1[f"{col}_en"] = encoder.transform(df1[col]).astype(np.int32)
        df2[f"{col}_en"] = encoder.transform(df2[col]).astype(np.int32)

    for df in [df1, df2]:
        # Transform dates into datetime objects
        df['date'] = pd.to_datetime(df['date'])
        df['actual_offblock_time'] = pd.to_datetime(df['actual_offblock_time'])
        df['arrival_time'] = pd.to_datetime(df['arrival_time'])
        df['weekday'] = df['date'].dt.weekday

        # Convert datetime to Unix time (seconds since the epoch)
        df['date_unix'] = df['date'].view('int64') // 10 ** 9
        df['arrival_time'] = df['arrival_time'].view('int64') // 10 ** 9

        # Transform date signals into periodical signals
        day = 24 * 60 * 60
        # week = 7 * day
        year = (365.2425) * day

        df['date sin'] = np.sin(df['date_unix'] * (2 * np.pi / day))
        df['year sin'] = np.sin(df['date_unix'] * (2 * np.pi / year))
        df["start_hour"] = df["actual_offblock_time"].dt.hour
        df['arrival day sin'] = np.sin(df['arrival_time'] * (2 * np.pi / day))
    return [df1, df2]


def train_tow_hgbr(challenge_df,
                   feature_cols,
                   model_path='hgbr_model.joblib', test=False, with_traj=False, permute=False):
    """
    Input: Challenge dataframe (flightlist only), path to save the model to
    Output: Trained ML model
    """

    if with_traj:
        challenge_df = challenge_df[challenge_df["kpi"] > 0]
        feature_cols.extend(["sum_vertical_rate_ascending", "sum_vertical_rate_descending", "average_altitude_cruising",
                             "total_duration_cruising", "average_groundspeed_cruising"])
        model_path = model_path.replace(".", "_with_traj.")
    else:
        # challenge_df = challenge_df[challenge_df["kpi"] == 0]
        pass

    # Define target column
    target_col = 'tow'

    X = challenge_df[feature_cols]
    y = challenge_df[target_col]

    # Create and fit the HistGradientBoostingRegressor model
    hgbr = HGBR(random_state=42,
                loss='squared_error',
                min_samples_leaf=16,
                max_depth=9,
                categorical_features=[0, 1, 2, 3, 4, 5, 11, 12],
                max_iter=2000,
                l2_regularization=0.1,
                learning_rate=0.078)

    # If this is a test run (Test = True) implement a train test split
    if test:
        # Train test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train model on training data
        hgbr.fit(X_train, y_train)

        if permute:
            # Optionally: Check feature importance
            result = permutation_importance(hgbr, X_test, y_test, n_repeats=10, random_state=42)
            for i in result.importances_mean.argsort()[::-1]:
                print(f"{X.columns[i]}:{result.importances_mean[i]:.3f} +/- {result.importances_std[i]:.3f}")


        # Make predictions
        y_train_pred = hgbr.predict(X_train)
        y_test_pred = hgbr.predict(X_test)
        # Evaluate the model
        train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
        train_r2 = r2_score(y_train, y_train_pred)

        test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
        test_r2 = r2_score(y_test, y_test_pred)

        print(f"With trajectory data: {with_traj}")
        print("Train RMSE:", train_rmse)
        print("Train R^2:", train_r2)
        print("Test RMSE:", test_rmse)
        print("Test R^2:", test_r2)

        # Save the model to a file
        joblib.dump(hgbr, model_path)

    else:
        # Train model on wholw challenge set
        hgbr.fit(X, y)

        y_pred = hgbr.predict(X)
        rmse = np.sqrt(mean_squared_error(y, y_pred))
        print(f"The RMSE of the trained model is {rmse}")
        print(f"With trajectory data: {with_traj}")

        # Save the model to a file
        joblib.dump(hgbr, model_path)

    return hgbr


def predict_tow_hgbr(submission_df,
                     feature_cols,
                     model_path="hgbr_model.joblib",
                     submission_path="data/submission.csv",
                     with_traj=False):
    """
    Input: submission dataset, path to the saved model, path to save submission to
    Output: sumbmission with predicted tow
    """
    base_model = joblib.load(model_path)

    if with_traj:
        base_data = submission_df[submission_df["kpi"] == 0]
    else:
        base_data = submission_df

    X1 = base_data[feature_cols]

    y1 = base_model.predict(X1)

    base_data['tow'] = y1

    if with_traj:
        traj_model_path = model_path.replace(".", "_with_traj.")
        traj_model = joblib.load(traj_model_path)

        traj_cols = feature_cols + ["sum_vertical_rate_ascending", "sum_vertical_rate_descending",
                                    "average_altitude_cruising",
                                    "total_duration_cruising", "average_groundspeed_cruising"]
        traj_data = submission_df[submission_df["kpi"] != 0]

        X2 = traj_data[traj_cols]
        y2 = traj_model.predict(X2)
        traj_data['tow'] = y2

        result_df = pd.concat([base_data, traj_data]).sort_index()
    else:
        result_df = base_data

    result_df = result_df[["flight_id", "tow"]]

    # Save the predictions
    result_df.to_csv(submission_path, index=False)

    return result_df
