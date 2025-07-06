# Importing modules
from flask import Blueprint, request, jsonify
from extensions import database # Import database from extensions.py
from models import Audit, Finding, CAPA
from datetime import datetime

# Groups all API routes in single, reusable module. 
routes = Blueprint("routes", __name__)

# **** AUDIT FUNCTIONS ****

# Function to create new audit object. 
@routes.route("/audits", methods = ["POST"])
def create_audit():
    # Grabs JSON body of request. 
    data = request.json

    # Initializes new audit object. 
    audit = Audit(
        title = data["title"],
        department = data["department"],
        date = datetime.strptime(data["date"], "%Y-%m-%d").date(),
        status = data.get("status", "Pending")
    )

    # Adds audit to the database. 
    database.session.add(audit)
    database.session.commit()

    # Returns confirmation message with HTTP status 201 for created. 
    return jsonify({"message": "Audit Successfully Created"}), 201

# Function to return all audit objects. 
@routes.route("/audits", methods = ["GET"])
def get_audits():
    # Retrieves all audit records. 
    audits = Audit.query.all()

    # Converts audit object to a list with its attributes as separate items. 
    result = [
        {
            "id": audit.id,
            "title": audit.title,
            "department": audit.department,
            "date": audit.date.isoformat(),
            "status": audit.status
        }
        for audit in audits
    ]

    # Returns list as a JSON with status code 200 for OK status. 
    return jsonify(result), 200

# Function to return a single audit object based on ID. 
@routes.route("/audits/<int:id>", methods = ["GET"])
def get_audit(id):
    # Searches for audit object, returns 404 error if not found. 
    audit = Audit.query.get_or_404(id)

    # Returns audit object as a JSON with status code 200 for OK status. 
    return jsonify(
        {
            "id": audit.id,
            "title": audit.title,
            "department": audit.department,
            "date": audit.date.isoformat(),
            "status": audit.status
        }
    ), 200

# Function to update a single audit object based on ID. 
@routes.route("/audits/<int:id>", methods = ["PUT"])
def update_audit(id):
    # Searches for audit object, returns 404 error if not found. 
    audit = Audit.query.get_or_404(id)

    # Grabs JSON body of request.
    data = request.json

    # Updates fields provided, otherwise leaves them unchanged. 
    audit.title = data.get("title", audit.title)
    audit.department = data.get("department", audit.department)
    audit.date = data.get("date", audit.date)
    audit.status = data.get("status", audit.status)

    # Saves and confirms update to the database with confirmation message. 
    database.session.commit()
    return jsonify({"message": "Audit Successfully Updated"}), 200

# Function to delete a single audit object based on ID. 
@routes.route("/audits/<int:id>", methods = ["DELETE"])
def delete_audit(id):
    # Searches for audit object, returns 404 error if not found.
    audit = Audit.query.get_or_404(id)

    # Deletes audit object and updates the database. 
    database.session.delete(audit)
    database.session.commit()

    # Returns confirmation message. 
    return jsonify({"message": "Audit Successfully Deleted"}), 200

# **** FINDINGS FUNCTIONS ****

# Function to create a new finding for an audit object. 
@routes.route("/findings", methods = ["POST"])
def create_finding():
    # Grabs JSON body of request.
    data = request.json

    # Creates a new finding object based on audit_id from data. 
    finding = Finding(
        audit_id = data["audit_id"],
        description = data["description"],
        severity = data["severity"],
        status = data.get("status", "Open")
    )

    # Updates database with new finding. 
    database.session.add(finding)
    database.session.commit()

    # Returns confirmation message. 
    return jsonify({"message": "Finding Successfully Created"}), 201

# Function returns all findings for a single audit object based on ID. 
@routes.route("/findings/<int:audit_id>", methods = ["GET"])
def get_findings_for_audit(audit_id):
    # Uses filter to find findings for specific audit object. 
    findings = Finding.query.filter_by(audit_id = audit_id).all()

    # Converts findings object to a list with each attribute as separate items. 
    result = [
        {
            "id": finding.id,
            "description": finding.description,
            "severity": finding.severity,
            "status": finding.status
        }
        for finding in findings
    ]

    # Returns list as a JSON. 
    return jsonify(result), 200

# **** CAPA FUNCTIONS ****

# Function to create a new CAPA object related to a Finding object. 
@routes.route("/capas", methods = ["POST"])
def create_capa():
    # Grabs JSON body of request.
    data = request.json

    # Creates a new CAPA object based on Finding ID. 
    capa = CAPA(
        finding_id = data["finding_id"],
        action = data["action"],
        assignee = data["assignee"],
        due_date = datetime.strptime(data["due_date"], "%Y-%m-%d").date(),
        status = data.get("status", "Pending")
    )

    # Updates database with new CAPA. 
    database.session.add(capa)
    database.session.commit()

    # Returns confirmation message. 
    return jsonify({"message": "CAPA Successfully Created"}), 201

# Function updates CAPAs for finding object based on ID. 
@routes.route('/capas/<int:capa_id>', methods=['PUT'])
def update_capa(capa_id):
    # Grabs JSON body. 
    data = request.get_json()

    # Gets CAPA object based on ID. 
    capa = CAPA.query.get(capa_id)
    if not capa:
        return jsonify({"error": "CAPA Not found"}), 404

    # Sets CAPA object based on action, assignee, and due date. 
    capa.action = data.get('action', capa.action)
    capa.assignee = data.get('assignee', capa.assignee)
    due_date = data.get('due_date')
    if due_date:
        capa.due_date = datetime.strptime(due_date, '%Y-%m-%d').date()

    # Updates database with CAPA changes. 
    database.session.commit()
    return jsonify({"message": "CAPA Successfully Updated"})

# Function returns all CAPAs for a single finding object based on ID.
@routes.route("/capas/<int:finding_id>", methods = ["GET"])
def get_capas_for_finding(finding_id):
    # Uses filter to find CAPAs for specific finding object. 
    capas = CAPA.query.filter_by(finding_id = finding_id).all()

    # Converts CAPAs object to a list with each attribute as separate items.
    result = [
        {
            "id": capa.id,
            "action": capa.action,
            "assignee": capa.assignee,
            "due_date": capa.due_date.isoformat(),
            "status": capa.status
        }
        for capa in capas
    ]

    # Returns list as a JSON.
    return jsonify(result), 200 