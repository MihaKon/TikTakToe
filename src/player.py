from databaseManager import DatabaseManager


class Player:
    def __init__(self, name):
        self.name = name

    def insert_player_into_db(self, db_manager: DatabaseManager):
        db_manager.insert_name_into_db(self.name)

    def update_player_score(self, letter: str, db_manager: DatabaseManager):
        db_manager.update_name_score_in_db(letter, self.name)

    def show_player_score(self, db_manager: DatabaseManager):
        db_manager.display_db_for_name(self.name)
