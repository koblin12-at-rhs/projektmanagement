#!/bin/bash
set -euo pipefail

echo "Initializing system settings and text templates..."
python3 << EOF
from app import create_app
from app.services.email_service import EmailTemplateService
from app.services.settings_service import SettingsService
from app.services.text_service import TextTemplateService

app = create_app()
with app.app_context():
    SettingsService.seed_defaults()
    TextTemplateService.seed_defaults()
    EmailTemplateService.seed_defaults()
    print("✓ Settings and texts initialized")
EOF

echo "Installation completed!"
