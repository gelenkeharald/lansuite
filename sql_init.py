import mysql.connector as mariadb

connection = mariadb.connect(user='root', password='Vietnam15', database='ranking')

cursor = connection.cursor()

    
default_elo = 2350
hours_to_elo_factor = 0.25

# persons
sql_cmd = "DROP TABLE IF EXISTS persons"
cursor.execute(sql_cmd)

sql_cmd = """
CREATE TABLE persons (
id INT AUTO_INCREMENT,
name VARCHAR(20) NOT NULL,
PRIMARY KEY (id),
UNIQUE KEY (name)
);"""
cursor.execute(sql_cmd)

sql_cmd = "INSERT INTO persons VALUES (NULL, 'Robert')"
cursor.execute(sql_cmd)

sql_cmd = "INSERT INTO persons VALUES (NULL, 'Martin')"
cursor.execute(sql_cmd)

sql_cmd = "INSERT INTO persons VALUES (NULL, 'Matze')"
cursor.execute(sql_cmd)

sql_cmd = "INSERT INTO persons VALUES (NULL, 'Franz')"
cursor.execute(sql_cmd)

sql_cmd = "INSERT INTO persons VALUES (NULL, 'Raik')"
cursor.execute(sql_cmd)

sql_cmd = "INSERT INTO persons VALUES (NULL, 'Stefan')"
cursor.execute(sql_cmd)

sql_cmd = "INSERT INTO persons VALUES (NULL, 'Kiesow')"
cursor.execute(sql_cmd)

sql_cmd = "INSERT INTO persons VALUES (NULL, 'Tilo')"
cursor.execute(sql_cmd)


# games
sql_cmd = "DROP TABLE IF EXISTS games"
cursor.execute(sql_cmd)

sql_cmd = """
CREATE TABLE games (
id INT AUTO_INCREMENT,
name VARCHAR(20) NOT NULL,
PRIMARY KEY (id),
UNIQUE KEY (name)
);"""
cursor.execute(sql_cmd)

sql_cmd = "INSERT INTO games VALUES (NULL, 'Dota 2')"
cursor.execute(sql_cmd)

sql_cmd = "INSERT INTO games VALUES (NULL, 'Counter-Strike')"
cursor.execute(sql_cmd)

# stats
sql_cmd = "DROP TABLE IF EXISTS stats"
cursor.execute(sql_cmd)

sql_cmd = """
CREATE TABLE stats (
id INT AUTO_INCREMENT,
game_id INTEGER,
match_id INTEGER,
person_id INTEGER,
num_games INTEGER,
wins INTEGER,
elo REAL,
PRIMARY KEY (id)
);"""
cursor.execute(sql_cmd)

# teams
sql_cmd = "DROP TABLE IF EXISTS teams"
cursor.execute(sql_cmd)

sql_cmd = """
CREATE TABLE teams (
id INT AUTO_INCREMENT,
game_id INTEGER,
match_id INTEGER,
team_1 VARCHAR(50),
team_2 VARCHAR(50),
team_win INTEGER,
PRIMARY KEY (id)
);"""
cursor.execute(sql_cmd)

connection.commit()
connection.close()