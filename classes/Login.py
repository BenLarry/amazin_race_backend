from classes.Database import Database

class Login():
    def __init__(self, name, id):
        self.id = id
        self.name = name
        self.db = Database().get_conn()


    def create_player(self):
        try:
            sql = "insert into player (name) VALUES(%s)"
            cursor = self.db.cursor()
            cursor.execute(sql, (self.name,))
            return {
                "id": cursor.lastrowid,
                "name": self.name
            }
        except Exception as e:
            print(e)

    def login_player(self):
        try:
            pass
        except Exception as e:
            print(e)