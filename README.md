**How to run and debug project in local env?**

1. create a repo for all python projects and install virtualenv python on Win/Linux
cd ~
mkdir dev
cd dev
mkdir .virtualenvs
pip install virtualenv

2. clone a python project from git, as
git clone git@github.com:weiwei2001/RPN-API.git
cd RPN-API

3. create an environment for RPN-API
    - on Windows: 
        virtualenv --python="/c/Program Files (x86)/Python/Python3.7/python.exe" ../.virtualenvs/RPN-API

    - on Linux:
        virtualenv ../.virtualenvs/RPN-API

4. activate virtualenv:
source activate ../.virtualenvs/RPN-API

5. install libs:
pip install -r requirements.txt

7. Run server:
python wsgi.py run

9. Tests
    - tests with unittest: python -m unittest tests.test_http.TestRPN
    - tests with curl:
        - Get a list of all operand: curl -X 'GET' 'http://127.0.0.1:5000/rpn/op' -H 'accept: application/json'
        - List the available stacks: curl -X 'GET'  'http://127.0.0.1:5000/rpn/stack' -H 'accept: application/json'
        - Create a new stack: curl -X 'POST' 'http://127.0.0.1:5000/rpn/stack' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{ "value": [ 1, 2, 3 ] }'
        - Get a stack: curl -X 'GET' 'http://127.0.0.1:5000/rpn/stack/134a2dfd-e826-47be-ba8b-1555d2f54956' -H 'accept: application/json'
        - Push a new value to a stack: curl -X 'POST' 'http://127.0.0.1:5000/rpn/stack/134a2dfd-e826-47be-ba8b-1555d2f54956' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{ "value": 1 }'
        - Apply an operand to a stack: curl -X 'POST' 'http://127.0.0.1:5000/rpn/op/%2B/stack/134a2dfd-e826-47be-ba8b-1555d2f54956' -H 'accept: application/json'
        - Delete a stack: curl -X 'DELETE''http://127.0.0.1:5000/rpn/stack/134a2dfd-e826-47be-ba8b-1555d2f54956' -H 'accept: application/json'

10. Release the current version on local:
$ cd RPN-API
$ git checkout master
$ git pull
$ git tag rpn-v1.0.0
$ git push origin rpn-v1.0.0
