# PRC Data Challenge

Contribution of Malte Cordts, Sabrina Kerz, and Dennis Schorn to the [PRC Data Challenge 2024](https://ansperformance.eu/study/data-challenge/).

## Next Meeting
Monday, October 10 19:00 lcl (17:00 UTC)

## Current rankings

Available [here](https://datacomp.opensky-network.org/api/rankings)

<!--result-start-->
| Rank | Team Name | RMSE | File Version |
| ---- | --------- | ---- | ------------ |
| 1 | team_likable_jelly | 1573.65 | v12 |
| 2 | team_delightful_avocado | 2377.52 | v5 |
| 3 | team_brave_pillow | 2381.07 | v59 |
| 4 | team_tiny_rainbow | 2525.69 | v97 |
| 5 | team_honest_turtle | 2586.84 | v16 |
| 6 | team_mindful_donkey | 2683.05 | v9 |
| 7 | team_gentle_wreath | 2702.16 | v20 |
| 8 | team_amazing_forest | 2730.61 | v17 |
| 9 | team_diligent_igloo | 2790.44 | v11 |
| 10 | team_patient_net | 2850.31 | v4 |
| 11 | team_modest_scooter | 2880.63 | v4 |
| 12 | team_faithful_engine | 2965.47 | v1 |
| 13 | team_exuberant_hippo | 3036.23 | v7 |
| 14 | team_loyal_hippo | 3215.64 | v8 |
| 15 | team_zesty_ostrich | 3380.77 | v6 |
| 16 | team_exuberant_scooter | 3506.05 | v2 |
| 17 | team_energetic_quiver | 3683.31 | v15 |
| 18 | **team_organized_volcano** | 3755.47 | v9 |
| 19 | team_outspoken_engine | 4026.94 | v6 |
| 20 | team_respectful_kangaroo | 4052.19 | v5 |
| 21 | team_nice_hippo | 4263.82 | v7 |
| 22 | team_gentle_elephant | 4299.75 | v1 |
| 23 | team_amiable_garden | 4988.93 | v13 |
| 24 | team_elegant_lemon | 5184.86 | v18 |
| 25 | team_jolly_koala | 5771.74 | v5 |
| 26 | team_refreshing_unicorn | 6533.31 | v1 |
| 27 | team_zippy_river | 6839.35 | v11 |
| 28 | team_youthful_xerox | 9146.31 | v1 |
| 29 | team_versatile_yacht | 10207.85 | v10 |
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

Old: We have 474972 and missed 52191 flights

New: We have 464592 and missed 69525 flights


### Versions

Versions 0-6 were submitted for the early data, from 7 onwards we worked with the final data.
All trajectories were downloaded and processed after 8. New features from trajectories were extracted after 12

7. kpi > 0.8 traj_model, rest base_model on rest of data
8. kpi > 0.8 traj model, rest base_model on all data
9. all base_model
10. all base_model, sorted by index (makes no sense, don't ask)
11. kpi > 0.8 traj model, rest base_model on all data, sorted by index
12. traj model only on tow > 250t and kpi > 0.8, rest base
13. traj model with new trajectories traj model only on tow > 250t and kpi > 0.8, rest base

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

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](./LICENSE) file for details.
