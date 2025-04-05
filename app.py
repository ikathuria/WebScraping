from flask import Flask, jsonify
from flask import request, render_template
from scripts.orcid_papers import fetch_orcid_works
from scripts.github_pins import ScrapeGitHubRepos

UPLOAD_DIR = 'static/data/'

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html', page="home")


@app.route('/github', defaults={'username': ''}, methods=["GET", "POST"])
@app.route('/github/<username>')
def github_pins(username):
    if request.method == "POST":
        username = request.form['git-user']
        if username != '':
            data = ScrapeGitHubRepos(username).scrape_github()
            return jsonify(data)

    if username != '':
        data = ScrapeGitHubRepos(username).scrape_github()
        return jsonify(data)

    return render_template('github.html', page="github")


@app.route('/orcid', defaults={'username': ''}, methods=["GET", "POST"])
@app.route('/orcid/<username>')
def orcid_works(username):
    if request.method == "POST":
        username = request.form['orcid-user']
        if username != '':
            data = fetch_orcid_works(username)
            return jsonify(data)

    if username != '':
        data = fetch_orcid_works(username)
        return jsonify(data)

    return render_template('orcid.html', page="orcid")


# @app.route('/justdial', methods=["GET", "POST"])
# def justdial():
#     if request.method == "POST":
#         topic = request.form['topic']
#         cities = request.form['cities']

#         # making sure its not empty
#         if topic != '' and cities != '':
#             topic = topic.lower()
#             cities = [i.lower() for i in cities.split('\n')]
#             data = scrape_justdial(topic, cities)
#             df = pd.DataFrame.from_dict(data, orient='index').T
#             print(df)
#             df.to_csv(UPLOAD_DIR + 'justdial.csv', index=False)

#             return send_from_directory(UPLOAD_DIR, 'justdial.csv')

    # return render_template('justdial.html', page="justdial")


@app.route('/amazon')
def amazon():
    return render_template('amazon.html', page="amazon")


@app.route('/myntra')
def myntra():
    return render_template('myntra.html', page="myntra")


@app.route('/google')
def google():
    return render_template('google.html', page="google")


if __name__ == "__main__":
    app.run()
