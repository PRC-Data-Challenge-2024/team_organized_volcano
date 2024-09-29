from collections import Counter
import pandas as pd 
import numpy as np
import ruptures as rpt


def calculate_kpi(flight_list, id, f):

    '''
    Calculates the percentage of available datapoints based on the actual flight time in the flight list.
    The KPI is defined as KPI = number of available datapoints (max one per second) / flight time in seconds
    '''

    f['timestamp'] = pd.to_datetime(f['timestamp']).dt.tz_localize(None)
    if flight_list.index.isin([id]).any():

        actual_offblock_time = flight_list.loc[int(id), "actual_offblock_time"]
        arrival_time = flight_list.loc[int(id), "arrival_time"]
        flight_time = flight_list.loc[int(id), "calculated_flight_time"]
        reduced_f = f[f["timestamp"] < arrival_time]
        reduced_f = reduced_f[reduced_f["timestamp"] > actual_offblock_time]
        points_removed = len(f) - len(reduced_f)
        length_data = len(reduced_f["timestamp"].round("S").unique())

    else:
        return()
        
    kpi = length_data / flight_time

    if kpi > 1:
        seconds = Counter(reduced_f["timestamp"].round("S"))
        print(f"Error in {id}")
    
    return(kpi)

def split_flight(df, threshold = 300, points = 800):
    '''
    This function finds two points in the trajectory based on the vertical rate to devide it in 3 phases:
    1. The ascending phase
    2. The cruising phase
    3. The descending phase
    It uses the breakpoint detection from the ruptures package: https://centre-borelli.github.io/ruptures-docs/
    '''
    df.sort_values(['timestamp'], inplace = True)
    # find breakpoints
    df['vertical_rate_mod'] = np.where(np.abs(df['vertical_rate']) > threshold, 1000, 0)
    signal = df['vertical_rate_mod'].values
    # change point detection
    model = "l2"  # "l1", "rbf", "linear", "normal", "ar"
    algo = rpt.Binseg(model="l2").fit(signal)
    my_bkps = algo.predict(n_bkps=2)

    return(my_bkps, signal)

def cut_trajectory(df, column = 'altitude', thresh = 5):

    '''
    This function cuts constant parts at the start and end of each trajectory of more than 5 values using the altitude column. 
    '''
    
    # Get the values from the specified column
    col_values = df[column]

    def trim_constant_edges(list):
            # Find the start index where the column stops having the leading constant values
            start_val = list[0]
            start_idx = 0
            for i in range(1, len(list)):
                if list[i] != start_val:
                    start_idx = i
                    break
            
            # Find the end index where the column stops having trailing constant values
            end_val = list[-1]
            end_idx = len(list)
            for i in range(len(list)-2, -1, -1):
                if list[i] != end_val:
                    end_idx = i + 1
                    break
            
            # Return the trimmed DataFrame
            return (start_idx, end_idx)
    
    start = col_values.index[0]
    last_start = start -thresh -1
    end = col_values.index[-1]
    last_end = end + thresh + 1

    while((start - last_start > thresh) or (last_end - end > thresh)):

        # Define variables from last loop
        last_start = start
        last_end = end 

        col_values = col_values.loc[last_start:last_end]

        # Look for new edges to trim
        delta_start, delta_end = trim_constant_edges(col_values.values)

        start = last_start + delta_start 
        end = last_start + delta_end -1



    return(df.loc[start:end])