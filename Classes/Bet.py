from dataclasses import dataclass

@dataclass
class Bet:
    team1 : str
    team2 : str
    sport : str
    website_name : str
    odds : list[float]
    odds_description : list[str]

    def __init__(self, team1, team2, sport, website_name, odds, odds_description):
        self.team1 = team1
        self.team2 = team2
        self.sport = sport
        self.website_name = website_name
        self.odds = odds
        self.odds_description = odds_description