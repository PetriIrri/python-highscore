#!/usr/bin/python3

import cgi
import cgitb
import os

from config import *
import functions
import json
from customExceptions import *
# Poista tämä rivi, kun sovellus on valmis. Tuotantokäytössä emme halua koskaan paljastaa koodissa
# potentiaalisesti olevia bugeja.
cgitb.enable()

# Pisteet lähetetään sovellukselle JSON-muodossa. Tämä pitää kommunikoida sovellukselle.
print("Content-type: application/json\n\n")

# HTTP-metodin selvitys
cgi_method = os.environ["REQUEST_METHOD"]
# initialize errors. 0 means that no errors happened
error = {"error": 0, "message": ""}
if cgi_method == "POST":
    # save player score to file
    # first authenticate
    data = cgi.FieldStorage()
    try:
        user = data.getvalue("user", "")
        password = data.getvalue("password", "")
        # if password and username is empty raise error
        if user == "" or password == "":
            raise noLoginIdError()
        if verify_password(user, password):
            # Read the saved players from file. Creates a list of dictionaries
            # if file is not found raise error
            if not os.path.isfile(PATH):
                raise fileError()
            players = functions.readCSV(PATH, SEP)
            # Get the name and score from the POST reguest
            name = data.getvalue("name", "")
            score = data.getvalue("score", "")
            # raise error if name or score is empty
            if name == "" or score == "":
                raise playerError()
            # Save player if his score is in top ten
            if functions.checkTopTen(PATH, int(score), SEP, MAX):
                newPlayer = {"name": name, "score": int(score)}
                # add the new player to players list
                players.append(newPlayer)
                # sort the list according to player scores
                players.sort(key = lambda k: k["score"], reverse = True)
                # pop the last index if list length > 10. popped index is the player with the lowest score
                if len(players) > 10:
                    players.pop()
                outputCSV = ""
                for player in players:
                    outputCSV += player["name"] + SEP + str(player["score"]) + "\n"
                functions.writeCSV(PATH, outputCSV)
            else:
                # Players score was not in top ten. raise error
                raise scoreLowError()
        else:
            # The given password or username were not correct. raise error
            raise wrogPasswordError()
    except noLoginIdError:
        error["error"] = 1
        error["message"] = "Login credentials were not received"
    except wrogPasswordError:
        error["error"] = 2
        error["message"] = "Password or username not correct"
    except playerError:
        error["error"] = 3
        error["message"] = "Player name or score missing"
    except TypeError:
        error["error"] = 4
        error["message"] = "Score or another variable was not in correct format"
    except ValueError:
        error["error"] = 5
        error["message"] = "Score or another variable has illegal value"
    except fileError:
        error["error"] = 6
        error["message"] = "File was not found"
    except IOError:
        error["error"] = 7
        error["message"] = "File read/write error"
    except scoreLowError:
        error["error"] = 8
        error["message"] = "Player score too low. Player not saved"
    except Exception:
        error["error"] = 9
        error["message"] = "Unidentified error. Please submit bug report to the dev team"

    # print out the error message
    jsonOutput = functions.dictToJson(error)
    # print out the JSON
    print(jsonOutput)
else:
    # send scores to application
    players = []
    try:
        # Read the saved players from file. Creates a list of dictionaries
        # if file is not found raise error
        if not os.path.isfile(PATH):
            raise fileError()
        players = functions.readCSV(PATH, SEP)
        # add count parameter that tells how many values were found
        length = len(players)
        players.append({"count": len(players)})
        # Transform the dictionaries to JSON format
        
    except TypeError:
        error["error"] = 4
        error["message"] = "Score or another variable was not in correct format"
    except ValueError:
        error["error"] = 5
        error["message"] = "Score or another variable has illegal value"
    except fileError:
        error["error"] = 6
        error["message"] = "File was not found"
    except IOError:
        error["error"] = 7
        error["message"] = "File read/write error"
    except Exception:
        error["error"] = 9
        error["message"] = "Unidentified error. Please submit bug report to the dev team"
    # add error message to output
    players.append(error)
    jsonOutput = functions.dictToJson(players)
    # print out the JSON
    print(jsonOutput)
