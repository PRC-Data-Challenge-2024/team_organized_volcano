# Full script that downloads the data, trains & saves the model, predicts on unseen data & submits to result
from pyopensky.s3 import S3Client
import pandas as pd
from pathlib import Path
from first_hgbr_model import train_tow_hgbr, predict_tow_hgbr, data_manipulation
from submit_solution import submit_solution
import warnings

# Set global feature cols for our model
feature_cols = ['country_code_adep_en', 'country_code_ades_en', 'aircraft_type_en', 'weekday', 'airline_en',
                    'wtc_en', 'year sin', 'arrival day sin',
                    'flight_duration', 'taxiout_time', 'flown_distance', 'start_hour', 'mtow_group']
"""[0, 1, 2, 3, 4, 5, 11, 12]"""
# Ignore Deprecations warnings
warnings.filterwarnings("ignore", category=FutureWarning)

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

# 2. Data manipulation
prepared_challenge_df, prepared_submission_df = data_manipulation(challenge_df, submission_df)

# 2. Train the model & save it to the default path
model = train_tow_hgbr(prepared_challenge_df, feature_cols=feature_cols, test = True)

# 3. Predict on the submission data (using default model path)
#result = predict_tow_hgbr(prepared_submission_df, feature_cols=feature_cols)

# 4. Submit the data (default path) with a new, manual version number
#msg = submit_solution(version_number=5)
#print(msg)
