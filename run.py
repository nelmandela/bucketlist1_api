import os

from app import create_app

# print(os.environ.get("FLASK_CONFIG"))

# create app instance
# app = create_app(os.getenv('FLASK_CONFIG'))

app = create_app('development')

if __name__ == "__main__":
    app.run()
