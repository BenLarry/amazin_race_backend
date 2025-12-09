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
            sql = """SELECT game_airport.ident, game_airport.id, special, visited, game_ID, latitude_deg, longitude_deg 
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



    def calculate_co2(self):
        conn = self.db.get_conn()
        cursor = conn.cursor(dictionary=True)
        sql = """select latitude_deg, longitude_deg, type from airport
        inner join game_airport on game_airport.ident = airport.ident
        where game_ID = %s
        """
        cursor.execute(sql, (self.game_ID,))
        destination_points = cursor.fetchall()
        
        
        sql_player_location = """select latitude_deg, longitude_deg from airport
        inner join game on game.player_airport = airport.ident
        where game.ID = %s
        """
        cursor.execute(sql_player_location, (self.game_ID,))
        player_coords = cursor.fetchone()
        player_point_coords = (player_coords['latitude_deg'], player_coords['longitude_deg'])


        co2_prices = []
        for airport in destination_points:
            airport_coords = (airport["latitude_deg"], airport["longitude_deg"])
            km = distance.distance(airport_coords, player_point_coords).km
            co2_price = km * 0.20
            co2_prices.append({
                "airport": airport["type"],
                "price": co2_price
            })

        return co2_prices