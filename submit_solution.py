import json
import subprocess
import os
# manual submission:
# # mc cp data/submission.csv dc24/submissions/team_organized_volcano_v1_5963b2d2-8f7d-4132-b324-623f1564179f.csv


def submit_solution(version_number=-1):
    path_to_infos = "response_1723016820162.json"
    with open(path_to_infos) as fh:
        data = json.load(fh)

    team_id = data["team_id"]
    team_name = data["team_name"]
    sub_file = team_name + "_v" + str(version_number) + "_" + team_id + ".csv"

    # troubleshoot with f"&& mc alias list " \
    command = f"mc alias set dc24 https://s3.opensky-network.org/ ZG58zJvKhts2bkOX eU95azmBpK82kg96mE0TNzsWov3OvP2d " \
              f"&&  mc cp data/submission.csv dc24/submissions/{sub_file}"

    if not os.path.exists("data/submission.csv"):
        raise Exception("Submission file does not exist, please save the submission as "
                        "'data/submission.csv' into the data folder and try again :)")
    else:
        try:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            print(result.stdout)
            print(result.stderr)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e.stderr}")
            raise Exception("Submission not possible, did you set up minIO and are you on Windows?")
    return f"Successfully uploaded #new submission with version_number {version_number}"
