from classes.Database import Database

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
