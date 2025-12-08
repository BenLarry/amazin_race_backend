from database import Database
from Game import Game
from Login import Login

class Airport():
    def __init__(self, visited, special, game_id, ident = None):
        self.db = Database()
        self.ident = ident
        self.visited = visited
        self.special = special
        self.game_id = game_id
        
    
        
    def set_airport_visited(self):
        if self.ident == None:
            return {"error": "Identtiä ei löydy"}
        try:
            conn = self.db.get_conn()
            cursor = conn.cursor(dictionary=True)
            sql = "UPDATE game_airport SET visited = 1 where ident = %s"
            cursor.execute(sql, (self.ident, ))
        except self.db.connector.errors.ProgrammingError as err:
            print(err)
            return {"error": "räätälöity virheilmoitus"}, 500
        except Exception as err:
            print(err)
            return {"error": "geneerinen virheilmoitus"}, 500    
        

    def set_airport_special(self, game_id):
        if self.ident == None:
            return {"error": "Identtiä ei löydy"}
        try:
            conn = self.db.get_conn()
            cursor = conn.cursor(dictionary=True)
            sql = "UPDATE game_aiport SET special = 1 where ident = %s AND game_id = %s"
            cursor.execute(sql, (self.ident, self.game_id))
        except self.db.connector.errors.ProgrammingError as err:
            print(err)
            return {"error": "räätälöity virheilmoitus"}, 500
        except Exception as err:
            print(err)
            return {"error": "geneerinen virheilmoitus"}, 500  
        

    def get_airport(self):
        if self.ident == None:
            return {"error": "Identtiä ei löydy"}
        try:
            conn = self.db.get_conn()
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT ident, id, name, type, latitude_deg, longitude_deg FROM game_airport WHERE ident = %s"
            cursor.execute(sql, (self.ident, ))
            airport_data = cursor.fetchall()
            print(airport_data)
            return airport_data
        except self.db.connector.errors.ProgrammingError as err:
            print(err)
            return {"error": "räätälöity virheilmoitus"}, 500
        except Exception as err:
            print(err)
            return {"error": "geneerinen virheilmoitus"}, 500    
        

peli = Game(6, "EU")

maanosa = peli.select_game_continent()

print(maanosa)

ok = peli.select_game_airports(maanosa['continent'])

kenttä1 = peli.select_random_airport()

kenttä2 = peli.select_random_airport()


pelaaja1 = Login("moi", 6)



ok2 = peli.create_game(pelaaja1.id, kenttä1, kenttä2, kenttä1)






ok = Airport('EDWG', 0, 0, 48)
ok.get_airport()
