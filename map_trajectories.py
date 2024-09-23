# Use this to extract relevant data from the trajectories
# We have parquet files for every single day of the year, all locally available. Get the IDs from flightlist,
# open each parquet file, store 3 mappings
# 1. which parquet files contain training ids?
# 2. which parquet files contain submission ids?
# 3. which parquet files contain other ids?

import os
import dask.dataframe as dd
from tqdm import tqdm
import pickle

path_to_folder = "data/trajectories/"
path_to_train = "data/challenge_set.csv"
path_to_submission = "data/submission_set.csv"
path_to_mapping = "data/mapping.pkl"

ids_train = set(list(dd.read_csv(path_to_train)["flight_id"]))
ids_submission = set(list(dd.read_csv(path_to_submission)["flight_id"]))

file_names = [i for _, _, i in os.walk(path_to_folder)]
file_paths = [path_to_folder + k for k in file_names[0]]
contains_train, contains_submission, contains_rest, = [], [], []

for i, f in tqdm(enumerate(file_paths)):
    three = 0
    name = file_paths[i].split("/")[-1]
    df = dd.read_parquet(f, columns=["flight_id"])
    temp_ids = set([int(b) for b in df["flight_id"].unique().compute()])
    if len(ids_train.intersection(temp_ids)) > 0:
        contains_train.append(name)
        three += 1
    if len(ids_submission.intersection(temp_ids)) > 0:
        contains_submission.append(name)
        three += 1
    if len(temp_ids - ids_submission - ids_train) > 0:
        contains_rest.append(name)
        three += 1
    if three != 3:
        print(f"{name} does not contain all 3 types of ids!")

with open(path_to_mapping, "wb") as fh:
    pickle.dump([contains_train, contains_submission, contains_rest], fh)

print("Train")
print(len(contains_train))

print("Submission")
print(len(contains_submission))

print("Rest")
print(len(contains_rest))

# All ids are represented in all files
