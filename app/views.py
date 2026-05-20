from app import app

@app.route("/")
def index():
    return "<h1>Hello world!</h1>"

@app.route("/about-us")
def about():
    return "We are cool!"