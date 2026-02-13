import pytest

from app import create_app, db
from app.models.user import User
from app.services.email_service import EmailTemplateService
from app.services.settings_service import SettingsService
from app.services.text_service import TextTemplateService


@pytest.fixture()
def app():
    app = create_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite://",
        SECRET_KEY="test",
        WTF_CSRF_ENABLED=False,
    )
    with app.app_context():
        db.drop_all()
        db.create_all()
        admin = User(username="admin", email="admin@example.com", role="admin")
        admin.set_password("secret")
        user = User(username="user", email="user@example.com", role="student")
        user.set_password("secret")
        db.session.add_all([admin, user])
        db.session.commit()
        SettingsService.seed_defaults()
        TextTemplateService.seed_defaults()
        EmailTemplateService.seed_defaults()
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()
