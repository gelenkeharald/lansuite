from ELO import ELO

class Person(ELO):
    def __init__(self, id, name, matches, wins, elo):
        self.id = id
        self.name = name
        self.matches = matches
        self.wins = wins
        if matches == 0:
            self.ratio = 0
        else:
            self.ratio = wins/matches
        self.elo = elo
        self.rank = 0
        
    def set_new_elo(self, point, probability):
        k=self.get_elo_weighting_factor(self.elo, self.matches)
            
        self.__new_elo = self.calc_new_elo(self.elo, k, point, probability)
        self.__new_elo_summand = self.calc_new_elo_summand(k, point, probability)
            
    def get_new_elo(self):
        return self.__new_elo
            
    def get_new_elo_summand_string(self):
        return ["", "+"][self.__new_elo_summand > 0] + str(round(self.__new_elo_summand, 2))