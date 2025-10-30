# ==========================================
# 🧠 SENKRON Local Font Extractor (universal)
# DejaVuSans.ttf yerel ZIP’ten çıkarılır
# ==========================================

Add-Type -AssemblyName System.IO.Compression.FileSystem

$zipPath  = "$HOME\SENKRON_v4_1_5_CLEAN\dejavu-sans.zip"
$fontDir  = "$HOME\SENKRON_v4_1_5_CLEAN\fonts"
$fontFile = Join-Path $fontDir "DejaVuSans.ttf"

if (!(Test-Path $fontDir)) {
    New-Item -ItemType Directory -Path $fontDir -Force | Out-Null
}

Write-Host "🧩 ZIP dosyası: $zipPath" -ForegroundColor Cyan

if (!(Test-Path $zipPath)) {
    Write-Host "❌ ZIP dosyası bulunamadı!" -ForegroundColor Red
    exit
}

try {
    $zip = [IO.Compression.ZipFile]::OpenRead($zipPath)
    $found = $false

    foreach ($entry in $zip.Entries) {
        if ($entry.FullName -like "*DejaVuSans.ttf") {
            Write-Host "📦 $($entry.FullName) bulunuyor, çıkarılıyor..." -ForegroundColor Yellow
            $stream = $entry.Open()
            $target = [System.IO.File]::Create($fontFile)
            $stream.CopyTo($target)
            $stream.Close()
            $target.Close()
            $found = $true
        }
    }

    $zip.Dispose()

    if ($found -and (Test-Path $fontFile)) {
        $size = [math]::Round((Get-Item $fontFile).Length / 1KB, 2)
        Write-Host "✅ DejaVuSans.ttf başarıyla çıkarıldı ($size KB)" -ForegroundColor Green
        Write-Host "📂 Konum: $fontFile"
        Write-Host "`n💡 Şimdi test et: python self_reflection_visualizer.py" -ForegroundColor Cyan
    } else {
        Write-Host "⚠️ ZIP içinde DejaVuSans.ttf bulunamadı." -ForegroundColor DarkYellow
    }
}
catch {
    Write-Host "❌ Hata oluştu: $($_.Exception.Message)" -ForegroundColor Red
}
