import pandas as pd
from itertools import combinations
from settings import TEAMS_LEVEL_URL

def teamLevel(df, team):
    flanks = df.flank[df['DiscordId'].isin(team)].tolist()
    pockets = df.pocket[df['DiscordId'].isin(team)].tolist()
    if len(flanks)==4:
        scores = [
            flanks[0]+flanks[1]+pockets[2]+pockets[3],flanks[0]+flanks[2]+pockets[1]+pockets[3],
            flanks[0]+flanks[3]+pockets[1]+pockets[2],flanks[2]+flanks[3]+pockets[0]+pockets[1],
            flanks[1]+flanks[3]+pockets[0]+pockets[2],flanks[1]+flanks[2]+pockets[0]+pockets[3]
        ]
    elif len(flanks)==3:
        scores = [
            flanks[0]+flanks[1]+pockets[2],flanks[0]+flanks[2]+pockets[1],flanks[1]+flanks[2]+pockets[0]
        ]
    elif len(flanks)==2:
        scores = [
            flanks[0]+flanks[1]
        ]
    return max(scores)

def divideTeam(players):
    df = pd.read_csv(TEAMS_LEVEL_URL)
    df = df[df['DiscordId'].isin(players)]
    if len(players)==8:
        teams = list(combinations(df['DiscordId'].tolist(),4))[:35]
    elif len(players)==6:
         teams = list(combinations(df['DiscordId'].tolist(),3))[:10]
    if len(players)==4:
        teams = list(combinations(df['DiscordId'].tolist(),2))[:3]
    dfTeams = pd.DataFrame(pd.Series(teams),columns=['Team1'])
    dfTeams['Team1'] = dfTeams['Team1'].apply(lambda x: list(x))
    dfTeams['Team2'] = dfTeams['Team1'].apply(lambda x: df['DiscordId'][~df['DiscordId'].isin(x)].tolist())
    dfTeams['Level_1'] = dfTeams['Team1'].apply(lambda x: teamLevel(df,x))
    dfTeams['Level_2'] = dfTeams['Team2'].apply(lambda x: teamLevel(df,x))
    dfTeams['Overall_diff'] = abs(dfTeams['Level_1'] - dfTeams['Level_2'])
    dfTeams = dfTeams.sort_values(['Overall_diff'])
    team1 = dfTeams['Team1'].iloc[0]
    team2 = dfTeams['Team2'].iloc[0]
    return team1,team2