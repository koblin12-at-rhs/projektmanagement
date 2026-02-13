from app import db
from app.models.project import Project
from app.services.settings_service import SettingsService


class ProjectService:
    @staticmethod
    def create_project(user_id: int, payload: dict):
        allowed, message = SettingsService.can_create_project()
        if not allowed:
            return None, message
        project = Project(
            title=payload["title"],
            description=payload.get("description"),
            custom_fields=payload.get("custom_fields"),
            created_by_id=user_id,
        )
        db.session.add(project)
        db.session.commit()
        return project, None
