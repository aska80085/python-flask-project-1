from email_phone_validator import validate_email, validate_phone
from app import USERS, EXPRS
from abc import ABC, abstractmethod


class User:
    def __init__(self, id, first_name, last_name, phone, email, score=0):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.score = score

    @staticmethod
    def is_valid_email(email):
        return validate_email(email)

    @staticmethod
    def is_valid_phone(phone):
        return validate_phone(phone)

    @staticmethod
    def is_valid_id(user_id):
        if user_id < 0 or user_id >= len(USERS):
            return False
        return True

    def increase_score(self, amount=1):
        self.score += amount


class Expression:
    def __init__(self, id, operation, *values, reward=None):
        self.id = id
        self.operation = operation
        self.values = values
        self.answer = self.__evaluate()
        if reward is None:
            reward = len(values) - 1
        self.reward = reward

    def to_string(self):
        expr_str = str(self.values[0]) + "".join(
            " " + self.operation + " " + str(value) for value in self.values[1:]
        )
        return expr_str

    def __evaluate(self):
        return eval(self.to_string())

    @staticmethod
    def is_valid_id(expr_id):
        if expr_id < 0 or expr_id >= len(EXPRS):
            return False
        return True


class Question(ABC):
    def __init__(self, id, title, description, reward=None):
        self.id = id
        self.title = title
        self.description = description
        if reward is None:
            reward = 1
        self.reward = reward

    @property
    @abstractmethod
    def answer(self):
        pass


class OneAnswer(Question):
    def __init__(self, id, title, description, answer: str, reward=None):
        super().__init__(id, title, description, reward)
        if self.is_valid(answer):
            self._answer = answer
        else:
            self._answer = None

    @property
    def answer(self):
        return self._answer

    @answer.setter
    def answer(self, value: str):
        if self.is_valid(value):
            self._answer = value

    @staticmethod
    def is_valid(answer):
        return isinstance(answer, str)


class MultipleChoice(Question):
    def __init__(self, id, title, description, answer: int, choices: list, reward=None):
        super().__init__(id, title, description, reward)
        if self.is_valid(answer, choices):
            self.choices = choices
            self._answer = answer
        else:
            self.choices = None
            self._answer = None

    @property
    def answer(self):
        return self._answer

    @answer.setter
    def answer(self, value: int):
        if self.is_valid(value, self.choices):
            self._answer = value

    @staticmethod
    def is_valid(answer, choices):
        if (
            not isinstance(answer, int)
            or not isinstance(choices, list)
            or answer < 0
            or answer >= len(choices)
        ):
            return False
        return True
