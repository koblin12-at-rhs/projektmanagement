from datetime import datetime

from app import db


class TextTemplate(db.Model):
    __tablename__ = "text_templates"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(255), unique=False, nullable=False, index=True)
    language = db.Column(db.String(5), default="de", nullable=False)
    text_short = db.Column(db.String(255), nullable=True)
    text_long = db.Column(db.Text, nullable=True)
    text_html = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(100), nullable=False)
    context = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint("key", "language", name="uq_text_key_language"),)


TEXT_TEMPLATES_DEFAULTS = {
    "button.new_project": {
        "de": {"text_short": "Neues Projekt", "category": "buttons"},
        "en": {"text_short": "New Project", "category": "buttons"},
    },
    "message.project_created": {
        "de": {"text_long": "Ihr Projektantrag wurde erfolgreich eingereicht.", "category": "messages"},
        "en": {"text_long": "Your project request has been submitted successfully.", "category": "messages"},
    },
}
