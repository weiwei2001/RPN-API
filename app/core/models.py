class Stack:
    id = ""
    value = ""

    def __init__(self, id, value):
        self.id = id
        self.value = value

    def serialize(self):
        return {
            "id": self.id,
            "value": self.value,
        }
