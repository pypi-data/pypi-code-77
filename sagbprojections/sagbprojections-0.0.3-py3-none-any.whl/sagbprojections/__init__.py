import pandas as pd

#Download latest data
statpath = 'https://raw.githubusercontent.com/BerkeleySportsAnalytics/sagb-site/master/dfs/inputs/statline.csv'
stats = pd.read_csv(statpath).drop(columns = 'Unnamed: 0')
dfspath = 'https://raw.githubusercontent.com/BerkeleySportsAnalytics/sagb-site/master/dfs/inputs/dfs.csv'
dfs = pd.read_csv(dfspath).drop(columns = 'Unnamed: 0')
draftkingspath = 'https://raw.githubusercontent.com/BerkeleySportsAnalytics/sagb-site/master/dfs/inputs/draftkings.csv'
dfk = pd.read_csv(draftkingspath).drop(columns = 'Unnamed: 0')
fanduelpath = 'https://raw.githubusercontent.com/BerkeleySportsAnalytics/sagb-site/master/dfs/inputs/fanduel.csv'
fanduel = pd.read_csv(fanduelpath).drop(columns = 'Unnamed: 0')

def getPlayerStats(name):
    """Get projected stats of specific player"""
    return stats[stats['Name'] == name]

def getTeamStats(team):
    """Get projected stats of all players from certain team"""
    return stats[stats['Team'] == team.upper()]

def scoresOver(fantasy, score):
    """Get players with scores over score based on DraftKings or FantasyDuel"""
    if fantasy.lower() == 'fanduel':
        return dfs[dfs['Projected Fanduel Points'] > score]
    elif fantasy.lower() == 'draftkings':
        return dfs[dfs['Projected Draftkings Points'] > score]
    else:
        assert False

def fanduelOptimal():
    """Get the fanduel optimal lineup"""
    return fanduel

def draftkingsOptimal():
    """Get the draftkings optimal lineup"""
    return dfk

def statsOver(stat, value):
    """Get players with stat values over value for a certain statistic
    (points, rebounds, assists, etc...)"""
    assert stat in ['Minutes', '2PT FG', '3PT FG', 'FTM', 'Rebounds', 'Assists', 'Blocks', 'Steals', 'Turnovers']
    return stats[stats[stat] > value]

def getInjured():
    """Get names and injury types for all injured players"""
    return stats[stats['Injury Indicator'] != ' ']['Name']

def getAllStats():
    """Get daily projections for all players"""
    return stats

def getAllProjections():
    """Get all projections from fanduel and draftkings"""
    return dfs

'''
def getHistorical():
    """Get Historical Prediction data for all players"""
    pass #Is this possible to implement?'''

if __name__ == "__main__": #Test API Functions
    #print(getPlayerStats('James Harden'))
    #print(getTeamStats('BKN'))
    #print(statsOver('Rebounds', 10))
    #print(getAllProjections())
    print(scoresOver('fanduel', 40))
    print(scoresOver('draftkings', 40))
