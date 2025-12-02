from flask import Flask, request
from flask_cors import CORS
from classes.Login import Login

app = Flask(__name__)
CORS(app)



@app.route("/")
def helloWorld():
  return "Hello, cross-origin-world!"

@app.route("/login/<name>", methods=['GET', 'POST'])
def login(name):
  if request.method == 'GET':
    return f"GET METHOD LOGIN {name}"
  if request.method == 'POST':
    x = Login("abc")
    
    print(x.create_player())
    return f"POST METHOD LOGIN {name}"

  





if __name__ == "__main__":
    app.run(use_reloader=True, host='127.0.0.1', port=3000)