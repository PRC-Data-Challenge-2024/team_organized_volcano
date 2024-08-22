import json
import subprocess
import os
num = 0

path_to_infos = "response_1723016820162.json"
with open(path_to_infos) as fh:
    data = json.load(fh)

print(data)
team_id = data["team_id"]
team_name = data["team_name"]
sub_file = team_name + "_v" + num + "_" + team_id + ".csv"
command = f"mc cp submission.csv dc24/submission/{sub_file}"
if not os.path.exists(sub_file):
    raise Exception("Submission file does not exist, please save the submission as "
                    "'submission.csv' into this folder and try again :)")
else:
    try:
        subprocess.run(command, shell=True, check=True)
    except:
        raise Exception("Submission not possible, did you set up minIO and are you on windows?")
