"""set FLASK_ENV=development"""

from flask import Flask
from flask import request, render_template, Response, send_from_directory, url_for
import json
import pandas as pd
from justdial import scrape_justdial

UPLOAD_DIR = 'static/data/'

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html', page="home")


@app.route("/justdial/")
def justdial():
    return render_template('justdial.html', page="justdial")


@app.route('/justdial/', methods=["POST"])
def get_justdial_input():
    topic = request.form['topic']
    cities = request.form['cities']

    # making sure its not empty
    if topic != '' and cities != '':
        topic = topic.lower()
        cities = cities.split('\n')
        data = scrape_justdial(topic, cities)
        df = pd.DataFrame.from_dict(data, orient='index').T
        df.to_csv(UPLOAD_DIR + 'justdial.csv', index=False)

        return send_from_directory(UPLOAD_DIR, 'justdial.csv')

    else:
        return render_template('justdial.html', page="justdial")


@app.route("/amazon/")
def amazon():
    return render_template('amazon.html', page="amazon")


@app.route("/myntra/")
def myntra():
    return render_template('myntra.html', page="myntra")


@app.route("/google/")
def google():
    return render_template('google.html', page="google")


if __name__ == "__main__":
    app.run()