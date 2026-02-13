from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from app.models.project import Project
from app.services.project_service import ProjectService

projects_bp = Blueprint("projects", __name__)


@projects_bp.post("")
@login_required
def create_project():
    payload = request.get_json() or {}
    project, message = ProjectService.create_project(current_user.id, payload)
    if not project:
        return jsonify({"message": message}), 403
    return jsonify({"id": project.id, "title": project.title}), 201


@projects_bp.get("")
@login_required
def list_projects():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return jsonify([
        {"id": p.id, "title": p.title, "status": p.status.value, "created_by_id": p.created_by_id}
        for p in projects
    ])
