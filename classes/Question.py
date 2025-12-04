from database import Database
from Login import Login
from Game import Game

class Question():
    def __init__(self, points ="", level = "" ,question = "", ID = None):
        self.db = Database()
        self.ID = ID
        self.question = question
        self.points = points
        self.level = level

        

    def get_question(self):
        try:
            conn = self.db.get_conn()
            cursor = conn.cursor(dictionary=True)
            sql = """ 
            SELECT question.ID, question.question, question.points, answer.choice, answer.is_correct
            FROM (
                SELECT game_question.question_ID 
                FROM game_question
                INNER JOIN question ON game_question.question_ID = question.ID
                WHERE game_question.answered = 0
                ORDER BY RAND()
                LIMIT 1
            ) AS random_question
            INNER JOIN question ON random_question.question_ID = question.ID
            INNER JOIN question_answer ON question.ID = question_answer.question_ID
            INNER JOIN answer ON question_answer.answer_ID = answer.ID
            ORDER BY answer.ID;
            """
            cursor.execute(sql)
            result = cursor.fetchall()
            formatted_question = {
                "ID": result[0]["ID"],
                "question": result[0]["question"],
                "points": result[0]["points"],
                "choice_1": {
                    "ID": 1,
                    "answer": result[0]["choice"],
                    "is_correct": result[0]["is_correct"]
                },
                "choice_2": {
                    "ID": 2,
                    "answer": result[1]["choice"],
                    "is_correct": result[1]["is_correct"]
                },
                "choice_3": {
                    "ID": 3,
                    "answer": result[2]["choice"],
                    "is_correct": result[2]["is_correct"]
                },
            }
            return formatted_question
        except self.db.connector.errors.ProgrammingError as err:
            print(err)
            return {"error": "räätälöity virheilmoitus"}, 500
        except Exception as err:
            print(err)
            return {"error": "geneerinen virheilmoitus"}, 500    




    def select_game_questions(self, game_id):
        if game_id == '':
            return {"error": "game_ID:tä ei löydy"}
        try:
            conn = self.db.get_conn()
            cursor = conn.cursor(dictionary=True)
            sql_selected_questions = """
            (
                SELECT * FROM question WHERE level = 1 ORDER BY RAND() LIMIT 10
            )
            UNION ALL
            (
            SELECT * FROM question WHERE level = 2 ORDER BY RAND() LIMIT 10 
            )
            UNION ALL
            (
                SELECT * FROM question WHERE level = 3 ORDER BY RAND() LIMIT 10
            )
            """
            cursor.execute(sql_selected_questions)
            questions = cursor.fetchall()
            


            sql_update_questions = "INSERT INTO game_question(question_ID, game_id, answered) VALUES(%s, %s, 0)"
            for question in questions:
                cursor.execute(sql_update_questions, (question['ID'], game_id))
        except self.db.connector.errors.ProgrammingError as err:
            print(err)
            return {"error": "räätälöity virheilmoitus"}, 500
        except Exception as err:
            print(err)
            return {"error": "geneerinen virheilmoitus"}, 500    


        

        
pelaaja1 = Login("moi", 6)

peli = Game(pelaaja1.id, "EU")


okei = peli.get_game(pelaaja1.id)

print("--------------------------------------")
print(okei)
print("----------------------------------------")     
ok = Question()
jees = ok.select_game_questions(okei['ID'])

kysymys= ok.get_question()


for i in range(1, 4): 
    print(kysymys[f"choice_{i}"]["answer"])