class User:
    def __init__(self, id, first_name, last_name, phone, email, score=0):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.score = score


class Expression:
    def __init__(self, id, operation, *values):
        self.id = id
        self.operation = operation
        self.values = values
        self.answer = self.__evaulate()

    def to_string(self):
        expr_str = str(self.values[0]) + "".join(
            " " + self.operation + " " + str(value) for value in self.values[1:]
        )
        return expr_str

    def __evaulate(self):
        return eval(self.to_string())
