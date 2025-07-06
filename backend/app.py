from flask import Flask # Flask is used to initialize the app
from flask_sqlalchemy import SQLAlchemy # SQLAlchemy interacts with SQL databases
from flask_cors import CORS # CORS allows frontend to backend requests
from routes import routes # Imports routes from routes.py
from extensions import database # Import database from extensions.py

# Create App: Creates Flask app
def create_app(): 
    app = Flask(__name__) # Initializes new Flask app
    CORS(app) # Enables CORS for the Flask app

    # Database Configuration (SQLite)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///audit_tracker.db" # Connects SQLAlchemy to SQLite Database
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # Disables Flask's event notification system for SQLAlchemy

    database.init_app(app)

    # Registers blueprint of routes defined in routes.py
    app.register_blueprint(routes)

    @app.route("/") # Tells Flask to execute the function when the root URL is accessed
    # Home Function: Returns message as JSON response to check the API running status
    def home(): 
        return {"message": "Audit Tracker API is Running"}

    return app

# Ensures the file runs only when directly executed
if __name__ == "__main__":
    app = create_app() # Initializes App instance
    app.run(debug = True) # Starts Flask development server
