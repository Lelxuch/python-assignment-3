# python-assignment-3

Title: Assignment 3

Python Flask web application with a database. In this project I used jwt technology to check user authorization. The authorization page finds '/login' and then checks if this user is in the database. Later it redirects to '/proteced' with a jwt key in the parameters. This page checks if the jwt key is correct and grants access.

## Installation

PyPI
```bash
pip install flask
pip install flask-sqlalchemy
pip install pyjwt
```

## Usage

Go to src folder and open main.py. First you need to do is to set your password for pgAdmin instead of root, and database name instead of pythonPractice in app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/pythonPractice'

```bash
cd src
python3 main.py
```

## Examples

### Case when jwt token is right

It returns "Hello, token which is provided is correct [your_token]"

### Case when jwt token is wrong


It returns "Hello, Could not verify the token"
