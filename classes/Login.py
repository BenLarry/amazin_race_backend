from classes.Database import Database

class Login():
    def __init__(self, name, id):
        self.id = id
        self.name = name
        self.db = Database()

    def create_player(self):
        try:
            conn = self.db.get_conn()
            sql = "insert into player (name) VALUES(%s)"
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (self.name,))
            return {
                "id": cursor.lastrowid,
                "name": self.name
            }
        except Exception as e:
            print(e)

    def login_player(self):
        try:
            conn = self.db.get_conn()
            sql = "SELECT * FROM player WHERE name=%s AND id=%s"
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (self.name, self.id))
            result = cursor.fetchone()
            if result:
                return result
            return {}
            
        except Exception as e:
            print(e)