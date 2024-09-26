import numpy as np
import pandas as pd

# The plan is to have a script that processes all the trajectory data, and stores relevant features for our ML model
# locally. Each file contains all trajectories for a give day, so if flight took place at midnight,
# they will appear in two files. Since the whole set is around 170gb, we download overlapping files individually,
# extract what we want to use,
# and delete the original file.

# Try extracting ids from a parquet file without loading the whole file
import dask.dataframe as dd

# In order to determine overlape, we download a file, get its set of ids, downlaod the next file, get that set and see
# if there is an overlap. If there is we continue with the next file and so forth

from pyopensky.s3 import S3Client
from pathlib import Path

# Downloads the csv files containing the challenge_set(flightlist) from the competition S3 bucket
s3 = S3Client()
file_name = Path("data/challenge_set.csv")
old_ids, old_name = None, None
overlapper, sizes, current_size = 0, [], 0
this = False
for obj in s3.s3client.list_objects("competition-data", recursive=True): # iterates over all objects in "competition-data"
    print(obj.object_name)
    if obj.object_name.startswith("2022-03-01"):
        this = True
    if this:
        exit()
    if obj.object_name.endswith("parquet"): # as "competition-data" contains .parquet and .csv files, only the latter are downloaded
        # Download new file
        s3.download_object(obj, filename=Path("data/trajectories/" + obj.object_name)) # downloads object in "competition-data"
        """
        df = dd.read_parquet("data/trajectories/" + obj.object_name, columns=["flight_id"])
        try:
            id_set = set(df["flight_id"])
        except ValueError:
            df = df.compute()
            id_set = set(df["flight_id"])
        # If we have an old file, work on it and compare ids
        if old_ids and old_name:
            overlap = old_ids.intersection(id_set)
            if len(overlap) > 0:
                # There is overlap between the ids
                print(f"Overlap in {obj.object_name}: \n{overlap}")
                overlapper += 1
                current_size += 1
            else:
                # Process the old file, then delete it
                sizes.append(current_size)

        # Store the current file as old file
        old_ids, old_name = id_set, obj.object_name
        """