from dataclasses import dataclass
import numpy as np

@dataclass
class Best_bet:
    team1 : str
    team2 : str
    sport : str
    websites_names : list[str]
    odds : list[float]
    odds_description : list[str]

    def __init__(self, team1, team2, sport, websites_names, odds, odds_description):
        self.team1 = team1
        self.team2 = team2
        self.sport = sport
        self.websites_names = websites_names
        self.odds = odds
        self.odds_description = odds_description
    
    def get_rentability(self):
        return 1 - np.sum([1/x for x in self.odds])
    
    def make_money(self, money_to_make, max_money_to_bet):
        m_size = len(self.odds)

        # if bet is not valuable then do not gamble
        if self.get_rentability() < 0:
            return [0 for _ in range(m_size)]
        
        
        diagonal = np.array([odd - 1 for odd in self.odds])
        A = np.full((m_size, m_size), -1, np.float32)
        np.fill_diagonal(A, diagonal)
        b = np.array([[money_to_make] for _ in range(m_size)])

        sol = np.linalg.solve(A,b)

        if max(sol) > max_money_to_bet:
            sol = sol * (max_money_to_bet / max(sol))

        return sol
    
        

    
