# Imports required packages and functions
from pyopensky.s3 import S3Client
from collections import Counter
import pandas as pd
import numpy as np
import os
# import plotly.express as px

print("Hello")

# Downloads the challenge_set.csv file containing the flightlist from the competition S3 bucket
s3 = S3Client()

if not os.path.exists("data/submission_set.csv"):
    for obj in s3.s3client.list_objects("competition-data", recursive=True): # iterates over all objects in "competition-data"
        if not obj.object_name.endswith("parquet"): # as "competition-data" contains .parquet and .csv files, only the latter are downloaded
            s3.download_object(obj) # downloads object in "competition-data"

challenge_df = pd.read_csv('data/challenge_set.csv')
submission_df = pd.read_csv('data/submission_set.csv')

print(submission_df.head())

submission_df["tow"] = 100000
submission_df = submission_df[["flight_id", "tow"]]
submission_df.to_csv("submission.csv", index=False)
