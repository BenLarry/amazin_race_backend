from classes.Database import Database
from geopy import distance

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
            sql = "UPDATE game_airport SET special = 1 where ident = %s AND game_ID = %s"
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
            sql = """SELECT game_airport.ident, game_airport.id, special, visited, game_ID, latitude_deg, longitude_deg, type 
            FROM game_airport, airport 
            where airport.ident = game_airport.ident AND game_ID = %s; 
            """
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
            sql = "SELECT * FROM game_airport WHERE visited = 0 and game_ID = %s ORDER BY RAND() LIMIT 1"
            cursor.execute(sql, (self.game_ID,))
            random_airport = cursor.fetchone()
            return random_airport["ident"]
        except self.db.connector.errors.ProgrammingError as err:
            print(err)
            return {"error": "räätälöity virheilmoitus"}, 500
        except Exception as err:
            print(err)
            return {"error": "geneerinen virheilmoitus"}, 500   



    def calculate_co2(self, ident):
        try:
            conn = self.db.get_conn()
            cursor = conn.cursor(dictionary=True)
            sql = """select latitude_deg, longitude_deg from airport
            inner join game_airport on game_airport.ident = airport.ident
            where game_ID = %s and game_airport.ident = %s
            """
            cursor.execute(sql, (self.game_ID, ident,))
            destination_coords = cursor.fetchone()
            destination_point = (destination_coords['latitude_deg'], destination_coords['longitude_deg'])
            
            sql_player_location = """select latitude_deg, longitude_deg from airport
            inner join game on game.player_airport = airport.ident
            where game.ID = %s
            """
            cursor.execute(sql_player_location, (self.game_ID,))
            player_coords = cursor.fetchone()
            player_point_coords = (player_coords['latitude_deg'], player_coords['longitude_deg'])
         
            km = distance.distance(destination_point, player_point_coords).km
            co2_price = km * 0.20
           
            return {
                "price": int(co2_price)
                }
        
        except self.db.connector.errors.ProgrammingError as err:
            print(err)
            return {"error": "räätälöity virheilmoitus"}, 500
        except Exception as err:
            print(err)
            return {"error": "geneerinen virheilmoitus"}, 500   