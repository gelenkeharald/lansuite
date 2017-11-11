import tkinter as tk

class Team(tk.Frame):
    def __init__(self, parent, window, id, team_won_radiobutton):
        self.parent = parent
        
        tk.Frame.__init__(self, window)
        self.window = window
        
        self.id = id
              
        self.fr = tk.Frame(self.window, borderwidth=2, relief='groove')
        self.fr.grid(row=3, column=self.id-1, sticky=tk.N)
        
        tk.Label(self.fr, text="Pos", font="bold").grid(row=1, column=0)
        tk.Label(self.fr, text="Name", font="bold").grid(row=1, column=1)
        tk.Label(self.fr, text="Elo", font="bold").grid(row=1, column=2)
        tk.Label(self.fr, text="+/-", font="bold").grid(row=1, column=3)
        
        radiobutton=tk.Radiobutton(self.fr, text="Team " + str(self.id), font="bold", indicatoron=0, variable=team_won_radiobutton, value=self.id, command=self.parent.set_team_won)
        radiobutton.grid(row=0, column=0, columnspan=2)
                    
        self.status_label=tk.Label(self.fr, font="bold")
        self.status_label.grid(row=0, column=2)
        
        self.elo_sum = 0
        self.elo = 0
        self.members = []
        self.new_elo_summand_labels = []


    # add a team member
    def add_member(self, person):
        self.members.append(person)
        self.elo_sum += person.elo
        self.elo = self.elo_sum / len(self.members)
     
     
    def set_elo_probability(self, probability):
        self.elo_probability = probability
     
    
     # all members added, print team values
    def members_complete(self):
        for i in range(len(self.members)):
            tk.Label(self.fr, text=self.members[i].rank).grid(row=2+i, column=0)
            tk.Label(self.fr, text=self.members[i].name).grid(row=2+i, column=1)
            tk.Label(self.fr, text=round(self.members[i].elo, 2)).grid(row=2+i, column=2)
            
            self.members[i].set_new_elo(0.5, self.elo_probability) # initially calculated for drawn game
            self.new_elo_summand_labels.append( tk.Label(self.fr, text=self.members[i].get_new_elo_summand_string() ) )
            self.new_elo_summand_labels[i].grid(row=2+i, column=3)
        
        elo_str = "Ø " + str(round(self.elo, 2))
        tk.Label(self.fr, text=elo_str).grid(row=2+1+i, column=2)
        elo_prob_str = str(round(self.elo_probability*100, 1)) + " %"
        tk.Label(self.fr, text=elo_prob_str).grid(row=2+2+i, column=2)
        
    
    def set_status(self, team_id):
        if self.id == team_id:
            self.status_label.configure(text="won", fg="Green")
            self.point = 1
            for i in range(len(self.members)):
                self.members[i].set_new_elo(self.point, self.elo_probability)
                self.new_elo_summand_labels[i].configure( text=self.members[i].get_new_elo_summand_string() )
        else:
            self.status_label.configure(text="lost", fg="Red")
            self.point = 0
            for i in range(len(self.members)):
                self.members[i].set_new_elo(self.point, self.elo_probability)
                self.new_elo_summand_labels[i].configure( text=self.members[i].get_new_elo_summand_string() )