from flask import Flask, request
from flask_cors import CORS
from classes.Player import Player
from classes.Question import Question
from classes.Game import Game
from classes.Highscore import Highscore
from classes.Airport import Airport


app = Flask(__name__)
CORS(app)

@app.route("/")
def helloWorld():
  return "Hello, cross-origin-world!"

#args 
@app.route("/login", methods=['GET', 'POST'])
def login():
  params = request.args.to_dict()
  if not params:
    return {"error": "Not found"}, 404
  if request.method == 'GET':
    user = Player(params["name"], params["player_ID"]).login_player()
    return user
  if request.method == 'POST':
    user = Player(params["name"]).create_player()
    return user

@app.route("/game", methods=['GET', 'POST'])
def game():
  params = request.args.to_dict()
  if not params:
    return {"error": "Not found"}, 404
  if request.method == 'GET':
    game = Game(params["player_ID"])
    return game.get_game()
  if request.method == 'POST':
    game = Game(params["player_ID"])
  if "ident" in params:
    return game.move_player(params["ident"], params["game_ID"])
  if "amount" in params:
    return game.add_points(int(params["amount"]), params["game_ID"])
  return game.create_game()
  


@app.route("/highscore", methods=['GET', 'POST'])
def highscore():
  params = request.args.to_dict()
  if request.method == 'GET':
    highscore = Highscore()
  if 'player_ID' in params: 
    return highscore.get_highscore_params(params['player_ID'])
  return highscore.get_highscore()

@app.route("/question", methods = ['GET', 'POST'])
def question():
  params = request.args.to_dict()
  if request.method == 'GET':
    question = Question()
    return question.get_question(params["game_ID"])
  if request.method =='POST':
    if not params:
      return {"error": "Not found"}, 404
    question = Question()
    return question.set_question_answered(params['question_ID'])
  

@app.route("/airport", methods = ['GET', 'POST'])
@app.route("/airport/<cost>")
def airport(cost = None):
  params = request.args.to_dict()
  if not params:
    return {"error": "Not found"}, 404
  if request.method == 'GET' and cost != None:
    airport = Airport(params['game_ID'])
    return airport.calculate_co2(params["ident"])
  if request.method =='GET':
    airport = Airport(params['game_ID'])
    return airport.get_airport()
  if request.method == 'POST':
    airport = Airport(params['game_ID'])  
  if "amount" in params:
    return airport.update_co2(params["amount"])
  if "ident" in params:
    return airport.set_airport_visited(params['ident'])
    





if __name__ == "__main__":
    app.run(use_reloader=True, host='127.0.0.1', port=3000)