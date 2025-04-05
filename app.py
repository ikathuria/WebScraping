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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
