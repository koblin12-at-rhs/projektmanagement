from datetime import datetime

from app import db


class EmailTemplate(db.Model):
    __tablename__ = "email_templates"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(255), unique=True, nullable=False)
    subject = db.Column(db.String(500), nullable=False)
    body_text = db.Column(db.Text, nullable=False)
    body_html = db.Column(db.Text, nullable=True)
    available_variables = db.Column(db.JSON, nullable=True)
    language = db.Column(db.String(5), default="de")
    category = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


EMAIL_TEMPLATES_DEFAULTS = {
    "project.new_request": {
        "subject": "Neuer Projektantrag: {{project_title}}",
        "body_text": "Hallo {{admin_name}},\nNeuer Antrag für {{project_title}}.",
        "available_variables": ["project_title", "admin_name"],
        "category": "project",
    }
}
