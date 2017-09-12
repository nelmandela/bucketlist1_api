import os

from flask import jsonify

from app import create_app

# create app instance
# app = create_app(os.environ.get('FLASK_CONFIG'))

app = create_app('development')
# basic test route
@app.route('/users', methods=['GET'])
def get_users():
    response = jsonify({"message": "this are users"})
    response.status_code = 200
    return response

if __name__ == "__main__":
    app.run()
