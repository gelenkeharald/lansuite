import tkinter as tk

class Row(tk.Frame):
    def __init__(self, parent, window, row, next_match_checkbutton):
        self.parent = parent
        
        tk.Frame.__init__(self, window)
        self.window = window
        
        # create GUI widgets
        self.rank = tk.Label(self.window)
        self.rank.grid(row=row, column=0)
        
        self.name = tk.Label(self.window)
        self.name.grid(row=row, column=1)
        
        self.matches = tk.Label(self.window)
        self.matches.grid(row=row, column=2)
        
        self.wins = tk.Label(self.window)
        self.wins.grid(row=row, column=3)
        
        self.ratio = tk.Label(self.window)
        self.ratio.grid(row=row, column=4)
        
        self.elo = tk.Label(self.window)
        self.elo.grid(row=row, column=5)
        
        self.check = tk.Checkbutton(self.window, variable=next_match_checkbutton, command=self.parent.calc_rank)
        self.check.grid(row=row, column=6)
        
        self.pos = tk.Label(self.window)
        self.pos.grid(row=row, column=7)
        
        self.team_radiobutton = tk.IntVar()
        self.team1_radiobutton = tk.Radiobutton(self.window, variable=self.team_radiobutton, value=1, state=tk.DISABLED)
        self.team1_radiobutton.grid(row=row, column=8)
        self.team2_radiobutton = tk.Radiobutton(self.window, variable=self.team_radiobutton, value=2, state=tk.DISABLED)
        self.team2_radiobutton.grid(row=row, column=9)
        
    # update values
    def update_data(self, rank, name, matches, wins, ratio, elo):
        self.rank.configure(text=rank)
        self.name.configure(text=name)
        self.matches.configure(text=matches)
        self.wins.configure(text=wins)
        self.ratio.configure(text=ratio)
        self.elo.configure(text=elo)
        if matches < 5:
            self.elo.configure(fg="Blue")
        elif elo > 2400:
            self.elo.configure(fg="Green")
        elif elo < 2300:
            self.elo.configure(fg="Red")
        else:
            self.elo.configure(fg="Black")
            
    
    # update position
    def update_pos(self, pos):
        self.pos.configure(text=pos)
        
if __name__ == "__main__":
    root = tk.Tk()
    test=Row(root, 1 )
    test.grid()
    test.update(1,1,1,1,1) 
    
    
    root.mainloop()