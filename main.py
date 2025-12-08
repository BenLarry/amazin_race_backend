from flask import Flask, request
from flask_cors import CORS
from classes.Player import Player
from classes.Question import Question
from classes.Game import Game
from classes.Highscore import Highscore


app = Flask(__name__)
CORS(app)

@app.route("/")
def helloWorld():
  return "Hello, cross-origin-world!"

#args 
@app.route("/login", methods=['GET', 'POST'])
def login():
  params = request.args.to_dict()

  if request.method == 'GET':
    user = Player(params["name"], params["player_ID"]).login_player()
    return user
  if request.method == 'POST':
    user = Player(params["name"]).create_player()
    return user

@app.route("/game", methods=['GET', 'POST'])
def game():
  params = request.args.to_dict()
  
  if request.method == 'GET':
    game = Game(params["player_ID"])
    return game.get_game()
  if request.method == 'POST':
    game = Game(params["player_ID"])
    return game.create_game()
  


@app.route("/highscore", methods=['GET', 'POST'])
def highscore():
  params = request.args.to_dict()

  if request.method == 'GET':
    highscore = Highscore(params["player_ID"]) 
    return highscore.get_highscore()
  if request.method == 'POST':
    pass

@app.route("/question", methods = ['GET', 'POST'])
def question():
  params = request.args.to_dict()

  if request.method == 'GET':
    question = Question()
    return question.get_question()
  if request.method =='POST':
    question = Question()
    return question.set_question_answered(params['question_ID'])
  


if __name__ == "__main__":
    app.run(use_reloader=True, host='127.0.0.1', port=3000)