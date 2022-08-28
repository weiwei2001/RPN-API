import uuid
import json
from flask import jsonify
from flask.views import MethodView
from connexion import request
from app.core.models import Stack


class StackView(MethodView):
    def get_list(self):
        with open("./app/core/resources/data.json", 'r') as json_data_file:
            stacks = json.load(json_data_file)

        return jsonify({
            "stacks":
                [Stack(k, v).serialize() for k, v in stacks.items()]
        })

    def get(self, stack_id):
        with open("./app/core/resources/data.json", 'r') as json_data_file:
            stacks = json.load(json_data_file)

        stack = stacks.get(stack_id)
        if not stack:
            return f"stack id {stack_id} Not found", 404

        return Stack(stack_id, stacks[stack_id]).serialize()

    def delete(self, stack_id):
        with open("./app/core/resources/data.json", 'r') as json_data_file:
            stacks = json.load(json_data_file)

        stack = stacks.get(stack_id)
        if not stack:
            return "OK", 204

        del stacks[stack_id]

        with open("./app/core/resources/data.json", 'w') as json_data_file:
            json_data_file.write(json.dumps(stacks))

        return "OK", 204

    # Push a new value to a stack
    def post(self, stack_id):
        with open("./app/core/resources/data.json", 'r') as json_data_file:
            stacks = json.load(json_data_file)

        body = request.json
        new_value = body.get("value")
        stack = stacks.get(stack_id)
        if not stack:
            return f"stack id {stack_id} Not found", 404
        stack.append(new_value)
        stacks[stack_id] = stack

        with open("./app/core/resources/data.json", 'w') as json_data_file:
            json_data_file.write(json.dumps(stacks))

        return Stack(stack_id, stacks[stack_id]).serialize()

    # Create a new stack
    def create(self):
        with open("./app/core/resources/data.json", 'r') as json_data_file:
            stacks = json.load(json_data_file)

        body = request.json
        new_value = body.get("value")
        stack_id = uuid.uuid4()
        stacks[str(stack_id)] = new_value

        with open("./app/core/resources/data.json", 'w') as json_data_file:
            json_data_file.write(json.dumps(stacks))

        return Stack(stack_id, new_value).serialize(), 201
