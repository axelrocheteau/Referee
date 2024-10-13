from dataclasses import dataclass
import requests
import json
from Website import Website
from Bet import Bet


@dataclass
class PMU(Website):
    sport_list : list[str]

    def __init__(self, name, url):
        super(PMU, self).__init__(name, url)
        self.sport_list = [
            "football",
            "tennis",
            "basketball",
            "rugby",
            "baseball",
            "boxe",
            "football américain",
            "handball"
            "hockey sur glace"
            "mma"
            "volleyball"
        ]

    def get_page_content(self):
        ## request sports 
        response = requests.get(self.url, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
        self.page_content = response.text

 
    def organise_content(self):

        json_tree = json.loads(self.page_content)

        sports = []
        league_ids = []
        for sport in json_tree:
            # ignore random sports
            if sport["name"].lower() not in self.sport_list:
                continue

            sports.append({"id": sport["id"], "name": sport["name"]})
            league_ids.extend([(sport["name"], league["id"]) for category in sport["categories"] for league in category["leagues"] if league["matchCount"] >= 8])

        ## request all leagues
        for sport_name, league_id in league_ids:

            # load query
            url_league = f"https://sports.pmu.fr/sportsbook/rest/v2/matches/?marketGroup=online-desktop&leagueId={league_id}&ln=fr"
            response = requests.get(url_league, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
            json_league = json.loads(response.text)


            for match in json_league:
                #ignore match that do not have competitors
                if "competitors" not in match or "odds" not in match:
                    continue
                
                team1 = match["competitors"][0]["name"]
                team2 = match["competitors"][1]["name"]
                odds = []
                odds_descriptions = []

                for odd in match["odds"]:
                    if odd["name"] == "Double chance":
                        continue
                    
                    for outcome in odd["outcomes"]:
                        odds.append(outcome["oddValue"])
                        odds_descriptions.append(outcome["outcome"].replace('{$competitor1}', team1).replace('{$competitor2}', team2))

                # sport already created
                if sport_name in self.organised_page_content:
                    self.organised_page_content[sport_name].append({"team1" : team1, "team2" : team2, "odds" : odds, "odds_descriptions" : odds_descriptions})
                # sport not created
                else:
                    self.organised_page_content[sport_name] = [{"team1" : team1, "team2" : team2, "odds" : odds, "odds_descriptions" : odds_descriptions}]


    def organise_bets(self):
        super().organise_bets()

    