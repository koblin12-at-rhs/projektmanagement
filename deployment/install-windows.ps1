Param(
    [switch]$SkipWinget,
    [switch]$SkipPostgres,
    [string]$PostgresPassword = "makerspace",
    [string]$ProjectRoot = "$PSScriptRoot\.."
)

$ErrorActionPreference = "Stop"

function Write-Step {
    param([string]$Message)
    Write-Host "`n==> $Message" -ForegroundColor Cyan
}

function Ensure-Command {
    param(
        [string]$Command,
        [string]$WingetId,
        [switch]$SkipInstall
    )

    if (Get-Command $Command -ErrorAction SilentlyContinue) {
        Write-Host "[OK] $Command gefunden." -ForegroundColor Green
        return
    }

    if ($SkipInstall) {
        throw "Benötigter Befehl '$Command' fehlt und Installation wurde übersprungen."
    }

    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
        throw "winget ist nicht verfügbar. Bitte '$Command' manuell installieren."
    }

    Write-Host "Installiere $Command über winget ($WingetId)..." -ForegroundColor Yellow
    winget install --id $WingetId --accept-package-agreements --accept-source-agreements --silent

    if (-not (Get-Command $Command -ErrorAction SilentlyContinue)) {
        $env:PATH = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
    }

    if (-not (Get-Command $Command -ErrorAction SilentlyContinue)) {
        throw "Installation von '$Command' fehlgeschlagen oder PATH wurde noch nicht aktualisiert."
    }

    Write-Host "[OK] $Command installiert." -ForegroundColor Green
}

Write-Step "Prüfe Voraussetzungen"
Ensure-Command -Command "python" -WingetId "Python.Python.3.11" -SkipInstall:$SkipWinget
Ensure-Command -Command "node" -WingetId "OpenJS.NodeJS.LTS" -SkipInstall:$SkipWinget
Ensure-Command -Command "npm" -WingetId "OpenJS.NodeJS.LTS" -SkipInstall:$SkipWinget

if (-not $SkipPostgres) {
    Ensure-Command -Command "psql" -WingetId "PostgreSQL.PostgreSQL.15" -SkipInstall:$SkipWinget
}

Write-Step "Wechsle ins Projektverzeichnis"
$ResolvedRoot = (Resolve-Path $ProjectRoot).Path
Set-Location $ResolvedRoot
Write-Host "Arbeitsverzeichnis: $ResolvedRoot"

Write-Step "Backend einrichten (virtuelle Umgebung + Dependencies)"
python -m venv .venv
$venvPython = Join-Path $ResolvedRoot ".venv\Scripts\python.exe"
& $venvPython -m pip install --upgrade pip
& $venvPython -m pip install -r backend\requirements.txt

Write-Step "Frontend einrichten"
Push-Location frontend
npm install
Pop-Location

if (-not $SkipPostgres) {
    Write-Step "PostgreSQL-Datenbank vorbereiten"
    $createSql = @"
DO
$$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'makerspace') THEN
      CREATE ROLE makerspace WITH LOGIN PASSWORD '$PostgresPassword';
   END IF;
END
$$;

SELECT 'CREATE DATABASE makerspace_pms OWNER makerspace'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'makerspace_pms')\gexec
"@

    $tempSql = Join-Path $env:TEMP "makerspace_init.sql"
    Set-Content -Path $tempSql -Value $createSql -Encoding UTF8

    Write-Host "Bitte ggf. das Passwort des PostgreSQL-Superusers eingeben." -ForegroundColor Yellow
    psql -U postgres -f $tempSql
    Remove-Item $tempSql -ErrorAction SilentlyContinue
}

Write-Step "Backend Seed ausführen"
$seedScript = @"
from app import create_app
from app.services.settings_service import SettingsService
from app.services.text_service import TextTemplateService
from app.services.email_service import EmailTemplateService

app = create_app()
with app.app_context():
    SettingsService.seed_defaults()
    TextTemplateService.seed_defaults()
    EmailTemplateService.seed_defaults()

print("Seed abgeschlossen")
"@
$seedFile = Join-Path $env:TEMP "makerspace_seed.py"
Set-Content -Path $seedFile -Value $seedScript -Encoding UTF8
Push-Location backend
& $venvPython $seedFile
Pop-Location
Remove-Item $seedFile -ErrorAction SilentlyContinue

Write-Step "Beispiel-Startkommandos"
Write-Host "Backend starten: .venv\Scripts\python.exe backend\run.py"
Write-Host "Frontend starten: cd frontend; npm run dev"

Write-Host "`nInstallation abgeschlossen." -ForegroundColor Green
