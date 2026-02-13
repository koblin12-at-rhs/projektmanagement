from flask import Flask


def register_blueprints(app: Flask) -> None:
    from app.routes.auth import auth_bp
    from app.routes.projects import projects_bp
    from app.routes.settings import settings_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(projects_bp, url_prefix="/api/projects")
    app.register_blueprint(settings_bp, url_prefix="/api")
