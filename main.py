from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def helloWorld():
  return "Hello, cross-origin-world!"

if __name__ == "__main__":
    app.run(use_reloader=True, host='127.0.0.1', port=3000)