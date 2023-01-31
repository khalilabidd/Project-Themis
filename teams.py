import pandas as pd
from itertools import combinations
from settings import *


def devideTeam(players):
    df = pd.read_csv(TEAMS_LEVEL_URL)
    df = df[df['DiscordId'].isin(players)]
    teams = list(combinations(df['DiscordId'].tolist(),4))[:35]
    dfTeams = pd.DataFrame(pd.Series(teams),columns=['Team1'])
    dfTeams['Team1'] = dfTeams['Team1'].apply(lambda x: list(x))
    dfTeams['pocket_diff'] = dfTeams.apply(lambda x: (df.Position[df['DiscordId'].isin(
        x['Team1'])]=='pocket').sum() - (df.Position[~df['DiscordId'].isin(
        x['Team1'])]=='pocket').sum(), axis=1)
    dfTeams['flank_diff'] = dfTeams.apply(lambda x: (df.Position[df['DiscordId'].isin(
        x['Team1'])]=='flank').sum() - (df.Position[~df['DiscordId'].isin(
        x['Team1'])]=='flank').sum(), axis=1)
    dfTeams['position_diff'] = abs(dfTeams['pocket_diff'] + dfTeams['flank_diff'])
    dfTeams['pocket_diff'] = dfTeams['pocket_diff'].apply(abs)
    dfTeams['flank_diff'] = dfTeams['flank_diff'].apply(abs)
    dfTeams['Level_1'] = dfTeams.apply(lambda x: sum(df.Level[df['DiscordId'].isin(
        x['Team1'])].values),axis=1)
    dfTeams['Level_2'] = dfTeams.apply(lambda x: sum(df.Level[~df['DiscordId'].isin(
        x['Team1'])].values),axis=1)
    dfTeams['Overall_diff'] = abs(dfTeams['Level_1'] - dfTeams['Level_2'])
    dfTeams.sort_values(['Overall_diff','position_diff','pocket_diff','flank_diff'],inplace=True)
    team1 = dfTeams['Team1'].iloc[0]
    team2 = df['DiscordId'][~df['DiscordId'].isin(team1)].tolist()
    return team1,team2