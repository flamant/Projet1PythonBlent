param(
    [string]$BaseUrl = "http://127.0.0.1:5000"
)

$ErrorActionPreference = "Stop"

function Write-Ok($message) {
    Write-Host "[OK] $message" -ForegroundColor Green
}

function Write-Info($message) {
    Write-Host "[INFO] $message" -ForegroundColor Cyan
}

function Write-Fail($message) {
    Write-Host "[FAIL] $message" -ForegroundColor Red
}

try {
    Write-Info "Test de l'endpoint racine"
    $root = Invoke-RestMethod -Uri "$BaseUrl/" -Method Get
    Write-Ok ("GET / -> " + ($root | ConvertTo-Json -Depth 4 -Compress))

    Write-Info "Test de l'endpoint health"
    $health = Invoke-RestMethod -Uri "$BaseUrl/health" -Method Get
    Write-Ok ("GET /health -> " + ($health | ConvertTo-Json -Depth 4 -Compress))

    $testEmail = "test_$([guid]::NewGuid().ToString('N').Substring(0,8))@mail.fr"
    $registerBody = @{
        id = $testEmail
        statut = "client"
        client = $true
        administrator = $false
    } | ConvertTo-Json

    Write-Info "Test de l'inscription utilisateur"
    $register = Invoke-RestMethod `
        -Uri "$BaseUrl/api/auth/register" `
        -Method Post `
        -Headers @{ password = "antoine" } `
        -ContentType "application/json" `
        -Body $registerBody
    Write-Ok ("POST /api/auth/register -> " + ($register | ConvertTo-Json -Depth 4 -Compress))

    $loginBody = @{
        id = "admin@login.fr"
        statut = "administrator"
    } | ConvertTo-Json

    Write-Info "Test de la connexion administrateur"
    $login = Invoke-RestMethod `
        -Uri "$BaseUrl/api/auth/login" `
        -Method Post `
        -Headers @{ password = "admin" } `
        -ContentType "application/json" `
        -Body $loginBody
    Write-Ok ("POST /api/auth/login -> " + ($login | ConvertTo-Json -Depth 4 -Compress))

    Write-Host ""
    Write-Ok "Tous les tests ont reussi."
}
catch {
    Write-Host ""
    Write-Fail "Un test a echoue."
    Write-Fail $_.Exception.Message
    exit 1
}
