# PRC Data Challenge

Contribution of Malte Cordts, Sabrina Kerz, and Dennis Schorn to the [PRC Data Challenge 2024](https://ansperformance.eu/study/data-challenge/).

[Leaderboard](https://datacomp.opensky-network.org/results)

## Next Meeting
Sunday, September 8 17:00 lcl (15:00 UTC)

## Current rankings

<!--result-start-->
This will be replaced with the latest data.
<!--result-end-->

## KPIs 
### 1. Model (Flight List Based Model, Gradient Boost)
RMSE Train: 3617.819106712358 kg 

RMSE Test: 3989.357890082463 kg 

## Notebooks
[Initial Data Review](https://colab.research.google.com/drive/1WMxJp5L7vl9GBKhZzXFJeXjvI1MgSNON#scrollTo=p6q00gZ2aoNO) 

[Flight List Based Model](https://colab.research.google.com/drive/1h_4Kw_Kx4-c8agqgn95yTxK5HRhB2JIF)

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
