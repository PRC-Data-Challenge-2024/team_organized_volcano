# PRC Data Challenge

Contribution of Malte Cordts, Sabrina Kerz, and Dennis Schorn to the [PRC Data Challenge 2024](https://ansperformance.eu/study/data-challenge/) as <b> team_organized_volcano</b>.
This code falls under GNU GPLv3, see the license tab for the full license.

## Current rankings

Available [here](https://datacomp.opensky-network.org/api/rankings)

<!--result-start-->
| Rank | Team Name | RMSE | File Version |
| ---- | --------- | ---- | ------------ |
| 1 | team_likable_jelly | 1561.63 | v25 |
| 2 | team_tiny_rainbow | 2217.75 | v1 |
| 3 | team_gentle_elephant | 2252.89 | v11 |
| 4 | team_brave_pillow | 2270.06 | v101 |
| 5 | team_delightful_avocado | 2355.61 | v16 |
| 6 | team_youthful_xerox | 2386.53 | v8 |
| 7 | team_affectionate_bridge | 2456.7 | v6 |
| 8 | team_honest_turtle | 2479.56 | v46 |
| 9 | team_exuberant_scooter | 2587.5 | v7 |
| 10 | team_mindful_donkey | 2683.05 | v9 |
| 11 | team_diligent_igloo | 2692.37 | v16 |
| 12 | team_amazing_forest | 2695.6 | v18 |
| 13 | team_modest_scooter | 2696.67 | v6 |
| 14 | team_gentle_wreath | 2702.16 | v20 |
| 15 | team_elegant_lemon | 2746.3 | v26 |
| 16 | team_patient_net | 2752.72 | v10 |
| 17 | team_faithful_engine | 2784.52 | v5 |
| 18 | team_mellow_barn | 2859.32 | v14 |
| 19 | team_exuberant_hippo | 2932.55 | v8 |
| 20 | team_zealous_watermelon | 3024.17 | v1 |
| 21 | team_loyal_hippo | 3029.57 | v10 |
| 22 | team_zesty_ostrich | 3092.39 | v11 |
| 23 | team_jolly_koala | 3254.78 | v48 |
| 24 | team_bold_emu | 3286.56 | v3 |
| 25 | team_motivated_baker | 3409.82 | v1 |
| 26 | team_nice_wolf | 3595.25 | v3 |
| 27 | team_energetic_quiver | 3683.31 | v15 |
| 28 | **team_organized_volcano** | 3755.47 | v9 |
| 29 | team_faithful_napkin | 3810.9 | v0 |
| 30 | team_outspoken_engine | 3960.86 | v10 |
| 31 | team_respectful_kangaroo | 4052.19 | v5 |
| 32 | team_amiable_garden | 4097.9 | v17 |
| 33 | team_nice_hippo | 4263.82 | v7 |
| 34 | team_joyful_zeppelin | 4845.14 | v3 |
| 35 | team_refreshing_unicorn | 6533.31 | v1 |
| 36 | team_versatile_yacht | 6713.85 | v18 |
| 37 | team_zippy_river | 6839.35 | v11 |
| 38 | team_nice_jacket | 9660.8 | v5 |
| 39 | team_zippy_horse | 12261.94 | v2 |
| 40 | team_knowledgeable_jungle | 49479.86 | v6 |
| 41 | team_funny_yogurt | 51510.18 | v2 |
| 42 | team_dependable_gorilla | 95849.37 | v1 |
<!--result-end-->

## Our models

### base_model

The main model we used for most of the project, [HGBR](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.HistGradientBoostingRegressor.html). This was initially trained on features from the flight list. For this we also engineered the features that covered the timing of the flight ([Engineered Features](#Engineered Features)) After iteratively determining the most impactful features for the model (via sklearn's [permutation_importance](https://scikit-learn.org/stable/modules/generated/sklearn.inspection.permutation_importance.html)), we used it for all our submissions. 

### traj_model

The secondary model, another HGBR but with additional features that contained information from the trajectories. For this we first determined how many datapoints were missing per flight. This <b> KPI </b> is the percentage of available data, and we used it to distinguish high quality data (<b> KPI </b> > 0.8) from low quality data (<b> KPI </b> <= 0.8). Then we removed all repeating constant values at the start and end of each trajectory, since these appear to be artifacts in the data without meaningful information. Next we split each trajectory into 3 phases, the <i> ascending phase </i> during which the climb rate is positive, the <i> cruising phase </i> during which the climb rate is more or less constant, and the <i> descending phase </i> during which the aircraft has a negative climb rate. We then calculated additional values to feed into the model as more features:
- the sum of the vertical rate changes during <i> ascending </i> and <i> descending phase</i> each
- average altitude of the <i> cruising phase </i> 
- duration of the <i> cruising phase </i>
- average groundspeed during the <i> cruising phase </i>
- the <b> kpi </b>


## Notebooks
[Initial Data Review](https://colab.research.google.com/drive/1WMxJp5L7vl9GBKhZzXFJeXjvI1MgSNON#scrollTo=p6q00gZ2aoNO) 

[Flight List Based Model](https://colab.research.google.com/drive/1h_4Kw_Kx4-c8agqgn95yTxK5HRhB2JIF)

[Script for training and predicting the model](https://colab.research.google.com/drive/1mKO-b7YfdCXVuNLkEvr6OccVzr4FLsp0?usp=sharing)

## Documentation

[Flight List Based Model](https://docs.google.com/document/d/1--aCGaPIoykFuH6jPuZkSNKuL8PHXe96vltabt59e6Y/edit)

## Information
[Data Explanation](https://drive.google.com/file/d/1qJPLEoQPBFM8mL6tLpiV-vdHZd88V_wM/view?usp=drive_link) 

[Introduction Slides](https://drive.google.com/file/d/1aDVe83t2N_of7b_DXSE8yEuQ1MaV0RpH/view?usp=drive_link) 

## Goal
**We aim to hand in a solution before the final deadline!**

## Decisions & Plans
- We want to start with a simple model, using only the flight list
- Then iterate & improve it by adding handcrafted features
- Next include data from the actual trajectories, without temporal features
- Then move to more complex models if necessary, eventually ending up with a transformer
- Optimise for RMSE, since this is used in the final scoring of our submission

# Model Features Overview
## FightList
This table lists all the features in the flightlist and indicates whether each feature is used in the models.

### Raw Features
| Feature          | 1. HGBR Model |
| ---------------------------------------- | ------- |
| flight_id (unique ID)                    | ❌      |
| callsign (obfuscated callsign)           | ❌      |
| adep (Aerodrome of DEParture)            | ❌      |
| ades (Aerodrome of DEStination)          | ❌      |
| name_adep (ADEP airport name)            | ❌      |
| name_ades (ADES airport name)            | ❌      |
| country_code_adep (ADEP country code)    | ✅      |
| country_code_ades (ADES country code)    | ✅      |
| date (date of flight)                    | ❌      |
| actual_offblock_time (AOBT)              | ❌      |
| arrival_time (ARVT)                      | ❌      |
| aircraft_type (aircraft type code)       | ✅      |
| wtc (Wake Turbulence Category)           | ✅      |
| airline (Aircraft Operator code)         | ✅      |
| flight_duration (flight duration in mins)| ✅      |
| taxiout_time (taxi-out time in mins)     | ✅      |
| flown_distance (route length in nmi)     | ✅      |

### Engineered Features
| Feature                                  | 2. HGBR Model |
| ---------------------------------------- | ------- |
|weekday                                 | ✅      |
| year sin                                | ✅      |
| arrival day sin                         | ✅      |
| start_hour                              | ✅      |

## Trajectories

### Engineered Features
| Feature                                  | 3. HGBR Model |
| ---------------------------------------- | ------- |
|Average climb rate, 1st flight phase   | ✅      |
|Average climb rate, 3rd flight phase    | ✅     |
|Average altitude, 2nd flight phase    | ✅     |

### Versions

Since the trajectory data was updated during the project phase, we downloaded and processed the data multiple times. The first few versions (0-6) were testing different aspects of the model on the early data. 
From 7 onwards we worked with the final data (submission_set + final_submission_set).
All trajectories were re-downloaded and processed after version 8. New features from trajectories were extracted after version 12. The specific versions were 

7. kpi > 0.8 traj_model, rest base_model on rest of data
8. kpi > 0.8 traj model, rest base_model on all data
9. all base_model
10. all base_model, sorted by index (to test if the order of the data matters in the submission)
11. kpi > 0.8 traj model, rest base_model on all data, sorted by index
12. traj model only on tow > 250t and kpi > 0.8, rest base
13. traj model with new trajectories traj model only on tow > 250t and kpi > 0.8, rest base
14. traj model with custom weights that equal the kpi of each flight
15. traj model with new trajectories traj model only on tow > 250t and kpi > 0.0, rest base

### Our submissions
| File Version | RMSE    |
|--------------|---------|
| v6           | 9959.47 |
| v7           | 9950.77 |
| v8           | 10106.12|
| v9           | 3755.47 |
| v10          | 3755.47 |
| v11          | 10106.12|
| v12          | 4341.19 |
| v13          | 4023.11 |
| v14          | 4525.74 |
| v15          | 4446.98 |

Our models continued to display better RMSE for our train and test data, but the performance did not improve as expected on the actual submission set. 

We suspect part of the problem to be the actual distribution of the data. We found no flights over 250t in the data that we initially used for training our traj_model, while flights with over 250t appeared in the final_submission_set. Using the traj_model only on flights below a base_model prediction of 250t was tested (v12 and later) but the improvement form this was still smaller than just using the base_model.


For kpi=0 it looks like the traj_model does not overfit on our data: 

![overfit_test.png](overfit_test.png)

#### We were unable to fully determine why our models performed worse than expected on the final data set.

## Getting the code to run

Make sure mc client is set up as described on data challenge page, then run <b>train_and_submit.py</b>


## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](./LICENSE) file for details.
