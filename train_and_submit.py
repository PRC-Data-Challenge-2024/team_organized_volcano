# Full script that downloads the data, trains & saves the model, predicts on unseen data & submits to result
from pyopensky.s3 import S3Client
import pandas as pd
from pathlib import Path
from first_hgbr_model import train_tow_hgbr, predict_tow_hgbr
from submit_solution import submit_solution

# 1. Downlaod the data
# Downloads the csv files containing the challenge_set(flightlist) from the competition S3 bucket
s3 = S3Client()
file_name = Path("data/challenge_set.csv")
if not file_name.exists():
    for obj in s3.s3client.list_objects("competition-data", recursive=True): # iterates over all objects in "competition-data"
        if not obj.object_name.endswith("parquet"): # as "competition-data" contains .parquet and .csv files, only the latter are downloaded
            s3.download_object(obj, filename=Path("data/" + obj.object_name)) # downloads object in "competition-data"

challenge_df = pd.read_csv('data/challenge_set.csv')
submission_df = pd.read_csv('data/submission_set.csv')

# 2. Train the model & save it to the default path
model = train_tow_hgbr(challenge_df)

# 3. Predict on the submission data (using default model path)
result = predict_tow_hgbr(submission_df)

# 4. Submit the data (default path) with a new, manual version number
msg = submit_solution(version_number=1)
print(msg)
