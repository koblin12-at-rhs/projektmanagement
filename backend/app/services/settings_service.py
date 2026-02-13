import json
from collections import defaultdict

from app import db
from app.models.audit import AuditLog
from app.models.settings import SYSTEM_SETTINGS_DEFAULTS, SystemSettings


class SettingsService:
    _cache: dict[str, str] = {}

    @classmethod
    def seed_defaults(cls) -> None:
        for key, data in SYSTEM_SETTINGS_DEFAULTS.items():
            if not SystemSettings.query.filter_by(key=key).first():
                db.session.add(SystemSettings(key=key, **data))
        db.session.commit()
        cls.refresh_cache()

    @classmethod
    def refresh_cache(cls) -> None:
        cls._cache = {row.key: row.value for row in SystemSettings.query.all()}

    @classmethod
    def get_typed_value(cls, key: str):
        row = SystemSettings.query.filter_by(key=key).first()
        if not row:
            return None
        if row.value_type == "BOOLEAN":
            return (row.value or "").lower() == "true"
        if row.value_type == "INTEGER":
            return int(row.value or 0)
        if row.value_type == "JSON":
            return json.loads(row.value or "{}")
        return row.value

    @classmethod
    def can_create_project(cls) -> tuple[bool, str | None]:
        allowed = cls.get_typed_value("projects.allow_new_requests")
        if not allowed:
            return False, cls.get_typed_value("projects.request_disabled_message") or "Neue Projektanfragen sind derzeit nicht möglich."
        return True, None

    @classmethod
    def get_grouped_settings(cls):
        grouped = defaultdict(list)
        for row in SystemSettings.query.order_by(SystemSettings.category, SystemSettings.key).all():
            grouped[row.category].append(row)
        return grouped

    @classmethod
    def update_setting(cls, key: str, value: str, actor_id: int | None = None) -> SystemSettings | None:
        row = SystemSettings.query.filter_by(key=key).first()
        if not row:
            return None
        old_value = row.value
        row.value = str(value)
        row.updated_by_id = actor_id
        db.session.add(AuditLog(actor_id=actor_id, entity_type="system_setting", entity_key=key, old_value=old_value, new_value=row.value))
        db.session.commit()
        cls.refresh_cache()
        return row
