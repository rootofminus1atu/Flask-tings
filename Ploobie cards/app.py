from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/display")
def display():
    return render_template('display.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/shop")
def shop():
    return render_template('shop.html')


if __name__ == "__main__":
    app.run(debug=True)
