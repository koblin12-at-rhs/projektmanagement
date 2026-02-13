from app import db
from app.models.audit import AuditLog
from app.models.i18n import TEXT_TEMPLATES_DEFAULTS, TextTemplate


class TextTemplateService:
    @staticmethod
    def seed_defaults() -> None:
        for key, langs in TEXT_TEMPLATES_DEFAULTS.items():
            for lang, data in langs.items():
                if not TextTemplate.query.filter_by(key=key, language=lang).first():
                    db.session.add(TextTemplate(key=key, language=lang, **data))
        db.session.commit()

    @staticmethod
    def update_text(key: str, language: str, payload: dict, actor_id: int | None = None):
        row = TextTemplate.query.filter_by(key=key, language=language).first()
        if not row:
            return None
        old_value = f"{row.text_short}|{row.text_long}|{row.text_html}"
        row.text_short = payload.get("text_short")
        row.text_long = payload.get("text_long")
        row.text_html = payload.get("text_html")
        db.session.add(AuditLog(actor_id=actor_id, entity_type="text_template", entity_key=f"{key}:{language}", old_value=old_value, new_value=f"{row.text_short}|{row.text_long}|{row.text_html}"))
        db.session.commit()
        return row
