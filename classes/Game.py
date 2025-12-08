from classes.Database import Database
from classes.Airport import Airport
import random

class Game():
    def __init__(self, player_id = None):
        self.player_ID = player_id
        self.game_ID = None
        self.db = Database()

    def create_game(self):
        if self.player_ID == None:
            return {"error": "parametrit eivät täyty"} 
        try:
            #CONNECT TO DB
            conn = self.db.get_conn()
            cursor = conn.cursor(dictionary=True)
            sql = "Insert into game(player_ID, start_airport, end_airport, player_airport, is_over, co2_consumed, points) VALUES(%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (self.player_ID, None, None, None, 0, 0, 0))
            self.game_ID = cursor.lastrowid

            self.select_game_airports(self.select_game_continent())
            self.select_game_questions()

            start_airport = Airport().select_random_airport()


            #SELECT START AIRPORT AND END AIRPORT AND UPDATE THE GAME IN DB 
            return {
                "ID": self.game_ID,
                "player_ID": self.player_ID,
                "start_airport": start_airport,
                "end_airport": None,
                "player_airport": start_airport,
                "is_over": 0,
                "co2_consumed": 0,
                "points": 0
            }
        
            
        except self.db.connector.errors.ProgrammingError as err:
            print(err)
            return {"error": "räätälöity virheilmoitus"}, 500
        except Exception as err:
            print(err)
            return {"error": "geneerinen virheilmoitus"}, 500    


    def select_game_airports(self, continent):
        try:
            conn = self.db.get_conn()
            cursor = conn.cursor(dictionary=True)
            sql_select = "SELECT ident from airport WHERE continent = %s AND name != 'closed' ORDER BY RAND() LIMIT 30"
            cursor.execute(sql_select, (continent,))
            chosen_airports = cursor.fetchall()
            sql_update = "INSERT INTO game_airport(ident, special, visited, game_ID) VALUES (%s, %s, %s, %s)"
            for airport in chosen_airports:
                cursor.execute(sql_update, (airport['ident'], 0, 0, self.game_ID))
        except self.db.connector.errors.ProgrammingError as err:
            print(err)
            return {"error": "räätälöity virheilmoitus"}, 500
        except Exception as err:
            print(err)
            return {"error": "geneerinen virheilmoitus"}, 500    

    def select_game_questions(self):
        if self.game_ID == None:
            return {"error": "game_ID:tä ei löydy"}
        try:
            conn = self.db.get_conn()
            cursor = conn.cursor(dictionary=True)
            sql_selected_questions = """
            (
                SELECT * FROM question WHERE level = 1 ORDER BY RAND() LIMIT 10
            )
            UNION ALL
            (
            SELECT * FROM question WHERE level = 2 ORDER BY RAND() LIMIT 10 
            )
            UNION ALL
            (
                SELECT * FROM question WHERE level = 3 ORDER BY RAND() LIMIT 10
            )
            """
            cursor.execute(sql_selected_questions)
            questions = cursor.fetchall()


            sql_update_questions = "INSERT INTO game_question(question_ID, game_id, answered) VALUES(%s, %s, 0)"
            for question in questions:
                cursor.execute(sql_update_questions, (question['ID'], self.game_ID))
        except self.db.connector.errors.ProgrammingError as err:
            print(err)
            return {"error": "räätälöity virheilmoitus"}, 500
        except Exception as err:
            print(err)
            return {"error": "geneerinen virheilmoitus"}, 500    

    def select_game_continent(self):
        return random.choice(["AF", "AS", "EU", "NA", "SA"]) 


    def set_game_state(self, ID):
        if ID == None:
            return {"error": "ID:tä ei löytynyt"}
        try:
            conn = self.db.get_conn()
            cursor = conn.cursor(dictionary=True)
            sql = "UPDATE game SET is_over = 1 where ID = %s"
            cursor.execute(sql, (ID,))
        except self.db.connector.errors.ProgrammingError as err:
            print(err)
            return {"error": "räätälöity virheilmoitus"}, 500
        except Exception as err:
            print(err)
            return {"error": "geneerinen virheilmoitus"}, 500    


    def get_game(self):
        if self.player_ID == None:
            return {"error": "player_id ei löydy"}
        try:
            conn = self.db.get_conn()
            cursor = conn.cursor(dictionary=True)
            sql = "select * from game where player_id = %s AND is_over = %s"
            cursor.execute(sql, (self.player_ID, 0))
            game = cursor.fetchall()
            return game
        except self.db.connector.errors.ProgrammingError as err:
            print(err)
            return {"error": "räätälöity virheilmoitus"}, 500
        except Exception as err:
            print(err)
            return {"error": "geneerinen virheilmoitus"}, 500    