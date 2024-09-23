import pandas as pd

#path_to_file = "data/trajectories/2022-04-03.parquet"
path_to_file = "data/trajectories/2022-12-30.parquet"

raw_df = pd.read_parquet(path_to_file)

id_set = set([int(b) for b in raw_df["flight_id"].unique()])

all = raw_df.groupby(["flight_id"])

error_dict, result_dict = {}, {}
for z in all:
    # tuple that contains tuple (id, ) and df
    this_id = z[0][0]
    this_df = z[1]
    cols = this_df.columns
    # Verify we have no unwanted nans (first 9 cols should not appear in this)
    columns_with_nans = this_df.columns[this_df.isnull().any()]
    nan_set = set(columns_with_nans.to_list())
    required_cols = set(cols.to_list()[:9])
    try:
        assert required_cols.isdisjoint(nan_set)

        # Check the num of nans in the wind and temp columns and make sure they are the same
        u_wind_nans = this_df['u_component_of_wind'].isnull().sum()
        v_wind_nans = this_df['v_component_of_wind'].isnull().sum()
        temp_nans = this_df['temperature'].isnull().sum()

        assert u_wind_nans == v_wind_nans == temp_nans != len(this_df)

        non_nan_len = len(this_df) - u_wind_nans

        # Get the average wind on the plane (sum u_wind / len), sum v_wind / len)
        wind_u = this_df["u_component_of_wind"].sum()/non_nan_len
        wind_v = this_df["v_component_of_wind"].sum()/non_nan_len

        # Get the average temperature (sum temp / len)
        temp = this_df["temperature"].sum()/non_nan_len

        print(f"Values: {wind_u}, {wind_v}, {temp}")
        result_dict[this_id] = {"wind_u": wind_u, "wind_v": wind_v, "temp": temp}

    except AssertionError:
        x = z[1]
        error_dict[this_id] = nan_set.intersection(required_cols)

print(f"Processed {len(all)} trajectories")
print(f"Errors: {len(error_dict)} \nIDs: {error_dict.keys()}\ncols: {error_dict.values()}")
print(f"Working trajectories: {len(result_dict)}")
