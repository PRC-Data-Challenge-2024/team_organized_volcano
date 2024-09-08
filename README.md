# PRC Data Challenge

Contribution of Malte Cordts, Sabrina Kerz, and Dennis Schorn to the [PRC Data Challenge 2024](https://ansperformance.eu/study/data-challenge/).

[Leaderboard](https://datacomp.opensky-network.org/results)

## Next Meeting
Sunday, September 8 17:00 lcl (15:00 UTC)

## Current rankings

Available [here](https://datacomp.opensky-network.org/api/rankings)

<!--result-start-->
| Rank | Team Name | RMSE | File Version |
| ---- | --------- | ---- | ------------ |
| 1 | team_likable_jelly | 3310.61 | v2 |
| 2 | team_faithful_napkin | 3438.97 | v2 |
| 3 | team_inventive_emu | 3471.06 | v3 |
| 4 | team_gentle_wreath | 3473.09 | v6 |
| 5 | team_tiny_rainbow | 3496.83 | v5 |
| 6 | **team_organized_volcano** | 3692.36 | v2 |
| 7 | team_strong_fossil | 4067.41 | v1 |
| 8 | team_affectionate_bridge | 4103.79 | v2 |
| 9 | team_genuine_emu | 4227.99 | v3 |
| 10 | team_zippy_river | 5962.65 | v1 |
| 11 | team_gentle_dragon | 5990.08 | v1 |
| 12 | team_sincere_quicksand | 10740.28 | v0 |
| 13 | team_energetic_quiver | 16265.46 | v3 |
| 14 | team_affectionate_whistle | 29015.24 | v0 |
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
- Then move to more complex models if neccessary, eventually ending up with a transformer
- Optimise for RMSE, since this is used in the final scoring of our submission
- 

## Current ToDos
- [ ] Extract landing weight from trajectories if possible (Dennis)
- [ ] Improve simple model & features (Sabrina)
- [ ] Create download & upload scripts (Malte)
