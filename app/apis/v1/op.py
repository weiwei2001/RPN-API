import json
from flask.views import MethodView
from app.core.models import Stack


class OpView(MethodView):
    OPERANDS = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: a / b,
    }

    def get(self):
        return {"operands": [*self.OPERANDS]}

    def post_stack(self, op, stack_id):
        if op not in self.OPERANDS.keys():
            return f"op {op} Not found", 404

        with open("./app/core/resources/data.json", 'r') as json_data_file:
            stacks = json.load(json_data_file)

        stack = stacks.get(stack_id)
        if not stack:
            return f"stack id {stack_id} Not found", 404

        if len(stack) > 1:
            new_stack = stack[0:len(stack)-2]
            new_stack.append(self.OPERANDS[op](stack[len(stack) - 2], stack[len(stack) - 1]))
        else:
            new_stack = stack

        stacks[stack_id] = new_stack

        with open("./app/core/resources/data.json", 'w') as json_data_file:
            json_data_file.write(json.dumps(stacks))

        return Stack(stack_id, stacks[stack_id]).serialize()
