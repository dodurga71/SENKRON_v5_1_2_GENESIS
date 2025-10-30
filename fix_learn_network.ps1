# ==========================
# FIX_LEARN_NETWORK.PS1 — STABLE UTF8 SAFE
# ==========================

$learnFile = "$PSScriptRoot\learn.py"

if (-not (Test-Path $learnFile)) {
    Write-Host "learn.py bulunamadı." -ForegroundColor Red
    exit
}

# 1. Yeni kaynak URL
$newUrl = "https://raw.githubusercontent.com/huchenme/github-trending-api/master/sample/github_trending_python.json"

# 2. Eski adresi değiştir
$content = Get-Content $learnFile -Raw
if ($content -match "ghapi.huchen.dev") {
    $content = $content -replace "https://ghapi\.huchen\.dev/repositories\?language=python", $newUrl
    Write-Host "API adresi güncellendi -> github_trending_python.json" -ForegroundColor Yellow
}

# 3. Offline mod bloğu ekle
if ($content -notmatch "Offline mod aktif") {
    $offlineBlock = @"
import sys
args = sys.argv[1:]
if args and args[0] == "--offline":
    print("[OFFLINE] Offline mod aktif. Arxiv verisi kaynaktan cekilmeyecek.")
    exit()
"@
    $content = $offlineBlock + "`n" + $content
    Write-Host "Offline mod kontrolu eklendi." -ForegroundColor Cyan
}

# 4. Dosyayı kaydet
Set-Content -Path $learnFile -Value $content -Encoding UTF8
Write-Host "learn.py guncellendi." -ForegroundColor Green

# 5. Test calistir
Write-Host "LEARN modu yeniden baslatiliyor..." -ForegroundColor Cyan
& "$PSScriptRoot\.venv\Scripts\python.exe" "$learnFile"
