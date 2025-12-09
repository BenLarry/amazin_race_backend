from classes.Database import Database

class Highscore():
    def __init__(self, ):
        self.db = Database()

       

    
    def get_highscore(self):
        conn = self.db.get_conn()
        cursor = conn.cursor(dictionary=True)
        sql = """select player.name, MAX(game.points) as top_points
                from game
                inner join player on game.player_ID = player.ID
                where is_over = 1
                GROUP BY player.name
                order BY top_points DESC
                limit 10
            """
        cursor.execute(sql)
        highscore = cursor.fetchall()
        return highscore
        
    def get_highscore_params(self, ID):
        conn = self.db.get_conn()
        cursor = conn.cursor(dictionary=True)
        sql = """select player.name, MAX(game.points) as top_points
                from game
                inner join player on game.player_ID = player.ID
                where game.player_id = %s and is_over = 1
                order BY top_points DESC
                limit 1
            """
        cursor.execute(sql, (ID,))
        highscore_param = cursor.fetchall()
        return highscore_param
