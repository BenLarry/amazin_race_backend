from classes.Database import Database

class Airport():
    def __init__(self, game_ID):
        self.game_ID = game_ID
        self.db = Database()

        
    def set_airport_visited(self, ident):
        try:
            conn = self.db.get_conn()
            cursor = conn.cursor(dictionary=True)
            sql = "UPDATE game_airport SET visited = 1 where ident = %s"
            cursor.execute(sql, (ident,))
        except self.db.connector.errors.ProgrammingError as err:
            print(err)
            return {"error": "räätälöity virheilmoitus"}, 500
        except Exception as err:
            print(err)
            return {"error": "geneerinen virheilmoitus"}, 500    
        
    def set_airport_special(self, ident):
        try:
            conn = self.db.get_conn()
            cursor = conn.cursor(dictionary=True)
            sql = "UPDATE game_aiport SET special = 1 where ident = %s AND game_id = %s"
            cursor.execute(sql, (ident, self.game_ID))
        except self.db.connector.errors.ProgrammingError as err:
            print(err)
            return {"error": "räätälöity virheilmoitus"}, 500
        except Exception as err:
            print(err)
            return {"error": "geneerinen virheilmoitus"}, 500  
        
    def get_airport(self):
        try:
            conn = self.db.get_conn()
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT ident, id, special, visited, game_ID FROM game_airport WHERE game_ID = %s"
            cursor.execute(sql, (self.game_ID, ))
            airport_data = cursor.fetchall()
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
            return random_airport["ident"]
        except self.db.connector.errors.ProgrammingError as err:
            print(err)
            return {"error": "räätälöity virheilmoitus"}, 500
        except Exception as err:
            print(err)
            return {"error": "geneerinen virheilmoitus"}, 500   
