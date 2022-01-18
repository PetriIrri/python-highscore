import json

def readCSV(path, sep):
    # initialize list to which to save the contents of the file
    output = []
    file = open(path, "r", encoding="utf-8")
    # start reading the file
    for row in file:
        player = row.strip().split(sep)
        if player != "":
            # if row is not empty save the row to the output list as a dictionary
            output.append({"name": player[0], "score": int(player[1])})
    file.close()
    # return the dictionaries
    return output

def writeCSV(path, inputCSV):
    # open file and write the given text
    file = open(path, "w", encoding="utf-8")
    file.write(inputCSV)
    file.close()

def checkTopTen(path, newScore, sep, MAX):
    # get the current top ten
    players = readCSV(path, sep)
    # if there are already 10 or more players in the list compare the given score to the list
    if len(players) >= MAX:
        # save all the score in the list
        scores = []
        for player in players:
            score = player["score"]
            if score != "":
                # if row is not empty save the row to the score list
                scores.append(score)
        # check if the new score is bigger than the smallest score in the list
        if min(scores) < newScore:
            # players score was bigger than the smallest score in the list
            return True
        else:
            return False
    else:
        # there were not at least 10 entries in the list already.
        return True

def dictToJson(dictionary):
    # converts a dictionary or list of dictionaries to JSON
    jsonOutput = json.dumps(dictionary, indent = 2)
    return jsonOutput