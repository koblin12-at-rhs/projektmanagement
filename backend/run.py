from app import create_app, socketio
from app.services.email_service import EmailTemplateService
from app.services.settings_service import SettingsService
from app.services.text_service import TextTemplateService

app = create_app()

with app.app_context():
    SettingsService.seed_defaults()
    TextTemplateService.seed_defaults()
    EmailTemplateService.seed_defaults()

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
