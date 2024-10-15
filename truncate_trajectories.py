import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import os
from tqdm import tqdm
from pathlib import Path
from pyopensky.s3 import S3Client
from analyse_trajectories import split_flight, calculate_kpi, cut_trajectory
import numpy as np
import pickle
import warnings
from time import time
from concurrent.futures import ThreadPoolExecutor, as_completed

warnings.filterwarnings("ignore")

# Truncate trajectorie by cutting off everything before actual_offblock_time and after arrival_time
path_to_challenge = "data/challenge_set.csv"
path_to_submission = "data/submission_set.csv"
path_to_folder = "data/trajectories/"
path_to_truncated = "truncated_trajectories.pkl"

s3 = S3Client()
file_name = Path("data/challenge_set.csv")
if not file_name.exists():
    for obj in s3.s3client.list_objects("competition-data",
                                        recursive=True):  # iterates over all objects in "competition-data"
        if not obj.object_name.endswith(
                "parquet"):  # as "competition-data" contains .parquet and .csv files, only the latter are downloaded
            s3.download_object(obj, filename=Path("data/" + obj.object_name))  # downloads object in "competition-data"

file_names = [i for _, _, i in os.walk(path_to_folder)]
file_paths = [path_to_folder + k for k in file_names[0]]
contains_train, contains_submission, contains_rest, = [], [], []

raw_df_challenge = pd.read_csv(path_to_challenge)
raw_df_submission = pd.read_csv(path_to_submission)

raw_df_challenge["source"] = "challenge"
raw_df_submission["source"] = "submission"

raw_flight_list = pd.concat([raw_df_submission, raw_df_challenge])

# We care about flight_id, actual_offblock_time, arrival_time
flight_list = raw_flight_list[["flight_id", "actual_offblock_time", "arrival_time"]]
flight_list['actual_offblock_time'] = pd.to_datetime(flight_list['actual_offblock_time']).dt.tz_localize(None)
flight_list['arrival_time'] = pd.to_datetime(flight_list['arrival_time']).dt.tz_localize(None)
flight_list['calculated_flight_time'] = (flight_list['arrival_time'] - flight_list[
    'actual_offblock_time']) / pd.Timedelta(seconds=1)

# Adding empty columns for the new calculated values
flight_list['sum_vertical_rate_ascending'] = None
flight_list['sum_vertical_rate_descending'] = None
flight_list['average_altitude_cruising'] = None
flight_list['total_duration_cruising'] = None
flight_list['average_groundspeed_cruising'] = None
flight_list['kpi'] = None

flight_list.set_index('flight_id', inplace=True)

# Function to process a single flight (within a file)
def process_flight(id, f):
    f.sort_values('timestamp', ignore_index=True, inplace=True)
    kpi = calculate_kpi(flight_list, id, f)

    if kpi and (kpi > thresh):
        filtered_f = cut_trajectory(f)
        bkps, signal = split_flight(filtered_f)

        # Create dfs for the single phases
        ascending_phase = filtered_f.loc[0:bkps[0]]
        cruising_phase = filtered_f.loc[bkps[0]:bkps[1]]
        descending_phase = filtered_f.loc[bkps[1]:]
        last_cr_idx = int(cruising_phase.index[-1])
        first_cr_idx = int(cruising_phase.index[0])

        # Gather calculated values
        flight_data = {
            'flight_id': id,
            'kpi': kpi,
            'sum_vertical_rate_ascending': sum(ascending_phase['vertical_rate'].dropna().values),
            'sum_vertical_rate_descending': sum(descending_phase['vertical_rate'].dropna().values),
            'average_altitude_cruising': np.mean(cruising_phase['altitude'].dropna().values),
            'total_duration_cruising': (cruising_phase.loc[last_cr_idx, 'timestamp'] -
                                        cruising_phase.loc[first_cr_idx, 'timestamp']) / pd.Timedelta(minutes=1),
            'average_groundspeed_cruising': np.mean(cruising_phase['groundspeed'].dropna().values)
        }
        return flight_data
    return None


# Function to process a single file with parallelization at the flight level
def process_file(raw_df):
    flights = raw_df.groupby('flight_id')
    local_updates = []

    # Parallelize the processing of individual flights
    with ThreadPoolExecutor() as flight_executor:
        futures = {flight_executor.submit(process_flight, id, f): id for id, f in flights}
        for future in as_completed(futures):
            result = future.result()
            if result:
                local_updates.append(result)

    return local_updates


# Define the threshold for the KPI for data quality
thresh = 0.8

"""flight_results = []
for this_file in tqdm(file_paths):
    raw_df = pd.read_parquet(this_file)
    flight_results.extend(process_file(raw_df))

print("Processed all flights, writing results...")

# Update flight_list with results after processing
for result in flight_results:
    flight_list.loc[result['flight_id'], 'kpi'] = result['kpi']
    flight_list.loc[result['flight_id'], 'sum_vertical_rate_ascending'] = result['sum_vertical_rate_ascending']
    flight_list.loc[result['flight_id'], 'sum_vertical_rate_descending'] = result['sum_vertical_rate_descending']
    flight_list.loc[result['flight_id'], 'average_altitude_cruising'] = result['average_altitude_cruising']
    flight_list.loc[result['flight_id'], 'total_duration_cruising'] = result['total_duration_cruising']
    flight_list.loc[result['flight_id'], 'average_groundspeed_cruising'] = result['average_groundspeed_cruising']
"""


for this_file in tqdm(file_paths):
    raw_df = pd.read_parquet(this_file)
    flights = raw_df.groupby('flight_id')

    i = 0

    for id, f in flights:
        f.sort_values('timestamp', ignore_index=True, inplace=True)
        kpi = calculate_kpi(flight_list, id, f)

        if kpi and (kpi > thresh):
            flight_list.loc[id, 'kpi'] = kpi
            try:
                filtered_f = cut_trajectory(f)
                bkps, signal = split_flight(filtered_f)

                # Create dfs for the single phases
                ascending_phase = filtered_f.loc[0:bkps[0]]
                cruising_phase = filtered_f.loc[bkps[0]:bkps[1]]
                descending_phase = filtered_f.loc[bkps[1]:]
                last_cr_idx = int(cruising_phase.index[-1])
                first_cr_idx = int(cruising_phase.index[0])

                # Calculate values to be used in the HGBR
                flight_list.loc[id, 'sum_vertical_rate_ascending'] = sum(ascending_phase['vertical_rate'].dropna().values)
                flight_list.loc[id, 'sum_vertical_rate_descending'] = sum(descending_phase['vertical_rate'].dropna().values)
                flight_list.loc[id, 'average_altitude_cruising'] = np.mean(cruising_phase['altitude'].dropna().values)
                flight_list.loc[id, 'total_duration_cruising'] = (cruising_phase.loc[last_cr_idx, 'timestamp'] -
                                                                  cruising_phase.loc[
                                                                      first_cr_idx, 'timestamp']) / pd.Timedelta(minutes=1)
                flight_list.loc[id, 'average_groundspeed_cruising'] = np.mean(cruising_phase['groundspeed'].dropna().values)
            except:
                print(f"Error in id {id}")
            i += 1

# Save DataFrame as CSV
flight_list.to_csv('trajectory_features.csv', index=True)

with open(path_to_truncated, "wb") as fh:
    pickle.dump([contains_train, contains_submission, contains_rest], fh)
