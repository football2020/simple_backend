import flask
from flask import request
import pandas as pd
import json
from flask import jsonify
import os

app = flask.Flask(__name__)
app.config["DEBUG"] = True

DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "data/sample-2019-clean.csv"))
data = pd.read_csv(DATA_PATH)


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/game_dates', methods=['GET'])
def game_dates():
    return jsonify(sorted(data["GameDate"].unique()))

@app.route('/games_on_date', methods=['POST'])
def games_on_date():
    game_date = request.json["game_date"]
    games = {}
    for idx, row in data.loc[data["GameDate"] == game_date][['GameId', 'OffenseTeam', "DefenseTeam"]].iterrows():
        games[row["GameId"]] = {
            "offense": row["OffenseTeam"],
            "defense": row["DefenseTeam"]
        }
    return jsonify(games)

@app.route('/plays_in_game', methods=['POST'])
def plays_in_game():
    game_id = int(request.json["game_id"])
    team = request.json["team"]
    drives = {}
    drive_id = 0
    last_team = ""
    for idx, row in data.loc[(data['GameId'] == game_id)].sort_values(['Quarter', 'Minute', 'Second'],
                                                                      ascending=[True, False, False]).iterrows():
        if row["OffenseTeam"] != last_team:
            last_team = row["OffenseTeam"]
            drive_id += 1
            drive_start_time = "Quarter: " + str(row["Quarter"]) + " Game Clock: " + str(row["Minute"]) + ":" + str(
                row["Second"])
            drives[drive_id] = {
                "drive_id": drive_id,
                "team": row["OffenseTeam"],
                "drive_start_time": drive_start_time,
                "play_details": [{
                    "play_id": idx,
                    "Quarter": row["Quarter"],
                    "Minute": row["Minute"],
                    "Second": row["Second"],
                    "Down": row["Down"],
                    "ToGo": row["ToGo"],
                    "YardLine": row["YardLine"],
                    "YardLineDirection": row["YardLineDirection"],
                    "play_type": row["PlayType"],
                    "Description": row["Description"],
                    "Yards": row["Yards"],
                    "IsIncomplete": row["IsIncomplete"],
                    "IsTouchdown": row["IsTouchdown"],
                    "IsSack": row["IsSack"],
                    "IsChallenge": row["IsChallenge"],
                    "IsChallengeReversed": row["IsChallengeReversed"],
                    "IsInterception": row["IsInterception"],
                    "IsFumble": row["IsFumble"],
                    "IsPenalty": row["IsPenalty"],
                    "IsTwoPointConversion": row["IsTwoPointConversion"],
                    "IsTwoPointConversionSuccessful": row["IsTwoPointConversionSuccessful"],
                    "IsPenalty": row["IsPenalty"],
                }]
            }
        else:
            drives[drive_id]["play_details"].append({
                "play_id": idx,
                "Quarter": row["Quarter"],
                "Minute": row["Minute"],
                "Second": row["Second"],
                "Down": row["Down"],
                "ToGo": row["ToGo"],
                "YardLine": row["YardLine"],
                "YardLineDirection": row["YardLineDirection"],
                "play_type": row["PlayType"],
                "Description": row["Description"],
                "Yards": row["Yards"],
                "IsIncomplete": row["IsIncomplete"],
                "IsTouchdown": row["IsTouchdown"],
                "IsSack": row["IsSack"],
                "IsChallenge": row["IsChallenge"],
                "IsChallengeReversed": row["IsChallengeReversed"],
                "IsInterception": row["IsInterception"],
                "IsFumble": row["IsFumble"],
                "IsPenalty": row["IsPenalty"],
                "IsTwoPointConversion": row["IsTwoPointConversion"],
                "IsTwoPointConversionSuccessful": row["IsTwoPointConversionSuccessful"],
                "IsPenalty": row["IsPenalty"],
            })
    team_drives = {}
    for key, value in drives.items():
        if value["team"] == team:
            team_drives[key] = drives[key]

    return jsonify(team_drives)


app.run()
