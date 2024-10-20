from dataclasses import dataclass
from Classes.Bet import Bet

@dataclass
class Website:
    name: str
    url : str
    page_content : str
    organised_page_content : dict[str : list[dict[str : str|list[float]|list[str]]]]
    bets : list[Bet]

    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.page_content = ''
        self.organised_page_content = {}
        self.bets = []
    
    def get_page_content(self):
        pass

    def get_sport_content(self, sport):
        pass
    
    def organise_content(self):
        pass

    def organise_bets(self):
        for sport, matches in self.organised_page_content.items():
            for match in matches:
                self.bets.append(Bet(
                    match['team1'],
                    match['team2'],
                    sport,
                    self.name,
                    match['odds'],
                    match['odds_descriptions']
                    )
                )
    
    def place_bet(self, team1, team2, sport, odd, odd_description):
        pass

    def login(self):
        pass
