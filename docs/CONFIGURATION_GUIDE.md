# Konfigurationshandbuch

## Übersicht der konfigurierbaren Settings
- `projects.allow_new_requests`: globale Sperre für neue Projektanträge.
- `projects.request_disabled_message`: Hinweistext bei gesperrten Anträgen.
- `general.system_name`: Name im Kopfbereich.
- `general.footer_text`: Footer-Text.

## Textbausteine-Verwaltung
Textbausteine werden über `TextTemplate` verwaltet (`/api/admin/texts`).

### Best Practices
- Keine HTML-Tags in Kurztexten (`text_short`).
- `text_html` nur für Hilfeblöcke nutzen.
- Pro Sprache getrennte Einträge pflegen.

## E-Mail-Templates
- Verwaltung über `/api/admin/email-templates`.
- Vorschau über `/api/admin/email-templates/:key/preview`.
- Platzhalterformat: `{{variable}}`.

## Projektanfragen sperren
1. `projects.allow_new_requests` auf `false` setzen.
2. Nachricht in `projects.request_disabled_message` definieren.
3. Frontend zeigt Banner und deaktiviert Button.

## Import/Export
- JSON-Export: `POST /api/admin/settings/export`.
- YAML-Import: vorgesehen über `POST /api/admin/settings/import-yaml`.

## Backup-Strategie
- Datenbank-Backup via `pg_dump` (Cron).
- Settings/Text-Export regelmäßig versionieren.
