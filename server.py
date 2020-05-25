from flask import Flask, render_template, request
from calculation import calculate
from generation import generate
import os
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from werkzeug.utils import secure_filename
app = Flask(__name__)


def make_result_string(result):
    answer = ''
    for value in result:
        answer += '<p>' + value + '</p>'
    return answer


@app.route("/", methods=["GET", "POST"])
def get_home():
    if request.method == "POST":
        if not os.path.exists('uploads'):
            os.mkdir("uploads")

        if request.form["mode"] == 'file':

            input_file = request.files['input_file']
            filename = secure_filename(input_file.filename)
            path = os.path.join('uploads', filename)
            input_file.save(path)

        else:

            input_site = request.form['site']
            response = requests.get(input_site)
            if not response.ok:
                raise ValueError
            soup = BeautifulSoup(response.text, 'lxml')
            paragraphs = soup.find_all('body')
            url = urlparse(input_site)
            filename = os.path.basename(url.path)
            path = os.path.join('uploads', filename)
            with open(path, 'w') as file:
                file.write(paragraphs[0].text)

        input_depth = request.form["depth"]
        input_count = request.form["count"]
        input_verbosity = request.form["verbosity"]

        calculate(path, int(input_depth))
        result = generate(int(input_depth), int(input_count), int(input_verbosity))

        message_start = '<html> \n <body> \n'
        message_end = '\n <p><a href="/">Back</a> \n </body> \n </html>'
        return message_start + make_result_string(result) + message_end

    return render_template("home.html")


@app.route("/about")
def get_about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)

