from app import app, models, QUEST
from flask import request, Response, url_for
from http import HTTPStatus
import json
import random


@app.post("/questions/create")
def create_question():
    data = request.get_json()
    title = data["title"]
    description = data["description"]
    question_type = data["type"]
    question_id = len(QUEST)
    if question_type == "ONE-ANSWER":
        answer = data["answer"]  # expect string
        if not models.OneAnswer.is_valid(answer):
            return Response(
                "answer must be string",
                status=HTTPStatus.BAD_REQUEST,
            )
        question = models.OneAnswer(question_id, title, description, answer, reward=1)
    elif question_type == "MULTIPLE-CHOICE":
        choices = data["choices"]  # list of choices
        answer = data["answer"]  # expect number
        if not models.MultipleChoice.is_valid(answer, choices):
            return Response(
                "answer must be int, choices must be list. 0<=answer<=len(choices)",
                status=HTTPStatus.BAD_REQUEST,
            )
        question = models.MultipleChoice(
            question_id, title, description, answer, choices, reward=1
        )
    else:
        return Response(
            "Question must be of ONE-ANSWER type or MULTIPLE-CHOICE",
            status=HTTPStatus.BAD_REQUEST,
        )

    QUEST.append(question)
    return Response(
        json.dumps(
            {
                "id": question.id,
                "title": question.title,
                "description": question.description,
                "type": question_type,
                "answer": question.answer,
            }
        ),
        status=HTTPStatus.CREATED,
        mimetype="application/json",
    )


@app.get("/questions/random")
def get_random_question():
    if len(QUEST) == 0:
        return Response(
            f"No questions in the database. "
            f'Please, <a href="{url_for("create_question")}">add some questions first</a>',
            status=HTTPStatus.NOT_FOUND,
        )
    question = QUEST[random.randint(0, len(QUEST) - 1)]
    return Response(
        json.dumps(
            {
                "id": question.id,
                "reward": question.reward,
            }
        ),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )


@app.post("/questions/<question_id>/solve")
def solve_question():
    pass
