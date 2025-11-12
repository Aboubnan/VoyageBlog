from flask import Flask

# Initialisation du Controleur (C)
app = Flask(__name__)

@app.route('/')
def hello_world():
    # Vue (V) minimale
    return '<h1>Bienvenue sur notre Blog de Voyage !</h1>'

if __name__ == '__main__':
    app.run(debug=True)