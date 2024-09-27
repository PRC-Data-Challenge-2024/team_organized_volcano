import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import os
from tqdm import tqdm
from pathlib import Path
from pyopensky.s3 import S3Client

import pickle

# Truncate trajectorie by cutting off everything before actual_offblock_time and after arrival_time
path_to_challenge = "data/challenge_set.csv"
path_to_submission = "data/submission_set.csv"
path_to_folder = "data/trajectories/"
path_to_truncated = "truncated_trajectories.pkl"

s3 = S3Client()
file_name = Path("data/challenge_set.csv")
if not file_name.exists():
    for obj in s3.s3client.list_objects("competition-data", recursive=True): # iterates over all objects in "competition-data"
        if not obj.object_name.endswith("parquet"): # as "competition-data" contains .parquet and .csv files, only the latter are downloaded
            s3.download_object(obj, filename=Path("data/" + obj.object_name)) # downloads object in "competition-data"

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
flight_list['calculated_flight_time'] = (flight_list['arrival_time'] - flight_list['actual_offblock_time']) / pd.Timedelta(seconds=1)

data_quality = {}
real, later = 0, 0
for this_file in tqdm(file_paths):
    raw_df = pd.read_parquet(this_file)
    flights = raw_df.groupby('flight_id')

    for id, f in flights:
        f['timestamp'] = pd.to_datetime(f['timestamp']).dt.tz_localize(None)
        try:
            actual_offblock_time = flight_list.loc[flight_list["flight_id"] == int(id), "actual_offblock_time"].values[0]
            arrival_time = flight_list.loc[flight_list["flight_id"] == int(id), "arrival_time"].values[0]
            flight_time = flight_list.loc[flight_list["flight_id"] == int(id), "calculated_flight_time"].values[0]
            reduced_f = f[f["timestamp"] < arrival_time]
            reduced_f = reduced_f[reduced_f["timestamp"] > actual_offblock_time]
            points_removed = len(f) - len(reduced_f)
            length_data = len(reduced_f["timestamp"].round("S").unique())
            real += 1
        except IndexError:
            later += 1
            continue

        kpi = length_data / flight_time

        if kpi > 1:
            seconds = Counter(reduced_f["timestamp"].round("S"))
            print(f"Error in {id}")

        # Take care of flights spanning more than a day - if data is already present in the dict then add the kpi on top

        if data_quality.get(id, None):
            data_quality[id] += kpi
        else:
            data_quality[id] = kpi


with open(path_to_truncated, "wb") as fh:
    pickle.dump([contains_train, contains_submission, contains_rest], fh)


print(data_quality)
print(f"We have {real} and missed {later} flights")
plt.hist(data_quality.values(), bins=20)
plt.show()
plt.savefig("trajectory_kpi.png")
