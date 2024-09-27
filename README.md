# PRC Data Challenge

Contribution of Malte Cordts, Sabrina Kerz, and Dennis Schorn to the [PRC Data Challenge 2024](https://ansperformance.eu/study/data-challenge/).

## Next Meeting
Monday, September 23 18:00 lcl (16:00 UTC)

## Current rankings

Available [here](https://datacomp.opensky-network.org/api/rankings)

<!--result-start-->
| Rank | Team Name | RMSE | File Version |
| ---- | --------- | ---- | ------------ |
| 1 | team_honest_turtle | 2593.61 | v10 |
| 2 | team_tiny_rainbow | 2854.15 | v44 |
| 3 | team_affectionate_bridge | 2857.86 | v3 |
| 4 | team_diligent_volcano | 2929.79 | v5 |
| 5 | team_honest_cactus | 2986.09 | v1 |
| 6 | team_amazing_forest | 3111.02 | v9 |
| 7 | team_faithful_engine | 3152.34 | v0 |
| 8 | team_youthful_xerox | 3276.25 | v6 |
| 9 | team_likable_jelly | 3310.61 | v2 |
| 10 | team_inventive_emu | 3326.31 | v5 |
| 11 | team_mindful_donkey | 3352.1 | v5 |
| 12 | team_brave_pillow | 3353.91 | v2 |
| 13 | team_mellow_barn | 3387.23 | v2 |
| 14 | team_gentle_wreath | 3427.16 | v7 |
| 15 | team_faithful_napkin | 3438.97 | v2 |
| 16 | **team_organized_volcano** | 3502.38 | v5 |
| 17 | team_quick_candle | 3887.9 | v9 |
| 18 | team_genuine_emu | 4042.14 | v4 |
| 19 | team_strong_fossil | 4067.41 | v1 |
| 20 | team_zippy_river | 4610.5 | v4 |
| 21 | team_respectful_kangaroo | 5043.08 | v1 |
| 22 | team_exuberant_scooter | 5438.55 | v0 |
| 23 | team_gentle_dragon | 5990.08 | v1 |
| 24 | team_zesty_ostrich | 6043.18 | v0 |
| 25 | team_sincere_quicksand | 10740.28 | v0 |
| 26 | team_energetic_quiver | 16265.46 | v3 |
| 27 | team_unbelievable_donkey | 19826.41 | v2 |
| 28 | team_affectionate_whistle | 29015.24 | v0 |
<!--result-end-->

## KPIs 
### 1. Model (Flight List Based Model, Gradient Boost)
RMSE Train: 3360.5953623984747 kg 

RMSE Test:3695.7355259853975 kg 

## Notebooks
[Initial Data Review](https://colab.research.google.com/drive/1WMxJp5L7vl9GBKhZzXFJeXjvI1MgSNON#scrollTo=p6q00gZ2aoNO) 

[Flight List Based Model](https://colab.research.google.com/drive/1h_4Kw_Kx4-c8agqgn95yTxK5HRhB2JIF)

[Script for training and predicting the model](https://colab.research.google.com/drive/1mKO-b7YfdCXVuNLkEvr6OccVzr4FLsp0?usp=sharing)

## Documentation

[Flight List Based Model](https://docs.google.com/document/d/1--aCGaPIoykFuH6jPuZkSNKuL8PHXe96vltabt59e6Y/edit)

## Information
[Data Explanation](https://drive.google.com/file/d/1qJPLEoQPBFM8mL6tLpiV-vdHZd88V_wM/view?usp=drive_link) 

[Introduction Slides](https://drive.google.com/file/d/1aDVe83t2N_of7b_DXSE8yEuQ1MaV0RpH/view?usp=drive_link) 

Command to set up an alias for the data location:

mc alias set dc24 https://s3.opensky-network.org/ ZG58zJvKhts2bkOX eU95azmBpK82kg96mE0TNzsWov3OvP2d

## Goal
**We aim to hand in a solution before the final deadline!**

## Decisions & Plans
- We want to start with a simple model, using only the flight list
- Then iterate & improve it by adding handcrafted features
- Next include data from the actual trajectories, without temporal features
- Then move to more complex models if necessary, eventually ending up with a transformer
- Optimise for RMSE, since this is used in the final scoring of our submission
- 

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
| Feature                                  | 1. HGBR Model |
| ---------------------------------------- | ------- |
|weekday                                 | ✅      |
| year sin                                | ✅      |
| arrival day sin                         | ✅      |
| start_hour                              | ✅      |

## Trajectories

### Engineered Features
| Feature                                  | 1. HGBR Model |
| ---------------------------------------- | ------- |
|Average climb rate, 1st flight phase   | ✅      |
|Average climb rate, 3rd flight phase    | ✅     |
|Average altitude, 2nd flight phase    | ✅     |


## Expected trajectories in final submission
We have 474972 and missed 52191 flights
We have 464592 and missed 69525 flights

