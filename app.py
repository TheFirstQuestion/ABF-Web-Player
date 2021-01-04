from flask import Flask, render_template, redirect, url_for, request
from os import listdir
from os.path import isfile, join
import random
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

#################### Config ##########################
RECORDINGS_PATH = "static/recordings/"
DELIMITER = " -- "
######################################################

@app.route("/")
def main():
    global SONGS
    SONGS = getSongInfo()
    return render_template('index.html', songs=SONGS)

@app.route("/play")
def playPage():
    currSong = getSongByName(SONGS, request.args.get("song"))
    prevSong = getSongByNumber(SONGS, currSong.getOrder() - 1)
    nextSong = getSongByNumber(SONGS, currSong.getOrder() + 1)
    return render_template('play.html', song=currSong, prevSong=prevSong, nextSong=nextSong)

@app.route("/settings")
def settings():
    return render_template('settings.html')

@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='img/favicon.ico'), code=302)


####################### Helper Functions ################################
def getSongInfo():
    files = sorted([f for f in listdir(RECORDINGS_PATH) if isfile(join(RECORDINGS_PATH, f))])


    songs = []
    workingName = ""
    isNew = False
    count = 0

    for f in files:
        pieces = f.split(".")[0].split(DELIMITER)
        name = pieces[0]
        isNew = (name != workingName)
        if isNew:
            thisSong = Song(name=name, order=count)
            count = count + 1
        else:
            thisSong = songs[-1]

        if pieces[1] == "Band":
            if pieces[2].split(" (")[0] == "Field Drumz":
                thisSong.addFieldDrumz(f)
            elif pieces[2].split(" (")[0] == "Kit":
                thisSong.addKit(f)
            elif pieces[2].split(" (")[0] == "No Drumz":
                thisSong.addNoDrumz(f)
            else:
                print("Malformed filename (Band): " + f)
                continue
        elif pieces[1] == "Part":
            if pieces[2].split(" (")[0] == "Snare":
                thisSong.addSnarePart(f)
            elif pieces[2].split(" (")[0] == "Tom":
                thisSong.addTomPart(f)
            else:
                print("Malformed filename (Part): " + f)
                continue
        else:
            print("Malformed filename: " + f)
            continue

        if isNew:
            workingName = name
            songs.append(thisSong)

    # Shuffle songs, if applicable
    if (request.cookies.get('shuffle') == "true"):
        los = len(songs)
        indices = random.sample(list(range(0, los)), los)
        i = 0
        for s in songs:
            s.setOrder(indices[i])
            i = i + 1

    return songs

def getSongByName(songs, name):
    for s in songs:
        if s.getName() == name:
            return s
    return None

def getSongByNumber(songs, num):
    for s in songs:
        if s.getOrder() == num:
            return s
    return None

########################## Song Class Definition #############################
class Song:
    order = -1
    hasFieldDrumz = False
    hasKit = False
    hasNoDrumz = False
    hasTomPart = False
    hasSnarePart = False

    def __init__(self, name, order):
        self.name = name
        self.order = order

    def getName(self):
        return self.name

    def setOrder(self, num):
        self.order = num

    def getOrder(self):
        return self.order

    def addTomPart(self, path):
        self.hasTomPart = True
        self.pathToTomPart = RECORDINGS_PATH + path

    def addSnarePart(self, path):
        self.hasSnarePart = True
        self.pathToSnarePart = RECORDINGS_PATH + path

    def addFieldDrumz(self, path):
        self.hasFieldDrumz = True
        self.pathToFieldDrumz = RECORDINGS_PATH + path

    def addKit(self, path):
        self.hasKit = True
        self.pathToKit = RECORDINGS_PATH + path

    def addNoDrumz(self, path):
        self.hasNoDrumz = True
        self.pathToNoDrumz = RECORDINGS_PATH + path


if __name__ == "__main__":
    app.run(host='0.0.0.0')
