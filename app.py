import aiohttp
import asyncio
from fpl import FPL
from flask import Flask, render_template, url_for, request
import nest_asyncio
import itertools as it
nest_asyncio.apply()

app = Flask(__name__)

def getBestForm(defenders_score, mids_score, attackers_score):
    attackers_score.pop(0)
    for i in range(3):
        defenders_score.pop(0)
        mids_score.pop(0)
    
    defence, mid, attack = 3, 3, 1
    for i in range(3):
        values = [attackers_score[0] if len(attackers_score)>0 else 0,
                  mids_score[0] if len(mids_score)>0 else 0,
                  defenders_score[0] if len(defenders_score)>0 else 0]
        max_position = values.index(max(values))
        if max_position == 0:
            attackers_score.pop(0)
            attack += 1
        elif max_position == 1:
            mids_score.pop(0)
            mid += 1
        else:
            defenders_score.pop(0)
            defence +=1
            
    return defence*100 + mid*10 + attack    

def getDreamTeams(myTeamPlayers_sorted):
    
    dreamTeams = dict.fromkeys(['best', 541, 532, 523, 451, 442, 433, 352, 343])
    goalKeeper = []
    defenders = []
    defenders_scores = []
    mids = []
    mids_scores = []
    attackers = []
    attackers_scores = []
    for player in myTeamPlayers_sorted:
        if (len(goalKeeper) == 1) and (len(defenders) == 5) and (len(mids) == 5) and (len(attackers) == 3): break
        if (player['position']==1 and len(goalKeeper)<1): 
            goalKeeper.append(player)
        if (player['position']==2 and len(defenders)<5): 
            defenders.append(player)
            defenders_scores.append(player['total_points'])
        if (player['position']==3 and len(mids)<5): 
            mids.append(player)
            mids_scores.append(player['total_points'])
        if (player['position']==4 and len(attackers)<3): 
            attackers.append(player)
            attackers_scores.append(player['total_points'])
    
    dreamTeams[541] = [goalKeeper, defenders, mids[:4], attackers[:1]]
    dreamTeams[532] = [goalKeeper, defenders, mids[:3], attackers[:2]]
    dreamTeams[523] = [goalKeeper, defenders, mids[:2], attackers[:3]]
    dreamTeams[451] = [goalKeeper, defenders[:4], mids, attackers[:1]]
    dreamTeams[442] = [goalKeeper, defenders[:4], mids[:4], attackers[:2]]
    dreamTeams[433] = [goalKeeper, defenders[:4], mids[:3], attackers]
    dreamTeams[352] = [goalKeeper, defenders[:3], mids, attackers[:2]]
    dreamTeams[343] = [goalKeeper, defenders[:3], mids[:4], attackers]
    
    bestFormation = getBestForm(defenders_scores, mids_scores, attackers_scores)
    dreamTeams['best'] = dreamTeams[bestFormation]
    return dreamTeams
        

def processSelectionsByTeams(selectionByTeam, myTeamPlayers):
    for currentPlayer in myTeamPlayers:
        playerTeamID = currentPlayer["team_id"]
        currentTeamStats = selectionByTeam[playerTeamID]
        currentTeamStats['unique_players'] += 1
        currentTeamStats['points'] += currentPlayer['total_points']
        currentTeamStats['players_names'].append(currentPlayer['name'])

def processGameWeek(gameWeek, gameWeekPlayer, playerID, player, myTeamPlayers, overview, gwCapPicksTemp, gwCapWrapper):
    
    if playerID in playerId_to_index:
        myTeamCurrentPlayer = myTeamPlayers[playerId_to_index[playerID]]
    else:
        myTeamCurrentPlayer = {}
        myTeamCurrentPlayer['id'] = playerID
        myTeamCurrentPlayer["name"] = player['web_name']
        myTeamCurrentPlayer["team_id"] = player['team']
        myTeamCurrentPlayer["team"] = team_by_id[player['team']]
        myTeamCurrentPlayer["position"] = player['element_type']
        myTeamCurrentPlayer["photo"] = player['photo'][:-4]
        myTeamCurrentPlayer["bought_for"] = 0
        myTeamCurrentPlayer["total_points"] = 0
        myTeamCurrentPlayer["total_points_without_captaincy"] = 0
        myTeamCurrentPlayer["minutes"] = 0
        myTeamCurrentPlayer["goals_scored"] = 0
        myTeamCurrentPlayer["assists"] = 0
        myTeamCurrentPlayer["clean_sheets"] = 0
        myTeamCurrentPlayer["goals_conceded"] = 0
        myTeamCurrentPlayer["own_goals"] = 0
        myTeamCurrentPlayer["penalties_saved"] = 0
        myTeamCurrentPlayer["penalties_missed"] = 0
        myTeamCurrentPlayer["yellow_cards"] = 0
        myTeamCurrentPlayer["red_cards"] = 0
        myTeamCurrentPlayer["saves"] = 0
        myTeamCurrentPlayer["bonus"] = 0
        myTeamCurrentPlayer["VPM"] = 0

        myTeamCurrentPlayer["times_captain"] = 0
        myTeamCurrentPlayer["times_vice_captain"] = 0
        myTeamCurrentPlayer["gameweeks_in_team"] = 0
        myTeamCurrentPlayer["gameweeks_on_pitch"] = 0
        myTeamCurrentPlayer["gameweeks_best_player"] = 0
        
        playerId_to_index [playerID] = len(myTeamPlayers)
        myTeamPlayers.append(myTeamCurrentPlayer)
        overview['unique_players'] += 1

    myTeamCurrentPlayer["gameweeks_in_team"] += 1
    playerSummary = player['history']
    playerSummary = [p for p in playerSummary if p['round'] == gameWeek]
    if playerSummary:   
        gwCapPicksTemp[player['web_name']] = 0
        for p in playerSummary:
            myTeamCurrentPlayer["total_points"] += (p["total_points"] * gameWeekPlayer["multiplier"])
            if not myTeamCurrentPlayer["bought_for"]:
                myTeamCurrentPlayer["bought_for"] = p['value']/10
            gwCapPicksTemp[player['web_name']] += p["total_points"]
            if gameWeekPlayer["multiplier"]:
                myTeamCurrentPlayer["total_points_without_captaincy"] += p["total_points"]
                myTeamCurrentPlayer["minutes"] += p["minutes"]
                myTeamCurrentPlayer["goals_scored"] += p["goals_scored"]
                myTeamCurrentPlayer["assists"] += p["assists"]
                myTeamCurrentPlayer["clean_sheets"] += p["clean_sheets"]
                myTeamCurrentPlayer["goals_conceded"] += p["goals_conceded"]
                myTeamCurrentPlayer["own_goals"] += p["own_goals"]
                myTeamCurrentPlayer["penalties_saved"] += p["penalties_saved"]
                myTeamCurrentPlayer["penalties_missed"] += p["penalties_missed"]
                myTeamCurrentPlayer["yellow_cards"] += p["yellow_cards"]
                myTeamCurrentPlayer["red_cards"] += p["red_cards"]
                myTeamCurrentPlayer["saves"] += p["saves"]
                myTeamCurrentPlayer["bonus"] += p["bonus"]
                myTeamCurrentPlayer["gameweeks_on_pitch"] += 1

                overview['total_minutes'] += p["minutes"]
                overview['total_goals'] += p["goals_scored"]
                overview['total_assists'] += p["assists"]
                overview['total_bonus'] += p["bonus"]
                if myTeamCurrentPlayer['position'] != 4:
                    overview['clean_sheets'] += p["clean_sheets"]

        if gameWeekPlayer["is_captain"]: myTeamCurrentPlayer["times_captain"] += 1
        if gameWeekPlayer["is_vice_captain"]: myTeamCurrentPlayer["times_vice_captain"] += 1
        if gameWeekPlayer["multiplier"] > gwCapWrapper[1] :
            gwCapWrapper[1] = gameWeekPlayer["multiplier"]
            gwCapWrapper[0] = myTeamCurrentPlayer['name']
    
    if player['web_name'] in gwCapPicksTemp:
        return gwCapPicksTemp[player['web_name']]
    else: return 0

        
        
async def main(teamID):
    async with aiohttp.ClientSession() as session:
        global team_by_id
        global playerId_to_index
        
        fpl = FPL(session)
        
        overview = {}
        overview['name'] = ""
        overview['team_name'] = ""
        overview['total_points'] = 0
        overview['overall_rank'] = 0
        overview['unique_players'] = 0
        overview['total_minutes'] = 0
        overview['total_goals'] = 0
        overview['total_assists'] = 0
        overview['clean_sheets'] = 0
        overview['total_bonus'] = 0
        
        if 'playerId_to_index' not in globals(): playerId_to_index = {}
        if 'team_by_id' not in globals(): team_by_id = {}
        team_by_id = { 1: "Arsenal",
                       2: "Aston Villa",
                       3: "Bournemouth",
                       4: "Brighton",
                       5: "Burnley",
                       6: "Chelsea",
                       7: "Crystal Palace",
                       8: "Everton",
                       9: "Leicester",
                       10: "Liverpool",
                       11: "Man City",
                       12: "Man Utd",
                       13: "Newcastle",
                       14: "Norwich",
                       15: "Sheffield",
                       16: "Southampton",
                       17: "Spurs",
                       18: "Watford",
                       19: "West Ham",
                       20: "Wolves"}
        
        playersCash = {}
        myTeamPlayers = []
        selectionByTeam = {}
        captainPicks = {}
        for i in range(1,21):
            tempDict = {}
            tempDict['team_name'] = team_by_id[i]
            tempDict['unique_players'] = 0
            tempDict['players_names'] = []
            tempDict['points'] = 0
            selectionByTeam[i] = tempDict
        
        user = await fpl.get_user(teamID)
        overview['total_points'] = user.summary_overall_points
        overview['overall_rank'] = user.summary_overall_rank
        overview['name'] = user.player_first_name + ' ' + user.player_last_name
        overview['team_name'] = user.name
        
        userGWsPicks = await user.get_picks()
        
        for i in it.chain(range(1,30), range(39,len(userGWsPicks)+1)):
            gwCapPicksTemp = {}
            gwCapPicks = {}
            gwCaptain = ""
            gwMultiplier = 0
            gwCapWrapper = [gwCaptain, gwMultiplier]

            gwTopPlayerId = -1
            gwTopPlayerScore = 0
            for gameWeekPlayer in userGWsPicks[i]:      
                playerID = gameWeekPlayer['element']
                if playerID in playersCash:
                    player = playersCash[playerID]
                else:
                    player = await fpl.get_player(playerID, include_summary=True, return_json=True)
                    playersCash[playerID] = player
                playerGwScore = processGameWeek(i, gameWeekPlayer, playerID, player, myTeamPlayers,
                 overview, gwCapPicksTemp, gwCapWrapper)
                if playerGwScore > gwTopPlayerScore:
                    gwTopPlayerId = playerID
                    gwTopPlayerScore = playerGwScore

            myTeamPlayers[playerId_to_index[gwTopPlayerId]]['gameweeks_best_player'] += 1
            gwTopPlayer = max(gwCapPicksTemp, key=gwCapPicksTemp.get)
            gwTopPoints = max(gwCapPicksTemp.values())
            gwCapPicks['captain'] = gwCapWrapper[0]
            gwCapPicks['captain_score'] = gwCapPicksTemp[gwCapWrapper[0]] * gwCapWrapper[1]
            gwCapPicks['captain_score_without'] = gwCapPicksTemp[gwCapWrapper[0]]
            gwCapPicks['top_player'] = gwTopPlayer
            gwCapPicks['top_player_score'] = gwTopPoints
            gwCapPicks['potential_lost'] = gwCapPicks['top_player_score'] * gwCapWrapper[1] - gwCapPicks['captain_score']
            captainPicks[i] = gwCapPicks
            
        processSelectionsByTeams(selectionByTeam, myTeamPlayers)
        selectionByTeam_sorted_left = {}
        selectionByTeam_sorted_right = {}
        for s in sorted(selectionByTeam.items(), key=lambda k_v: k_v[1]['points'], reverse = True):
            if len(selectionByTeam_sorted_left)<10:
                selectionByTeam_sorted_left[s[0]] = s[1]
            else: selectionByTeam_sorted_right[s[0]] = s[1]
        
        myTeamPlayers_sorted = []
        topVPM = 0
        topVPMPlayer = {}
        mostCaptained = 0
        mostCaptainedPlayer = {}
        for index,s in enumerate(sorted(myTeamPlayers, key=lambda i:i['total_points'], reverse = True)):
            myTeamPlayers_sorted.append(s)
            myTeamPlayers_sorted[index]['VPM'] = s['total_points'] / s['bought_for']
            if myTeamPlayers_sorted[index]['VPM'] > topVPM:
                topVPMPlayer = s
                topVPM = myTeamPlayers_sorted[index]['VPM']
            myTeamPlayers_sorted[index]['VPM'] = str("%.2f" %myTeamPlayers_sorted[index]['VPM'])
            if myTeamPlayers_sorted[index]['times_captain'] > mostCaptained:
                mostCaptainedPlayer = s
                mostCaptained = myTeamPlayers_sorted[index]['times_captain']

        playerId_to_index = {} #reseting the playerID dictionary

        return overview, myTeamPlayers_sorted, topVPMPlayer, mostCaptainedPlayer, selectionByTeam_sorted_left, selectionByTeam_sorted_right, captainPicks

@app.route('/', methods=['GET'])
def login():
    return render_template('Login.html', error=0)

@app.route('/main', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        teamID = request.form['content']
        try:
            overview, myTeamPlayers_sorted, topVPMPlayer, mostCaptainedPlayer, selectionByTeam_sorted_left, selectionByTeam_sorted_right, captainPicks = asyncio.run(main(teamID))
        except:
            return render_template('Login.html', error=1)
        else:
            dreamTeams = getDreamTeams(myTeamPlayers_sorted)
            return render_template('index.html', overview=overview, myTeamPlayers_sorted=myTeamPlayers_sorted,
            topVPMPlayer=topVPMPlayer, mostCaptainedPlayer=mostCaptainedPlayer, dreamTeams=dreamTeams, 
            selectionByTeam_sorted_left = selectionByTeam_sorted_left, selectionByTeam_sorted_right = selectionByTeam_sorted_right, captainPicks=captainPicks)
    else:
        return render_template('index.html', overview={} , myTeamPlayers_sorted=[None], topVPMPlayer={},
         mostCaptainedPlayer={}, dreamTeams={}, selectionByTeam_sorted_left={}, selectionByTeam_sorted_right={}, captainPicks={})

if __name__ == "__main__":
    app.run(debug=False)
