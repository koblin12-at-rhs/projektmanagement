# MakerSpace Projektmanagementsystem

On-premise Projektmanagementplattform für schulische MakerSpaces.

## Quickstart
1. Backend installieren:
   - `python -m venv .venv && source .venv/bin/activate`
   - `pip install -r backend/requirements.txt`
2. Server starten:
   - `cd backend && python run.py`
3. Frontend:
   - `cd frontend && npm install && npm run dev`

## Highlights
- Lokaler + SAML-Stub Login
- Projektanträge mit globaler Sperre
- Konfigurierbare Systemsettings
- Dynamische Textbausteine (i18n)
- E-Mail-Template-Verwaltung inkl. Vorschau
- Audit-Logging für Konfigurationsänderungen

## Konfiguration
Siehe `docs/CONFIGURATION_GUIDE.md` und `config/system_defaults.yaml`.


## Windows-Installation
PowerShell-Installer: `deployment/install-windows.ps1` (Details in `docs/INSTALLATION_WINDOWS.md`).
