import json
import subprocess
import os
num = 1

path_to_infos = "response_1723016820162.json"
with open(path_to_infos) as fh:
    data = json.load(fh)

team_id = data["team_id"]
team_name = data["team_name"]
sub_file = team_name + "_v" + str(num) + "_" + team_id + ".csv"

command = f"mc alias set dc24 https://s3.opensky-network.org/ ZG58zJvKhts2bkOX eU95azmBpK82kg96mE0TNzsWov3OvP2d " \
          f"&& mc alias list " \
          f"&&  mc cp submission.csv dc24/submission/{sub_file}"

if not os.path.exists("submission.csv"):
    raise Exception("Submission file does not exist, please save the submission as "
                    "'submission.csv' into this folder and try again :)")
else:
    try:
        subprocess.run(command, shell=True, check=True)
    except:
        raise Exception("Submission not possible, did you set up minIO and are you on windows?")
