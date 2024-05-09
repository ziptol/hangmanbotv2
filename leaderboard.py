import numpy as np

def getLeaderboard(filename):
    # pull leaderboard file
    leaderboard = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            leaderboard.append(line.split(" "))
    f.close()
    # format score - remove newline, change to int
    for entry in leaderboard:
        entry[1] = int(entry[1].replace("\n",""))
    return leaderboard

def setLeaderboard(filename, leaderboard):
    f = open(filename, "w")
    for entry in leaderboard:
        f.write(str(entry[0])+" "+str(entry[1])+"\n")
    f.close()

def incLeaderboard(filename, playername, score):
    # get current leaderboard
    leaderboard = getLeaderboard(filename)
    # find index of player
    try:
        # if player in list, increment their score
        pindex = [row[0] for row in leaderboard].index(playername)
        leaderboard[pindex][1] += score
        leaderboard = sortLeaderboard(leaderboard)
        setLeaderboard(filename, leaderboard)
        return True
    except:
        # if player not found, return add them to the leaderboard
        leaderboard.append([playername, score])
        leaderboard = sortLeaderboard(leaderboard)
        setLeaderboard(filename, leaderboard)
        return False

def clearLeaderboard(filename):
    open(filename, "w").close()

def sortLeaderboard(leaderboard):
    return sorted(leaderboard, key=lambda x: x[1], reverse=True)