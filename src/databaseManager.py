import sqlite3

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect("../players.db")
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS players(name, W, L, D)")

    def __del__(self):
        self.conn.close()

    def insert_name_into_db(self, name: str):
        """
        This code fragment inserts a new player into the 'players' table in an SQLite database.
        """
        self.cur.execute(f"INSERT INTO players VALUES ('{name}',0,0,0)")
        self.conn.commit()

    def check_name_in_db(self, name: str):
        """
        Checks whether a player with a given name exists in a database.
        """
        result_t = self.cur.execute(f"SELECT name FROM players WHERE name='{name}'")
        if result_t.fetchone():
            print("Name exists")
        else:
            self.insert_name_into_db(name)
            print("Player created")

    def display_db_for_name(self, name: str):
        """
        Displays content of selected dB.
        :param name: name of the player
        """
        for row in self.cur.execute(f"SELECT * FROM players WHERE name ='{name}'"):
            print(row)

    def update_name_score_in_db(self, letter: str, name: str):
        """
        Increment score by one in selected table.
        :param name: name of the player
        :param letter: W - Wins | L - Loses | D - Draws
        """
        self.cur.execute(f"UPDATE players SET {letter} = {letter}+1 WHERE name='{name}'")
        self.conn.commit()