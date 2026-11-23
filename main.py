from flask import Flask
from database import DatabaseHandler
from blueprints.public import public
from blueprints.private import private

app = Flask(__name__)
app.secret_key = "FHduv47fwDHJb"

db = DatabaseHandler()
db.createTables()

app.register_blueprint(public)
app.register_blueprint(private)




if __name__ == "__main__":
    app.run(debug=True)
