import tkinter as tk
import mysql.connector as mariadb # mariadb
import datetime

# embed matplot into tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import pyplot as plt


from Row import Row
from Team import Team
from Person import Person
from ELO import ELO

try:
    connection = mariadb.connect(host='127.0.0.1', user='root', password='Vietnam15', database='ranking')
except: #all
    try:
        connection = mariadb.connect(host='192.168.178.3', user='ranking_client', password='warcraft', database='ranking')
    except: #all
        print("no mysql connection possible")
    else:
        cursor = connection.cursor()
        connection.autocommit = True
        user = "client"
else:
    cursor = connection.cursor()
    connection.autocommit = True
    user = "admin"
    
class GUI(tk.Frame, ELO):
    def __init__(self, window, user):
        tk.Frame.__init__(self, window)
        self.window = window
        self.user = user
        self.intervall = tk.BooleanVar()
        
        if user == "admin":
            self.window.title("Ranking Admin")
        else:
            self.window.title("Ranking Client")
        self.window.geometry("1500x800")
        
        if user == "admin":
            menubar = tk.Menu(self.window)
            addmenu = tk.Menu(menubar, tearoff=0)
            addmenu.add_command(label=".. Person", command=self.add_person_gui)
            addmenu.add_command(label=".. Game", command=self.add_game_gui)
            menubar.add_cascade(label="Add", menu=addmenu)
            
            self.window.config(menu=menubar)
        
        cursor.execute("SELECT * FROM games")
        self.games = cursor.fetchall()
        self.games.sort(key=lambda tup: tup[1])
        
        self.games_options = {}
        for i in range(len(self.games)):
            self.games_options[self.games[i][1]] = self.games[i][0]      
        self.games_options["all"] = 0
        
        var = tk.StringVar()
        var.set( list(self.games_options.keys())[0] )
        self.current_game_id = self.games_options[var.get()]
        
        # game
        self.fr_game = tk.Frame(self.window, borderwidth=2, relief='groove')
        self.fr_game.grid(row = 0, column=0, columnspan=2)
        tk.Label(self.fr_game, text="Game:", font="bold").grid(row=0, column=0)
        self.games_optionmenu = tk.OptionMenu(self.fr_game, var, *self.games_options.keys(), command=self.set_current_game_id)
        self.games_optionmenu.grid(row = 0, column=1)
        tk.Label(self.fr_game, text="Total Matches:", font="bold").grid(row=0, column=2)
        self.total_matches_label = tk.Label(self.fr_game, text="Total Matches:", font="bold")
        self.total_matches_label.grid(row=0, column=3)
        
        # intervall
        self.fr_intervall = tk.Frame(self.window, borderwidth=2, relief='groove')
        self.fr_intervall.grid(row = 1, column=0, columnspan=2)
        tk.Checkbutton(self.fr_intervall, text="auto", variable=self.intervall, onvalue=1, offvalue=0, command=self.auto_update).grid(row=0, column=0)
        tk.Button(self.fr_intervall, text="Update", font="bold", command=self.update_stats).grid(row=0, column=1)
        self.last_update_label = tk.Label(self.fr_intervall, font="bold")
        self.last_update_label.grid(row=0, column=2)
        
        self.get_num_persons()
        self.next_match_checkbutton = [tk.BooleanVar() for i in range(self.num_persons)]
        
        # stats
        self.fr_stats = tk.Frame(self.window, borderwidth=2, relief='groove')
        self.fr_stats.grid(row=2, column=0, columnspan=2)
        tk.Label(self.fr_stats, text="Rank", font="bold").grid(row=0, column=0)
        tk.Label(self.fr_stats, text="Name", font="bold").grid(row=0, column=1)
        tk.Label(self.fr_stats, text="Matches", font="bold").grid(row=0, column=2)
        tk.Label(self.fr_stats, text="Wins", font="bold").grid(row=0, column=3)
        tk.Label(self.fr_stats, text="Ratio", font="bold").grid(row=0, column=4)
        tk.Label(self.fr_stats, text="Elo", font="bold").grid(row=0, column=5)
        tk.Button(self.fr_stats, text="Next Match?", font="bold", command=self.toggle_all_persons).grid(row=0, column=6)
        self.auto_button = tk.Button(self.fr_stats, text="Auto!", font="bold", state=tk.DISABLED, command=self.set_auto_team)
        self.auto_button.grid(row=0, column=7)
        self.man_button = tk.Button(self.fr_stats, text="Man!", font="bold", state=tk.DISABLED, command=self.set_man_team)
        self.man_button.grid(row=0, column=8, columnspan=2)
        
        self.enable_graph = True
        
        self.create_rows()
        self.update_time()
    
        
        if self.enable_graph == True:
            self.print_graph()
        
    def get_num_persons(self):
        cursor.execute("SELECT COUNT(*) FROM persons")
        self.num_persons = cursor.fetchone()[0]
        
    def add_game_gui(self):
        self.add_game_gui = tk.Tk()        
        
        for i in range(len(self.games)):
            tk.Label(self.add_game_gui, text=self.games[i][1]).grid(row=i, column=0)

        self.game_entry = tk.Entry(self.add_game_gui)
        self.game_entry.grid(row=i+1, column=0)
        tk.Button(self.add_game_gui, text="Add", command=self.add_game_sql).grid(row=i+1, column=1)
        
        
    def add_game_sql(self):
        sql_cmd = "INSERT INTO games VALUES (NULL, '" + str(self.game_entry.get()) + "')"
        cursor.execute(sql_cmd)
        self.add_game_gui.destroy()
        
        
    def add_person_gui(self):
        cursor.execute("SELECT * FROM persons")
        persons = cursor.fetchall()
        persons.sort()
        
        self.add_person_gui = tk.Tk()        
        
        for i in range(len(self.persons)):
            tk.Label(self.add_person_gui, text=persons[i]).grid(row=i, column=0)

        self.person_entry = tk.Entry(self.add_person_gui)
        self.person_entry.grid(row=i+1, column=0)
        tk.Button(self.add_person_gui, text="Add", command=self.add_person_sql).grid(row=i+1, column=1)
        
        
    def add_person_sql(self):
        sql_cmd = "INSERT INTO persons VALUES (NULL, '" + str(self.person_entry.get()) + "')"
        cursor.execute(sql_cmd)
        self.add_person_gui.destroy()
        
    
    # set current games id
    def set_current_game_id(self, var):
        self.current_game_id = self.games_options[var]
        if self.current_game_id == 0:
            self.auto_button.configure(state=tk.DISABLED)
            self.man_button.configure(state=tk.DISABLED)
        else:
            self.auto_button.configure(state=tk.ACTIVE)
            self.man_button.configure(state=tk.ACTIVE)
            
        self.update_stats()
            
        if self.enable_graph == True:
            self.print_graph()
            
    def get_matches_sql(self):
        if self.current_game_id == 0: # get matches for all games
            all_matches = 0
            for i in range(1,len(self.games)+1):
                sql_cmd = "SELECT match_id FROM stats WHERE game_id LIKE " + str(i) + " ORDER BY id DESC LIMIT 1"
                cursor.execute(sql_cmd)
                data = cursor.fetchone()
                if data is None:
                    self.matches = 0
                    break
                else:
                    all_matches = all_matches + data[0]
            self.matches = all_matches
        else:
            sql_cmd = "SELECT match_id FROM stats WHERE game_id LIKE " + str(self.current_game_id) + " ORDER BY id DESC LIMIT 1"
            cursor.execute(sql_cmd)
            data = cursor.fetchone()
            if data is None:
                self.matches = 0
            else:
                self.matches = data[0]
        
        
    # get current statistics from database
    def get_stat_data_sql(self):
    
        self.persons = []
        
        for person_id in range(1,self.num_persons+1):
            if self.current_game_id == 0: # get data for all games
                num_games = 0
                num_matches = 0
                wins = 0
                elo_sum = 0
                for i in range(1,len(self.games)+1):
                    cursor.execute("SELECT * FROM stats WHERE game_id LIKE " + str(i) + " AND person_id LIKE " + str(person_id) + " ORDER BY id DESC LIMIT 1")
                    data = cursor.fetchone()
                    
                    if data is None:
                        None
                    else:
                        num_games = num_games + 1
                        num_matches = num_matches + data[4]
                        wins = wins + data[5]
                        elo_sum = elo_sum + data[6]
                        
                if num_games == 0:
                    self.persons.append( Person(person_id, self.get_name_sql(person_id), 0, 0, 2350 ) )
                else:
                    elo = elo_sum / num_games
                    self.persons.append( Person(person_id, self.get_name_sql(person_id), num_matches, wins, elo ) )
            else:
                cursor.execute("SELECT * FROM stats WHERE game_id LIKE " + str(self.current_game_id) + " AND person_id LIKE " + str(person_id) + " ORDER BY id DESC LIMIT 1")

                data = cursor.fetchone()
                if data is None:
                    self.persons.append( Person(person_id, self.get_name_sql(person_id), 0, 0, 2350 ) )
                else:
                    self.persons.append( Person(person_id, self.get_name_sql(person_id), data[4], data[5], data[6] ) )
            
        self.persons.sort(key=lambda x: x.elo, reverse=True) # sort by elo
       
       
    # get name out of persons table
    def get_name_sql(self, id):
        cursor.execute("SELECT name FROM persons WHERE id LIKE " + str(id) )
        return cursor.fetchone()[0]
        
        
    # create GUI rows
    def create_rows(self):
        self.rows = []
        for i in range(self.num_persons): #Rows
            self.rows.append( Row(self, self.fr_stats, i+1, self.next_match_checkbutton[i]) )
        self.update_stats()
           

    def auto_update(self):
        if self.intervall.get():
            self.after(30000, self.auto_update)
            self.update_stats()
            
    def update_time(self):
        self.last_update_label.configure(text=datetime.datetime.strftime(datetime.datetime.now(), '%d.%m.%Y %H:%M:%S'))
    
    
    # update GUI with stats
    def update_stats(self):     
        self.update_time()
        if hasattr(self, 'commit_button'):
            self.commit_button.grid_forget()
        if hasattr(self, 'team1'):
            self.team1.fr.grid_forget()
        if hasattr(self, 'team2'):
            self.team2.fr.grid_forget()

        self.get_matches_sql()
        self.total_matches_label.configure(text=self.matches)
                
        self.get_stat_data_sql()
        for i in range(len(self.persons)):
            self.rows[i].update_data(i+1, self.persons[i].name, self.persons[i].matches, self.persons[i].wins, round(self.persons[i].ratio, 2), round(self.persons[i].elo, 2))
            
        if self.enable_graph == True:
            self.print_graph()

    
    # "check in" all persons for the next game
    def toggle_all_persons(self):
        val = not self.next_match_checkbutton[0].get()
        for i in range(self.num_persons):
            self.next_match_checkbutton[i].set( val )
        self.calc_rank()
        
    
    ## calculate rank for next game
    def calc_rank(self):
        self.rank = 0
        self.next_match_persons = []
        for i in range(len(self.persons)):
            if self.next_match_checkbutton[i].get():
                if self.rank%4 == 0 or self.rank%4 == 3: # 
                    self.rows[i].team_radiobutton.set(1)
                else:
                    self.rows[i].team_radiobutton.set(2)
                    
                self.rank = self.rank + 1
                self.persons[i].rank = self.rank
                self.next_match_persons.append( self.persons[i] )
                self.rows[i].update_pos(self.rank)
                self.rows[i].team1_radiobutton.configure(state=tk.ACTIVE)
                self.rows[i].team2_radiobutton.configure(state=tk.ACTIVE)
            else:
                self.rows[i].update_pos('-')
                self.rows[i].team1_radiobutton.configure(state=tk.DISABLED)
                self.rows[i].team2_radiobutton.configure(state=tk.DISABLED)
                
        if self.rank >=2 and self.current_game_id != 0:
            self.auto_button.configure(state=tk.ACTIVE)
            self.man_button.configure(state=tk.ACTIVE)
        else:
            self.auto_button.configure(state=tk.DISABLED)
            self.man_button.configure(state=tk.DISABLED)
    
    
    # assign persons automatically to balanced teams
    def set_auto_team(self): 
        self.calc_rank()
        if self.user == "admin":
            self.create_commit_button()
                
        if hasattr(self, 'team1'):
            self.team1.fr.grid_forget()
        if hasattr(self, 'team2'):
            self.team2.fr.grid_forget()
            
        self.team_won_radiobutton = tk.IntVar()
        self.team1 = Team(self, self.window, 1, self.team_won_radiobutton)
        self.team2 = Team(self, self.window, 2, self.team_won_radiobutton)
               
        for i in range(len(self.next_match_persons)):                
            if i%4 == 0 or i%4 == 3: # 
                self.team1.add_member(self.next_match_persons[i])
            else:
                self.team2.add_member(self.next_match_persons[i])
        
        self.team1.set_elo_probability( self.calc_probability(self.team1.elo, self.team2.elo) )
        self.team2.set_elo_probability( self.calc_probability(self.team2.elo, self.team1.elo) )
        self.team1.members_complete()
        self.team2.members_complete()
        
        
    # assign persons manually to teams
    def set_man_team(self):
        if self.user == "admin":
            self.create_commit_button()
                
        if hasattr(self, 'team1'):
            self.team1.fr.grid_forget()
        if hasattr(self, 'team2'):
            self.team2.fr.grid_forget()
            
        self.team_won_radiobutton = tk.IntVar()
        self.team1 = Team(self, self.window, 1, self.team_won_radiobutton)
        self.team2 = Team(self, self.window, 2, self.team_won_radiobutton)
               
        for i in range(len(self.next_match_persons)):
            j=0
            while self.persons[j].id != self.next_match_persons[i].id:
                j+=1           
            
            if self.rows[j].team_radiobutton.get() == 1:
                self.team1.add_member(self.next_match_persons[i])
            elif self.rows[j].team_radiobutton.get() == 2:
                self.team2.add_member(self.next_match_persons[i])
            else:
                print("err")
        
        self.team1.set_elo_probability( self.calc_probability(self.team1.elo, self.team2.elo) )
        self.team2.set_elo_probability( self.calc_probability(self.team2.elo, self.team1.elo) )
        self.team1.members_complete()
        self.team2.members_complete()
        
    # create the commit button
    def create_commit_button(self):
        self.commit_button = tk.Button(self.window, text="Commit!", font="bold", state=tk.DISABLED, command=self.commit_sql)
        self.commit_button.grid(row=3, column=0, columnspan=2)


    # set winning team
    def set_team_won(self):
        if self.user == "admin":
            # activate the commit button
            self.commit_button.configure(state=tk.ACTIVE)
        self.team1.set_status( self.team_won_radiobutton.get() )
        self.team2.set_status( self.team_won_radiobutton.get() )
        
    
    # commit data to database
    def commit_sql(self):
        match_id = self.matches + 1
        team1_str = ""
        for i in range(len(self.team1.members)):
            team1_str = team1_str + str(self.team1.members[i].id) + ', '
            
            sql_cmd = "INSERT INTO stats VALUES (NULL, " + str(self.current_game_id) + ", " + str(match_id) + ", " + str(self.team1.members[i].id) + ", " + str(self.team1.members[i].matches + 1) + ", " + str(self.team1.members[i].wins + self.team1.point) + ", " + str(self.team1.members[i].get_new_elo()) + ")"
            cursor.execute(sql_cmd)
            
        team2_str = ""
        for i in range(len(self.team2.members)):
            team2_str = team2_str + str(self.team2.members[i].id) + ', '
            
            sql_cmd = "INSERT INTO stats VALUES (NULL, " + str(self.current_game_id) + ", " + str(match_id) + ", " + str(self.team2.members[i].id) + ", " + str(self.team2.members[i].matches + 1) + ", " + str(self.team2.members[i].wins + self.team2.point) + ", " + str(self.team2.members[i].get_new_elo()) + ")"
            cursor.execute(sql_cmd)
                
        sql_cmd = "INSERT INTO teams VALUES (NULL, " + str(self.current_game_id) + ", " + str(match_id) + ", '" + team1_str + "', '" + team2_str + "', " + str(self.team_won_radiobutton.get()) + ")"
        cursor.execute(sql_cmd)
        
        # update GUI
        self.update_stats()
        
        
#    #
    def print_graph(self):
#        print("unused")
        self.fr_graph = tk.Frame(self.window, borderwidth=2, relief='groove')
        self.fr_graph.grid(row = 0, column=2, rowspan = 20)
        
        f = plt.figure(figsize=(7,7), dpi=100)
        a = f.add_subplot(111)
        plt.xlabel('Match', fontsize=18)
        plt.ylabel('ELO', fontsize=16)
        
        plot_style = ['b-', 'g-', 'r-', 'c-', 'm-', 'k-', 'b--', 'g--', 'r--', 'c--', 'm--', 'k--']
        names = []
        for person_id in range(1,self.num_persons+1):
            x = []
            y = []
            plt_vld = False
            for match_id in range(0, self.matches+1):
                cursor.execute("SELECT elo FROM stats WHERE game_id LIKE " + str(self.current_game_id) + " AND match_id LIKE " + str(match_id) + " AND person_id LIKE " + str(person_id))
                data=cursor.fetchone()
                
                if not data is None: # append data for current match_id
                    x.append(match_id)
                    y.append(data[0])
                    plt_vld = True
                elif plt_vld == True: # no data for current match_id, person was not attending, get last data
                    x.append(match_id)
                    y.append(y[-1])
                    
            if plt_vld == True: # add initial elo for starting point
                x.insert(0, x[0]-1)
                y.insert(0, 2350)
                a.plot(x, y, plot_style[person_id-1], linewidth=2.0)
                names.append(self.get_name_sql(person_id))
                
                        
        a.legend(names, loc='upper left')
        canvas = FigureCanvasTkAgg(f, master=self.fr_graph)
        canvas.show()
        canvas.get_tk_widget().grid()
        
            
        
if __name__ == "__main__":
    if 'user' in globals():
        root = tk.Tk()
        root.lift()
        GUI(root, user).grid()
        root.mainloop()
        
connection.commit()
connection.close()