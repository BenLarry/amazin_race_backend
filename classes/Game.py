from database import Database
from Login import Login
class Game():
    def __init__(self, player_id = None, continent = None):
        self.player_ID = player_id
        self.continent = continent
        self.db = Database()


    def create_game(self, player_id, start_airport, end_airport, player_airport):
        if player_id == None or start_airport == None or end_airport == None or player_airport == None:
            return {"error": "parametrit eivät täyty"} 
        try:
            conn = self.db.get_conn()
            cursor = conn.cursor(dictionary=True)
            sql = "Insert into game(player_ID, start_airport, end_airport, player_airport, is_over, co2_consumed, points) VALUES(%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (player_id, start_airport['ident'], end_airport['ident'], player_airport['ident'], 0, 0, 0))
        except self.db.connector.errors.ProgrammingError as err:
            print(err)
            return {"error": "räätälöity virheilmoitus"}, 500
        except Exception as err:
            print(err)
            return {"error": "geneerinen virheilmoitus"}, 500    


    def select_game_airports(self, continent):
        if continent == None:
            return {"error": "continent on tyhjä"}
        try:
            conn = self.db.get_conn()
            cursor = conn.cursor(dictionary=True)
            sql_select = "SELECT ident from airport WHERE continent = %s AND name != 'closed' ORDER BY RAND() LIMIT 30"
            cursor.execute(sql_select, (continent,))
            chosen_airports = cursor.fetchall()
            sql_update = "INSERT INTO game_airport(ident, special, visited) VALUES (%s, %s, %s)"
            for airport in chosen_airports:
                cursor.execute(sql_update, (airport['ident'], 0, 0))
        except self.db.connector.errors.ProgrammingError as err:
            print(err)
            return {"error": "räätälöity virheilmoitus"}, 500
        except Exception as err:
            print(err)
            return {"error": "geneerinen virheilmoitus"}, 500    

    #def select_game_questions(self):
       # pass
    #Sama metodi löytyy question.py Luokasta.


    def select_game_continent(self):
        if self.continent == None:
            return {"error": "continenttia ei löydy"}
        try:
            conn = self.db.get_conn()
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT DISTINCT continent FROM airport WHERE continent = %s"
            cursor.execute(sql, (self.continent,))
            continent =cursor.fetchone()
            return continent
        except self.db.connector.errors.ProgrammingError as err:
            print(err)
            return {"error": "räätälöity virheilmoitus"}, 500
        except Exception as err:
            print(err)
            return {"error": "geneerinen virheilmoitus"}, 500    

    def select_random_airport(self):
        try:
            conn = self.db.get_conn()
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT * FROM game_airport WHERE visited = 0 ORDER BY RAND() LIMIT 1"
            cursor.execute(sql)
            random_airport = cursor.fetchone()
            return random_airport
        except self.db.connector.errors.ProgrammingError as err:
            print(err)
            return {"error": "räätälöity virheilmoitus"}, 500
        except Exception as err:
            print(err)
            return {"error": "geneerinen virheilmoitus"}, 500    


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


    def get_game(self, player_id):
        if player_id == "":
            return {"error": "player_id ei löydy"}
        try:
            conn = self.db.get_conn()
            cursor = conn.cursor(dictionary=True)
            sql = "select * from game where player_id = %s"
            cursor.execute(sql, (player_id,))
            game = cursor.fetchone()
            return game
        except self.db.connector.errors.ProgrammingError as err:
            print(err)
            return {"error": "räätälöity virheilmoitus"}, 500
        except Exception as err:
            print(err)
            return {"error": "geneerinen virheilmoitus"}, 500    



pelaaja1 = Login("moi", 6)

peli = Game(pelaaja1.id, "EU")

ok = peli.get_game(pelaaja1.id)

print(ok)

peli.set_game_state(ok['ID'])
#maanosa = peli.select_game_continent()

#print(maanosa)

#ok = peli.select_game_airports(maanosa['continent'])

#kenttä1 = peli.select_random_airport()

#kenttä2 = peli.select_random_airport()






#ok2 = peli.create_game(pelaaja1.id, kenttä1, kenttä2, kenttä1)