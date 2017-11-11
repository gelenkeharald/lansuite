import math as math

class ELO():

    # calculate new elo value
    # R: current elo
    # k: weigthing factor
    # S: points
    # E: probability
    def calc_new_elo(self, R, k, S, E):
        return R+k*(S-E)
        

    # calculate new elo summand
    # k: weigthing factor
    # S: points
    # E: probability
    def calc_new_elo_summand(self, k, S, E):
        return k*(S-E)
        
    # todo: k: ist üblicherweise 20, bei Top-Spielern (Elo > 2400) 10, bei weniger als 30 gewerteten Partien 40, für Jugendspieler (unter 18, Elo < 2300) 40
    def get_elo_weighting_factor(self, R, num_games):
        if num_games < 5:
            return 40
            #return 10 # to get to know basics about the game
        elif R > 2400:
            return 10
        elif R < 2300:
            return 40
        else:
            return 20
    
    
    # calculate probability
    # Ra: current elo party A
    # Rb: current elo party B
    def calc_probability(self, Ra, Rb):
        return 1/(1+math.pow(10, (Rb-Ra)/400 ) )