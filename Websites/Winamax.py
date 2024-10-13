from dataclasses import dataclass
import requests
import json
import re
from Website import Website
from Bet import Bet

@dataclass
class Winamax(Website):

    def __init__(self, name, url):
        super(Winamax, self).__init__(name, url)

    def get_page_content(self):
        response = requests.get(self.url, headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"})
        html = response.text
        extract_json_re = re.compile('(?<=var PRELOADED_STATE = )(.*)(?=;</script><script type="text/javascript">)')
        json = re.search(extract_json_re, html).group(0)
        self.page_content = json

    def organise_content(self):
        json_formatted = json.loads(self.page_content)

        sports = json_formatted["sports"]
        matches = json_formatted["matches"]
        bets = json_formatted["bets"]
        outcomes = json_formatted["outcomes"]
        odds = json_formatted["odds"]

        for betid, bet in bets.items():
            ## exclude nonetype bets
            if bet is None:
                continue

            ## exclude alternative bets
            if bet["isAlternativeMainBet"] == "true":
                continue
            
            # Teams name
            match_id = bet["matchId"]
            title = matches[str(match_id)]["title"]
            team1, team2 = title.split(" - ")

            #sport name
            sport_id = matches[str(match_id)]["sportId"]
            sport_name = sports[str(sport_id)]["sportName"]

            # odds
            bet_odds = []
            bet_descriptions = []
            for outcome_id in bet["outcomes"]:
                bet_odds.append(odds[str(outcome_id)])
                bet_descriptions.append(outcomes[str(outcome_id)]["label"])

            # sport already created
            if sport_name in self.organised_page_content:
                self.organised_page_content[sport_name].append({"team1" : team1, "team2" : team2, "odds" : bet_odds, "odds_descriptions" : bet_descriptions})
            # sport not created
            else:
                self.organised_page_content[sport_name] = [{"team1" : team1, "team2" : team2, "odds" : bet_odds, "odds_descriptions" : bet_descriptions}]

    def organise_bets(self):
        super().organise_bets()

    