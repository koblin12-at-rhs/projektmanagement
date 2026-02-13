from datetime import datetime

from app import db


class SystemSettings(db.Model):
    __tablename__ = "system_settings"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(255), unique=True, nullable=False, index=True)
    value = db.Column(db.Text, nullable=True)
    value_type = db.Column(db.Enum("STRING", "BOOLEAN", "INTEGER", "JSON", name="setting_type_enum"), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_user_editable = db.Column(db.Boolean, default=False)
    is_admin_only = db.Column(db.Boolean, default=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)


SYSTEM_SETTINGS_DEFAULTS = {
    "projects.allow_new_requests": {
        "value": "true",
        "value_type": "BOOLEAN",
        "category": "projects",
        "description": "Neue Projektanfragen zulassen (false = Sperre aktiv)",
    },
    "projects.request_disabled_message": {
        "value": "Derzeit können keine neuen Projekte beantragt werden. Bitte versuchen Sie es später erneut.",
        "value_type": "STRING",
        "category": "projects",
        "description": "Nachricht bei gesperrten Anfragen",
    },
    "general.system_name": {
        "value": "MakerSpace Projektmanagement",
        "value_type": "STRING",
        "category": "general",
        "description": "Name des Systems",
    },
    "general.footer_text": {
        "value": "© 2026 Ihre Schule - MakerSpace",
        "value_type": "STRING",
        "category": "general",
        "description": "Footer-Text",
    },
}
