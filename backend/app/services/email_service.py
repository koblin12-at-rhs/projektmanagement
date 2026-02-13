import re

from app import db
from app.models.audit import AuditLog
from app.models.email_template import EMAIL_TEMPLATES_DEFAULTS, EmailTemplate


class EmailTemplateService:
    @staticmethod
    def seed_defaults() -> None:
        for key, data in EMAIL_TEMPLATES_DEFAULTS.items():
            if not EmailTemplate.query.filter_by(key=key).first():
                db.session.add(EmailTemplate(key=key, **data))
        db.session.commit()

    @staticmethod
    def render_preview(template: EmailTemplate, values: dict[str, str]) -> dict[str, str]:
        def repl(text: str) -> str:
            rendered = text
            for k, v in values.items():
                rendered = rendered.replace("{{" + k + "}}", str(v))
            return re.sub(r"{{\s*\w+\s*}}", "", rendered)

        return {"subject": repl(template.subject), "body_text": repl(template.body_text), "body_html": repl(template.body_html or "")}

    @staticmethod
    def update_template(key: str, payload: dict, actor_id: int | None = None):
        row = EmailTemplate.query.filter_by(key=key).first()
        if not row:
            return None
        old_value = row.body_text
        row.subject = payload.get("subject", row.subject)
        row.body_text = payload.get("body_text", row.body_text)
        row.body_html = payload.get("body_html", row.body_html)
        row.available_variables = payload.get("available_variables", row.available_variables)
        db.session.add(AuditLog(actor_id=actor_id, entity_type="email_template", entity_key=key, old_value=old_value, new_value=row.body_text))
        db.session.commit()
        return row
