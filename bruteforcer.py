import itertools
from typing import OrderedDict

ReentryStats = {
    "Out": 300.5, # Star dance to first movement
    "Enter": 74, # Disappeared to first full white
    "In": 71, # First full white to first non-white
    "Exit": 56.5 # First idle frame to first walking
}

ReentrySplits = { # Normal is 48
    "BoB": 48,
    "BoB (DSG)": 49,
    "WF": 48,
    "JRB": 48,
    "CCM": 48,
    "HMC": 26,
    "LLL": 10,
    "SSL": 48,
    "DDD": 42,
    "DDD (Far)": 85,
    "SL": 48,
    "WDW": 48,
    "TTM": 61,
    "T2": 51, # (T2->TTM)
    "VCutM": 37, 
    "BitFS": 44
}

PauseExitSplits = { # Normal is 38
    "LLL": 38,
    "SSL": 38,
    "HMC": 38,
    "SL": 38,
    "WDW": 71,
    "TTM": 41, # This must be equal to the value below
    "T2": 41 # This must be equal to the value above
}

def reentryTime(course):
    if course == "BBH": return ReentryStats["Out"] + 213 + ReentryStats["In"]
    elif course == "VCutM": return ReentryStats["Out"] + ReentrySplits["VCutM"] + 34
    elif course == "BitFS": return 340 + ReentrySplits["BitFS"] + 40
    else: return ReentryStats["Out"] + ReentrySplits[course] + ReentryStats["Enter"] + ReentryStats["In"]

def pauseexitTime(course):
    if course == "VCutM": return ReentrySplits["VCutM"] + 34.5 + 38 + ReentryStats["Exit"]
    elif course == "BitFS": return ReentrySplits["BitFS"] + 40 + 38 + ReentryStats["Exit"]
    else: return ReentrySplits[course] + ReentryStats["Enter"] + ReentryStats["In"] + PauseExitSplits[course] + ReentryStats["Exit"]

DownTimes = {
    "WDW1": 50,
    "WDW2": 50,
    "WDW3": 50,
    "TTM": 112,
    "T2": 108,
    "SL": 80,
    "50": 117,
    "Down": 0, # Down->Down signifies 1 upstairs visit
}

WDWTimes = {
    "WDW1": ReentrySplits["WDW"],
    "WDW2": ReentrySplits["WDW"],
    "WDW3": ReentrySplits["WDW"],
    "TTM": 114,
    "T2": 112,
    "SL": 80,
    "50": 122,
    "Down": pauseexitTime("WDW"),
}

TTMTimes = {
    "WDW1": 111,
    "WDW2": 111,
    "WDW3": 111,
    "TTM": ReentrySplits["TTM"],
    "T2": 59,
    "SL": 82,
    "50": 170,
    "Down": pauseexitTime("TTM"),
}

T2Times = {
    "WDW1": 106,
    "WDW2": 106,
    "WDW3": 106,
    "TTM": ReentrySplits["T2"],
    "SL": 78,
    "50": 157,
    "Down": pauseexitTime("T2"),
}

SLTimes = {
    "WDW1": (74+138),
    "WDW2": (74+138),
    "WDW3": (74+138),
    "TTM": (78+138),
    "T2": (165+138),
    "SL": ReentrySplits["SL"],
    "50": (130+138),
    "Down": pauseexitTime("SL"),
}

PaintingToPainting = {
    "Down": DownTimes,
    "WDW1": WDWTimes,
    "WDW2": WDWTimes,
    "WDW3": WDWTimes,
    "TTM": TTMTimes,
    "T2": T2Times,
    "SL": SLTimes,
}

def upstairs(a,b):
    return PaintingToPainting[a][b]

def upstairs_result(text, textlist, numlist):
    print(text, min(numlist),textlist[numlist.index(min(list(numlist)))])

uplist = ["Down", "WDW1", "WDW2", "WDW3", "SL", "TTM", "T2"]
uplist2 = ["Down", "SL", "TTM", "T2"]
uplist3 = ["Down", "WDW1", "WDW2", "SL", "TTM", "T2"]
wdwlesstext = []
wdwlessnum = []
bestofalltext = []
bestofallnum = []
wdwrestext = []
wdwresnum = []
twovisittext = []
twovisitnum = []
twovisitwdwrestext = []
twovisitwdwresnum = []
twovisitwdwslrestext = []
twovisitwdwslresnum = []
twovisitslrestext = []
twovisitslresnum = []
twovisit2wdwtext = []
twovisit2wdwnum = []
twovisit2wdwslrestext = []
twovisit2wdwslresnum = []
twovisit3wdwtext = []
twovisit3wdwnum = []
twovisit3wdwslrestext = []
twovisit3wdwslresnum = []

def getUpstairsMovements():
    best = 99999
    for up in itertools.permutations(uplist2):
        time = upstairs("Down", up[0])
        for i in range(len(uplist2)-1):
            time += upstairs(up[i], up[i+1])
        time += upstairs(up[-1], "50")
        wdwlesstext.append(up)
        wdwlessnum.append(time)
        if time < best:
            best = time

    for up in itertools.permutations(uplist):
        time = upstairs("Down", up[0])
        for i in range(len(uplist)-1):
            time += upstairs(up[i], up[i+1])
        time += upstairs(up[-1], "50")
        if up[0] == "Down":
            bestofalltext.append(up)
            bestofallnum.append(time)
            if (up.index("WDW1")>up.index("TTM") or up.index("WDW2")>up.index("TTM") or up.index("WDW3")>up.index("TTM")):
                wdwrestext.append(up)
                wdwresnum.append(time)
        else:
            twovisittext.append(up)
            twovisitnum.append(time)
            if (up.index("WDW1")>up.index("TTM") or up.index("WDW2")>up.index("TTM") or up.index("WDW3")>up.index("TTM")):
                twovisitwdwrestext.append(up)
                twovisitwdwresnum.append(time)
                if up.index("SL")>up.index("Down"):
                    twovisitwdwslrestext.append(up)
                    twovisitwdwslresnum.append(time)
            if up.index("SL")>up.index("Down"):
                twovisitslrestext.append(up)
                twovisitslresnum.append(time)

            for up2 in itertools.permutations(["WDW1", "WDW2", "WDW3"]):
                if up.index(up2[2])-up.index(up2[1])>=2 and up.index(up2[1])-up.index(up2[0])>=2:
                    twovisit3wdwtext.append(up)
                    twovisit3wdwnum.append(time)
                    if up.index("SL")>up.index("Down"):
                        twovisit3wdwslrestext.append(up)
                        twovisit3wdwslresnum.append(time)

        if time < best: best = time

    for up in itertools.permutations(uplist3):
        if up[0] != "Down":
            time = upstairs("Down", up[0]) + upstairs("WDW2", "WDW3")
            for i in range(len(uplist3)-1):
                time += upstairs(up[i], up[i+1])
            time += upstairs(up[-1], "50")
            if up.index("WDW2")-up.index("WDW1")>=2 or up.index("WDW2")-up.index("WDW1")>=2:
                twovisit2wdwtext.append(up)
                twovisit2wdwnum.append(time)
                if up.index("SL")>up.index("Down"):
                    twovisit2wdwslrestext.append(up)
                    twovisit2wdwslresnum.append(time)
            if time < best: best = time

    upstairs_result("1 Visit (WDWless):", wdwlesstext, wdwlessnum)
    upstairs_result("Best 1 Visit:", bestofalltext, bestofallnum)
    upstairs_result("1 Visit (WDW Restricted):", wdwrestext, wdwresnum)
    upstairs_result("Best 2 Visit:", twovisittext, twovisitnum)
    upstairs_result("2 Visit (WDW Restricted):", twovisitwdwrestext, twovisitwdwresnum)
    upstairs_result("2 Visit (WDW&SL Restricted):", twovisitwdwslrestext, twovisitwdwslresnum)
    upstairs_result("2 Visit (SL Restricted):", twovisitslrestext, twovisitslresnum)
    upstairs_result("2 Visit (Double WDW Restricted):", twovisit2wdwtext, twovisit2wdwnum)
    upstairs_result("2 Visit (Double WDW&SL Restricted):", twovisit2wdwslrestext, twovisit2wdwslresnum)
    upstairs_result("2 Visit (Triple WDW Restricted):", twovisit3wdwtext, twovisit3wdwnum)
    upstairs_result("2 Visit (Triple WDW&SL Restricted):", twovisit3wdwslrestext, twovisit3wdwslresnum)

MovementTimes = {
    "0": 144, # up to upstairs (staircase)
    "A": 135, # BitFS to 30 star door
    "B": 178, # 30 star door to MIPS room door
    "C": 632, # MIPS room door to MIPS
    "D": 139.5, # MIPS to LLL
    "E": pauseexitTime("LLL"), # LLL reentry and pause exit
    "F": 153.5, # pause exit to up
    "G": pauseexitTime("BitFS"), # BitFS reentry and pause exit
    "H": 111, # pause exit to door to downstairs (="K")
    "I": 106.5, # door to downstairs to down key
    "J": 159, # down key to MIPS room door
    "K": 111, # TotWC exit to door to downstairs (="H")
    "L": pauseexitTime("SSL"), # SSL reentry and pause exit
    "M": pauseexitTime("HMC"), # HMC reentry and pause exit
    "O": 133, # MIPS to VCutM
    "Q": 131, # WF to JRB
    "R": 163, # JRB to BitDW
    "T": 192, # 30 star door to VCutM
    "U": 176, # JRB to up
    "V": 73.5, # TotWC exit to JRB (="3")
    "W": 64, # JRB to door to downstairs
    "X": 110, # WF to BitDW
    "Y": 138, # MIPS room door to LLL
    "Z": 552, # SSL to MIPS
    "1": 319, # HMC to VCutM
    "2": 243, # 2 JRB Detour
    "3": 73.5, # pause exit to JRB (="V")
}

# Shifting Sand Land

SSL = {
    "standtall": 66.83,
    "sslreds": 75.47,
}

# Hazy Maze Cave

HMC = {
    "metalcap": 56.23,
    "swimmingbeast": 17.40,
    "toxicmaze": 72.23,
    "HMC100": 173.00, # When paired with toxicmaze
    "metalhead": 66.00,  # Current is 70.10
}

# Jolly Roger Bay

JRB = {
    "sunkenship": 78.78,
    "eelplay": 43.80,
    "stonepillar": 25.50,
    "jrbreds": 74.46,
    "JRB100": 171.00,  # When paired with jetstream
    "jetstream": 53.87,
}

# Big Boo's Haunt
BBH = {
    "ghosthunt": 54.73,
    "hauntedbooks": 31.53, # 74.00 without ghost hunt precollected
    "bbhreds": 95.83,
    "BBH100": 146.00, # When paired with bbhreds. 160.00 without ghost hunt precollected. current is 173.05
}

# Dire Dire Docks

DDD = {
    "chests": 63.70,
    "bowsersub": 81.27,
    "mantaray": 35.68,
}

# Vanish Cap Under the Moat
VCutM = {
    "vanishcap": 44.77,
}

# Bowser in the Fire Sea
BitFS = {
    "bitfsreds": 165.00, # Over no reds
}

# Wet Dry World
WDW = {
    "arrowlifts": 13.80,
    "topoftown": 47.67,
    "express": 46.00,
    "quickrace": 61.37,
    "secrets": 74.10,
    "WDW100": 118.10, # When paired with secrets. Without HOLP is 130.00. Current is 158.53
}

# Tiny Huge Island
THI = {
    "pluckpiranha": 81.50,
}

# Tall Tall Mountain
TTM = {
    "scalemountain": 30.63,
    "monkeycage": 59.77,
    "breathtaking": 29.30,
    "lonelymushroom": 10.47, # Without HOLP is 17.60
    "mountainside": 9.13,
    "ttmreds": 49.00, # Current is 50.83
    "TTM100": 124.00, # When paired with ttmreds. Without HOLP is 131.00. Current is 133.42 with HOLP / 146.82 without HOLP
}

# Snowman's Land
SL = {
    "whirlpond": 15.60,
    "chillbully": 12.60,
    "deepfreeze": 12.07,
    "slreds": 38.67,
    "intoigloo": 32.95,
    "SL100": 70.00, # Current is 94.08
    "bighead": 59.27,
}

HOLPTimes = { # Relative timeloss with setup, relative timeloss without setup
    "WDW": [300, (30*(12+7+7))], # wdw secrets, ttm lonely mushroom, and ttm 100 timelosses
    "BitS": [2755, 0], # Arbitrarily large number given since no such HOLP setup exists yet
    "BitFS": [1372, 20]
}

def holpTime(course):
    if course == "WDW": return HOLPTimes["WDW"][0] + HOLPTimes["BitS"][1] + HOLPTimes["BitFS"][1]
    elif course == "BitS": return HOLPTimes["WDW"][1] + HOLPTimes["BitS"][0] + HOLPTimes["BitFS"][1]
    elif course == "BitFS": return HOLPTimes["WDW"][1] + HOLPTimes["BitS"][1] + HOLPTimes["BitFS"][0]

downlist = [
    [
        ["BitFS (MIPS restricted)", [0], [bestofallnum], "BitFS"],
        ["WDW (MIPS restricted)", [0], [wdwresnum], "WDW"],
        ["WDW", [1, 2, 3, 4, 5, 6, 7, 8, 9], [twovisitwdwresnum, 
            min(twovisitwdwresnum, twovisit2wdwnum, twovisit3wdwnum), 
            min(twovisitwdwslresnum, twovisit2wdwslresnum, twovisit3wdwslresnum), 
            min(twovisitwdwresnum, twovisit2wdwnum, twovisit3wdwnum),
            min(twovisitwdwresnum, twovisit2wdwnum, twovisit3wdwnum),
            min(twovisitwdwslresnum, twovisit2wdwslresnum, twovisit3wdwslresnum),
            min(twovisitwdwslresnum, twovisit2wdwslresnum, twovisit3wdwslresnum),
            min(twovisitwdwresnum, twovisit2wdwnum, twovisit3wdwnum),
            min(twovisitwdwresnum, twovisit2wdwnum, twovisit3wdwnum)], "WDW"],
        ["WDW (No DDD early)", [1, 2, 3], [twovisitwdwresnum, 
            min(twovisitwdwresnum, twovisit2wdwnum, twovisit3wdwnum), 
            min(twovisitwdwslresnum, twovisit2wdwslresnum, twovisit3wdwslresnum)], "WDW"],
        ["No Preset (MIPS restricted)", [0], [bestofallnum], "BitS"],
        ["No Preset", [2, 3, 4, 5, 6, 7, 8, 9], [min(twovisitnum, twovisit2wdwnum), 
            min(twovisitslresnum, twovisit2wdwslresnum), 
            min(twovisitnum, twovisit2wdwnum),
            min(twovisitnum, twovisit2wdwnum),
            min(twovisitslresnum, twovisit2wdwslresnum),
            min(twovisitslresnum, twovisit2wdwslresnum),
            min(twovisitnum, twovisit2wdwnum),
            min(twovisitnum, twovisit2wdwnum)], "BitS"],
        ["No Preset (No DDD early)", [2, 3], [min(twovisitnum, twovisit2wdwnum), 
            min(twovisitslresnum, twovisit2wdwslresnum), 
            min(twovisitnum, twovisit2wdwnum)], "BitS"]
    ],
    [
        ["Original", ["A", "B", "D", "E", "K", "W", "X", "Y", "Z", "1"]],
        ["Classic", ["0", "D", "E", "F", "G", "H", "I", "J", "K", "W", "X", "Y", "Z", "1"]],
        ["Why", ["0", "C", "D", "F", "G", "H", "I", "J", "K", "W", "X", "1", "L"], ],
        ["Late VC", ["0", "F", "G", "H", "I", "J", "K", "M", "O", "W", "X", "Y", "Z"]],
        ["2 JRB A", ["0", "A", "D", "H", "K", "M", "Q", "R", "T", "U", "Z", "2"]],
        ["2 JRB A1", ["0", "A", "D", "H", "M", "T", "U", "V", "W", "X", "Z", "2"]],
        ["2 JRB B", ["0", "D", "G", "H", "K", "Q", "R", "Z", "1", "U", "2"]],
        ["2 JRB B1", ["0", "D", "G", "H", "V", "W", "X", "Z", "1", "U", "2"]],
        ["2 JRB C", ["0", "A", "B", "C", "D", "F", "K", "L", "Q", "R", "W", "1", "2"]],
        ["2 JRB C1", ["0", "A", "B", "C", "D", "F", "L", "V", "W", "W", "X", "1", "2"]]
    ]
]
downlist2 = {}

def getDownstairsMovements():
    for i in range(len(downlist[0])):
        downlist2[downlist[0][i][0]] = {}
        for j in range(len(downlist[0][i][1])):
            sum = min(downlist[0][i][2][j]) + holpTime(downlist[0][i][3])
            for k in range(len(downlist[1][downlist[0][i][1][j]][1])):
                sum += MovementTimes[downlist[1][downlist[0][i][1][j]][1][k]]
            downlist2[downlist[0][i][0]][downlist[1][downlist[0][i][1][j]][0]] = sum
        print(downlist[0][i][0], downlist2[downlist[0][i][0]])

Stars = {
    "SSL": SSL,
    "HMC": HMC,
    "JRB": JRB,
    "BBH": BBH,
    "DDD": DDD,
    "VCutM": VCutM,
    "BitFS": BitFS,
    "WDW": WDW,
    "THI": THI,
    "TTM": TTM,
    "SL": SL,
}

# Alternate 100 Coin Pairing Times

Pairs = {
    "SSL": {},
    "HMC": {"toxicmaze": 0.00},
    "JRB": {"jrbreds": 14.00, "jetstream": 0.00},
    "BBH": {"bbhreds": 0.00},
    "DDD": {},
    "VCutM": {},
    "BitFS": {},
    "WDW": {"secrets": 0.00},
    "THI": {},
    "TTM": {"ttmreds": 0.00},
    "SL": {"slreds": 0.00}
}

Detours = {
    "SSL": 0.00,
    "BitFS": 0.00,
    "BBH": 31.00,
    "VCutM": (1233+ReentryStats["Out"]+pauseexitTime("VCutM")-pauseexitTime("HMC"))/30, # hmctovcutm+vcutmtojrb-hmctojrb
    "THI": 11.00+19.50-8.00 # rough estimates for wdwtothi+thitottm-wdwtottm
}

Arr = {} # Shorthand for "Star Arrangements"

def match(list1, list2):
    return_list = []
    for x in range(len(list1)):
        for y in range(0, len(list2)):
            if list1[x]==list2[y]:
                return_list.append(str(list1[x]))
    return return_list

def getStarArrangements(course):
    Arr[course] = {}
    starnames = list(Stars[course].keys())
    starvalues = list(Stars[course].values())
    pairnames = list(Pairs[course].keys())
    pairvalues = list(Pairs[course].values())
    for i in range(0, len(starnames)+1):
        best = 99999
        bestjs = 99999 # Used for jetstreamless
        bestig = 99999 # Used for intoiglooless
        bestuk = 99999 # Used for monkeycageless
        for arrangement in itertools.combinations(starnames, i):
            arrangepair = list(match(sorted(pairnames), arrangement))
            time = 0
            
            for j in range(i):
                time += starvalues[starnames.index(arrangement[j])]
            
            if i == 0: # Deals with course detours, and if a course we don't want to be skipped is skipped, arbitrary time is added
                        if course in list(Detours.keys()):
                            time += -1*Detours[course]
                        else: time += 99999
            
            if course == "BBH":
                if "ghosthunt" not in arrangement:
                    if "hauntedbooks" in arrangement: time += 33
                    if "bbhreds" in arrangement: time += 14
            if course == "DDD":
                if "bowsersub" not in arrangement: time += 99999 # Sub is a required star
                elif "mantaray" in arrangement: time += (ReentrySplits["DDD (Far)"]-ReentrySplits["DDD"])
                    # Now that we know sub is in, we can assume that if mantaray is in, there will be at least one reentry, and therefore
                    # one far reentry will replace one close reentry, hence the difference of the two being added to the time regardless
                    # of numbers of reentries present in the arrangement
            if course == "JRB":
                if "sunkenship" not in arrangement and ("eelplay" in arrangement or "jetstream" in arrangement): time += 99999 # Plunder is required to unlock the other two
            
            if str(course+"100") in arrangement: # All 100 coin stuff goes through here no matter what
                if len(match(pairnames, arrangement)) > 0:
                    time += (pairvalues[pairnames.index(arrangepair[0])] - starvalues[pairnames.index(arrangepair[0])]) # 100 coin star time adjustments
                    if i < 2: time += 0 # If 1 or 0 stars collected, no reentries
                    else: time += (i-2)*reentryTime(course)/60
                    if course == "JRB" and "jetstream" not in arrangement:
                        if time < bestjs: bestjs = time # Tracking jetstreamless routes
                    elif course == "SL" and "intoigloo" not in arrangement:
                        if time < bestig: bestig = time # Tracking intoiglooless routes
                    elif course == "TTM" and "monkeycage" not in arrangement:
                        if time < bestuk: bestuk = time
                    if time < best: best = time
            else:
                if i < 2: time += 0
                else: time += (i-1)*reentryTime(course)/60
                if time < best: best = time
            time = round(time, 2)
        Arr[course][i] = [best, arrangement]
        if course == "JRB": Arr[course][str(str(i)+"js")] = [bestjs, arrangement]
        if course == "SL": Arr[course][str(str(i)+"ig")] = [bestig, arrangement]
        if course == "TTM": Arr[course][str(str(i)+"uk")] = [bestuk, arrangement]
    print(Arr[course])

def getAllStarArrangements():
    for i in range(len(Stars)):
        getStarArrangements(list(Stars.keys())[i])
    
def getStarCombinations():
    for combin in itertools.product(Arr["SSL"], Arr["HMC"], Arr["JRB"], Arr["BBH"], Arr["DDD"], Arr["VCutM"], Arr["BitFS"], Arr["WDW"], Arr["THI"], Arr["TTM"], Arr["SL"]):
        print(combin)

if __name__ == "__main__":
    getAllStarArrangements()
    getStarCombinations()
else:
    getUpstairsMovements()
    print("")
    getDownstairsMovements()
    print("")