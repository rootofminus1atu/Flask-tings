from flask import Flask, render_template, request

app = Flask(__name__)


subscribers = []


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/about")
def about():
    names = ["Donald", "Joe", "Hillary"]
    return render_template('about.html', names=names)


@app.route("/subscribe")
def subscribe():
    return render_template('subscribe.html')


@app.route("/form", methods=["POST"])
def form():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    subscribers.append(f"{first_name} {last_name} || {email}")
    
    return render_template(
        'form.html', subscribers=subscribers)


if __name__ == "__main__":
    app.run(debug=True)

# hi future me, to start the server type:
# flask run
#
# if that doesn't work, type:
# set FLASK_DEBUG=1
# set FLASK_APP=app.py
# flask run
#
# or even
# set FLASK_ENV=development
# but apparently this is deprecated
#
# now it should definiely work!
#
#
# ok sometimes python app.py has to be used