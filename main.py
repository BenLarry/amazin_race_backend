from flask import Flask, request
from flask_cors import CORS
from classes.Player import Player
from classes.Question import Question
from classes.Game import Game

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
    pass
    #user = Login(params["name"], params["ID"]).login_player()
    #return user
  if request.method == 'POST':
    return params
    #x = Login(name, 1)

@app.route("/game", methods=['GET', 'POST'])
def game():
  params = request.args.to_dict()
  
  if request.method == 'GET':
    game = Game(params["player_ID"])
    return game.get_game()
  if request.method == 'POST':
    game = Game(params["player_ID"])
    return game.create_game()
    

if __name__ == "__main__":
    app.run(use_reloader=True, host='127.0.0.1', port=3000)