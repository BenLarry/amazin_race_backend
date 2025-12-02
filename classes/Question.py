from database import Database

class Question():
    def __init__(self, question, points, level, ID = None):
        self.db = Database()
        self.ID = ID
        self.question = question
        self.points = points
        self.level = level

        

    def get_question(self):
        if self.ID == None:
            return {"error": "ID:tä ei löydy"}
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
            print(result)
        except self.db.connector.errors.ProgrammingError as err:
            print(err)
            return {"error": "räätälöity virheilmoitus"}, 500
        except Exception as err:
            print(err)
            return {"error": "geneerinen virheilmoitus"}, 500    




    def select_game_questions(self):
        if self.ID == None:
            return {"error": "ID:tä ei löydy"}
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
            


            sql_update_questions = "INSERT INTO game_question(question_ID, answered) VALUES(%s, 0)"
            for question in questions:
                cursor.execute(sql_update_questions, (question['ID'],))
        except self.db.connector.errors.ProgrammingError as err:
            print(err)
            return {"error": "räätälöity virheilmoitus"}, 500
        except Exception as err:
            print(err)
            return {"error": "geneerinen virheilmoitus"}, 500    


        

        

        
ok = Question(1, 1, 1, 1)
ok.select_game_questions()
print(ok.get_question())