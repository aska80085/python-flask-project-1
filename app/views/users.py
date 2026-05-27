from app import app, models, USERS
from flask import request, Response
from http import HTTPStatus
import json


@app.post("/user/create")
def user_create():
    data = request.get_json()
    user_id = len(USERS)
    first_name = data["first_name"]
    last_name = data["last_name"]
    phone = data["phone"]
    email = data["email"]

    if not models.User.is_valid_email(email):
        return Response(status=HTTPStatus.BAD_REQUEST)
    if not models.User.is_valid_phone(phone):
        return Response(status=HTTPStatus.BAD_REQUEST)
    user = models.User(user_id, first_name, last_name, phone, email)

    USERS.append(user)
    return Response(
        json.dumps(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone": user.phone,
                "email": user.email,
                "score": user.score,
            }
        ),
        HTTPStatus.CREATED,
        mimetype="application/json",
    )


@app.get("/user/<int:user_id>")
def get_user(user_id):
    if not models.User.is_valid_id(user_id):
        return Response(status=HTTPStatus.NOT_FOUND)
    user = USERS[user_id]
    return Response(
        json.dumps(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone": user.phone,
                "email": user.email,
                "score": user.score,
            }
        ),
        HTTPStatus.CREATED,
        mimetype="application/json",
    )
