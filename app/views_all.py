from app import app, USERS, EXPRS, QUEST


@app.route("/")
def index():
    response = f"<h1>Hello world!</h1>{USERS}<br>{EXPRS}<br>{QUEST}<br>"
    return response
