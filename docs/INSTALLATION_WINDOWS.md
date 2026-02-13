# Installation unter Windows (PowerShell)

## Voraussetzungen
- Windows 10/11
- PowerShell 5.1+ oder PowerShell 7+
- Administratorrechte (für Paketinstallation mit winget)

## Schnellstart
Im Projektverzeichnis:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\deployment\install-windows.ps1
```

## Optionen
- `-SkipWinget`: Keine automatische Installation fehlender Tools.
- `-SkipPostgres`: Überspringt PostgreSQL-Installation und DB-Erstellung.
- `-PostgresPassword "<passwort>"`: Passwort für DB-User `makerspace`.
- `-ProjectRoot "C:\Pfad\zum\Repo"`: Alternativer Projektpfad.

Beispiel:

```powershell
.\deployment\install-windows.ps1 -SkipPostgres -SkipWinget
```

## Was das Skript erledigt
1. Prüft/ installiert Python 3.11, Node.js (LTS), npm und optional PostgreSQL 15.
2. Erstellt `.venv` und installiert `backend/requirements.txt`.
3. Führt `npm install` im Frontend aus.
4. Legt optional DB und Rolle `makerspace` an.
5. Seedet Standard-Settings, Text-Templates und E-Mail-Templates.

## Start nach Installation
- Backend:
  ```powershell
  .\.venv\Scripts\python.exe backend\run.py
  ```
- Frontend:
  ```powershell
  cd frontend
  npm run dev
  ```
