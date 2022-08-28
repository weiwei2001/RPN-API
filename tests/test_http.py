import json
from unittest import TestCase
from app.app_file import create_app


class TestRPN(TestCase):
    def setUp(self):
        # Init app
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.testing = True
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def test_rpn(self):
        # Get all the operand
        response = self.client.get(
            "/rpn/op",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"operands": ["+", "-", "*", "/"]})

        # List the available stacks
        response = self.client.get(
            "/rpn/stack",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json(), {
                "stacks": [
                    {"id": "42395709-0b76-4890-8784-2ef6a00703f0", "value": [1, 2, 3]},
                    {"id": "1c16e6f9-a44e-4b7e-a5bf-558fdaf5c9ba", "value": [15, 9, 10]}
                ]
            }
        )

        # create a new stack
        response = self.client.post(
            "/rpn/stack",
            data=json.dumps(
                dict(value=[1, 2, 3, 4, 5])),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        new_stack_id = response.get_json()["id"]
        self.assertEqual(response.get_json(), {"id": new_stack_id, "value": [1, 2, 3, 4, 5]})

        # Push a new value to a stack
        response = self.client.post(
            f"/rpn/stack/{new_stack_id}",
            data=json.dumps(
                dict(value=6)),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"id": new_stack_id, "value": [1, 2, 3, 4, 5, 6]})

        # Apply an operand to a stack
        response = self.client.post(
            f"/rpn/op/+/stack/{new_stack_id}",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"id": new_stack_id, "value": [1, 2, 3, 4, 11]})

        # get a stack
        response = self.client.get(
            f"/rpn/stack/{new_stack_id}",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"id": new_stack_id, "value": [1, 2, 3, 4, 11]})

        # delete a stack
        response = self.client.delete(
            f"/rpn/stack/{new_stack_id}",
        )
        self.assertEqual(response.status_code, 204)
