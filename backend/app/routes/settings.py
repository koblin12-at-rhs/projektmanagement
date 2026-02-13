import json

from flask import Blueprint, Response, jsonify, request
from flask_login import current_user

from app.middleware.permission_middleware import admin_required
from app.models.email_template import EmailTemplate
from app.models.i18n import TextTemplate
from app.models.settings import SystemSettings
from app.services.email_service import EmailTemplateService
from app.services.settings_service import SettingsService
from app.services.text_service import TextTemplateService

settings_bp = Blueprint("settings", __name__)


@settings_bp.get("/settings/public")
def get_public_settings():
    return jsonify(
        {
            "system_name": SettingsService.get_typed_value("general.system_name"),
            "projects_allowed": SettingsService.get_typed_value("projects.allow_new_requests"),
            "projects_disabled_message": SettingsService.get_typed_value("projects.request_disabled_message"),
            "footer_text": SettingsService.get_typed_value("general.footer_text"),
        }
    )


@settings_bp.get("/settings/project-status")
def project_status():
    allowed, message = SettingsService.can_create_project()
    return jsonify({"allowed": allowed, "reason": None if allowed else "disabled_by_admin", "message": message})


@settings_bp.get("/admin/settings")
@admin_required
def list_settings_admin():
    rows = SystemSettings.query.order_by(SystemSettings.category, SystemSettings.key).all()
    return jsonify([
        {
            "key": r.key,
            "value": r.value,
            "value_type": r.value_type,
            "category": r.category,
            "description": r.description,
        }
        for r in rows
    ])


@settings_bp.put("/admin/settings/<path:key>")
@admin_required
def update_setting(key: str):
    payload = request.get_json() or {}
    row = SettingsService.update_setting(key, payload.get("value"), current_user.id)
    if not row:
        return jsonify({"message": "Setting not found"}), 404
    return jsonify({"key": row.key, "value": row.value})


@settings_bp.post("/admin/settings/bulk")
@admin_required
def bulk_update_settings():
    payload = request.get_json() or {}
    updated = []
    for item in payload.get("settings", []):
        row = SettingsService.update_setting(item["key"], item["value"], current_user.id)
        if row:
            updated.append(row.key)
    return jsonify({"updated": updated})


@settings_bp.post("/admin/settings/export")
@admin_required
def export_settings():
    data = {row.key: row.value for row in SystemSettings.query.order_by(SystemSettings.key).all()}
    return Response(json.dumps(data, indent=2, ensure_ascii=False), mimetype="application/json")


@settings_bp.get("/admin/texts")
@admin_required
def list_texts():
    return jsonify([
        {
            "key": t.key,
            "language": t.language,
            "text_short": t.text_short,
            "text_long": t.text_long,
            "text_html": t.text_html,
            "category": t.category,
        }
        for t in TextTemplate.query.order_by(TextTemplate.key, TextTemplate.language).all()
    ])


@settings_bp.put("/admin/texts/<path:key>")
@admin_required
def update_text(key: str):
    payload = request.get_json() or {}
    row = TextTemplateService.update_text(key, payload.get("language", "de"), payload, current_user.id)
    if not row:
        return jsonify({"message": "Text not found"}), 404
    return jsonify({"key": row.key, "language": row.language})


@settings_bp.get("/admin/email-templates")
@admin_required
def list_email_templates():
    return jsonify([
        {
            "key": e.key,
            "subject": e.subject,
            "body_text": e.body_text,
            "body_html": e.body_html,
            "available_variables": e.available_variables,
            "category": e.category,
        }
        for e in EmailTemplate.query.order_by(EmailTemplate.key).all()
    ])


@settings_bp.put("/admin/email-templates/<path:key>")
@admin_required
def update_email_template(key: str):
    row = EmailTemplateService.update_template(key, request.get_json() or {}, current_user.id)
    if not row:
        return jsonify({"message": "Template not found"}), 404
    return jsonify({"key": row.key})


@settings_bp.post("/admin/email-templates/<path:key>/preview")
@admin_required
def preview_email_template(key: str):
    row = EmailTemplate.query.filter_by(key=key).first()
    if not row:
        return jsonify({"message": "Template not found"}), 404
    return jsonify(EmailTemplateService.render_preview(row, (request.get_json() or {}).get("variables", {})))
