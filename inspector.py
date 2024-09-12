import pandas as pd

path_to_error = "data/trajectories/2022-04-03.parquet"

df = pd.read_parquet(path_to_error)
print(df)
print(df["flight_id"].unique())
print(set([int(b) for b in df["flight_id"].unique()]))
