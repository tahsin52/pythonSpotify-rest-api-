from base_file import lastFmSpotify
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/name/<user>')
def hello(user):
    return render_template('index.html', user=user)

if __name__ == '__main__':
    d = lastFmSpotify()
    d.fetch_songs_from_lastFm()

    app.run(debug=True)
