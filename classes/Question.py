from classes.Database import Database

class Question():
    def __init__(self, game_ID, points ="", level = "" ,question = "", ID = None):
        self.db = Database()
        self.ID = ID
        self.game_ID = game_ID
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

