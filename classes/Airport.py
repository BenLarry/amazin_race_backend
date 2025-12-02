from database import Database

class Airport():
    def __init__(self, visited, special,game_ID, ident = None):
        self.db = Database()
        self.ident = ident
        self.visited = visited
        self.special = special
        self.game_ID = game_ID
        
    
        
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
        

    def set_airport_special(self):
        if self.ident == None:
            return {"error": "Identtiä ei löydy"}
        try:
            conn = self.db.get_conn()
            cursor = conn.cursor(dictionary=True)
            sql = "UPDATE game_aiport SET special = 1 where ident = %s"
            cursor.execute(sql, (self.ident,))
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
            sql = "SELECT ident, id, name, type, latitude_deg, longitude_deg FROM airport WHERE ident = %s"
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
        



ok = Airport(0, 0, 0,)
ok.get_airport()
