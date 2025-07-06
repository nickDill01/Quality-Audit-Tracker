from extensions import database # Import database from extensions.py

class Audit(database.Model): 
    __tablename__ = "audit"

    # Columns in the table
    id = database.Column(database.Integer, primary_key = True)
    title = database.Column(database.String(100), nullable = False)
    department = database.Column(database.String(50), nullable = False)
    date = database.Column(database.Date, nullable = False)
    status = database.Column(database.String(25), default = "Pending") # Pending, In Progress, Completed

class Finding(database.Model): 
    __tablename__ = "finding"
    
    # Columns in the table
    id = database.Column(database.Integer, primary_key = True)
    audit_id = database.Column(database.Integer, database.ForeignKey("audit.id"), nullable = False)
    description = database.Column(database.String(250), nullable = False)
    severity = database.Column(database.String(25), nullable = False) # Major, Minor
    status = database.Column(database.String(25), default = "Open")  # Open, Closed

class CAPA(database.Model):
    __tablename__ = "capa"
    
    # Columns in the table
    id = database.Column(database.Integer, primary_key = True)
    finding_id = database.Column(database.Integer, database.ForeignKey("finding.id"), nullable = False)
    action = database.Column(database.String(250), nullable = False)
    assignee = database.Column(database.String(50), nullable = False) # Contact assigned to handle actions
    due_date = database.Column(database.Date, nullable = False)
    status = database.Column(database.String(25), default = "In Progress") # In Progress, Completed