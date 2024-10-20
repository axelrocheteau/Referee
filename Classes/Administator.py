from dataclasses import dataclass
from Classes.Website import Website
from Classes.Best_bet import Best_bet
import numpy as np
import distance

@dataclass
class Administator:
    websites : list[Website]
    organised_sport_bet : dict[str : list[dict[str : str|list[float]|list[str]]]]
    best_bets : list[Best_bet]
    valuable_bets : list[Best_bet]



    def __init__(self, name_urls):
        self.organised_sport_bet = {}
        self.websites = []
        self.best_bets = []
        self.valuable_bets = []

        # initialise every website
        for name_url in name_urls:
            website = name_url["class"](name_url["name"], name_url["url"])
            website.get_page_content()
            website.organise_content()
            website.organise_bets()

            self.websites.append(website)

    # gather all bets in one dictionary
    def organise_sport_bet(self):
        self.organised_sport_bet = {}
        for website in self.websites:

            # for each sport assemble all bets from every website
            for sport, bets in website.organised_page_content.items():
                if sport in self.organised_sport_bet:
                    self.organised_sport_bet[sport].extend(bets)
                else:
                    self.organised_sport_bet[sport] = bets
    
    def create_best_bet(self, equals_bet, sport):
        
        # take odds from first website
        bet = equals_bet[0]
        websites = [bet["website"] for _ in range(len(bet["odds"]))]
        best_odds = bet["odds"]
        team1 = bet["team1"]
        team2 = bet["team2"]
        odds_descriptions = bet["odds_descriptions"]
        
        # find best odds
        for bet in equals_bet[1:]:
            # prendre la meilleure odd
            for i, (best_odd, odd) in enumerate(zip(best_odds, bet["odds"])):
                if odd > best_odd:
                    best_odds[i] = odd
                    websites[i] = bet["website"]
        
        self.best_bets.append(
            Best_bet(
                team1,
                team2,
                sport,
                websites,
                best_odds,
                odds_descriptions
            )
        )


    # gather every similar bet in an objet best_bet
    def gather_bets(self):
        for sport, bets in self.organised_sport_bet.items():
            # search for equals bet
            # select a bet and match it with similar team 1 team 2 bets
            for i, beti in enumerate(bets):
                # if bet is already matched then pass
                if beti["matched"]:
                    continue

                equals_bet = [beti]

                matchi = f'{beti["team1"]} {beti["team2"]}'

                # try to match selected bet with the followings bet
                for j, betj in enumerate(bets[i+1:]):
                    if beti["website"] == betj["website"]:
                        continue

                    matchj = f'{betj["team1"]} {betj["team2"]}'
                    dissimilarity = distance.nlevenshtein(matchi, matchj)
                    # the lower 
                    if dissimilarity < 0.25:
                        beti["matched"] = True
                        betj["matched"] = True
                        equals_bet.append(betj)

                # create best_bet if there is several bets
                if len(equals_bet) > 1:
                    self.create_best_bet(equals_bet, sport)

    def define_valuable_bets(self):
        for best_bet in self.best_bets:
            rentability = best_bet.get_rentability()

            if rentability < 0:
                continue

            print_value = f'''
match: {best_bet.team1} vs {best_bet.team2},
rentability : {rentability}
sport : {best_bet.sport} 
            '''
            print(print_value)
            
            moneys = best_bet.make_money(10, 50)
            print(moneys, best_bet.odds)
            for money, website, odd, odd_description in zip(moneys, best_bet.websites_names, best_bet.odds, best_bet.odds_description):
                print_value = f'''
website : {website},
match: {best_bet.team1} vs {best_bet.team2},
money: {money},
odd:{odd},
odd_description:{odd_description}
                '''
                print(print_value)
                
        
            

           

                

        