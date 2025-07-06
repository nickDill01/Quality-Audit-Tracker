from app import create_app
from extensions import database # Import database from extensions.py
from models import Audit, Finding, CAPA

app = create_app()

with app.app_context():
    database.create_all()
    print("Database Initialized")