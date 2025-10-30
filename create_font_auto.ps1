# =========================================
# 🧠 SENKRON Font Auto-Installer (DejaVuSans.ttf)
# Türkçe + Emoji uyumlu PDF fontu
# =========================================

$fontDir  = "$HOME\SENKRON_v4_1_5_CLEAN\fonts"
$fontFile = Join-Path $fontDir "DejaVuSans.ttf"
$backupFont = "C:\Windows\Fonts\arialuni.ttf"

$fontUrls = @(
    "https://github.com/dejavu-fonts/dejavu-fonts/raw/version_2_37/ttf/DejaVuSans.ttf",
    "https://downloads.sourceforge.net/project/dejavu/dejavu/2.37/dejavu-fonts-ttf-2.37.zip",
    "https://upload.wikimedia.org/wikipedia/commons/8/8b/DejaVuSans.ttf"
)

if (!(Test-Path $fontDir)) {
    New-Item -ItemType Directory -Path $fontDir -Force | Out-Null
}

Write-Host "🧩 Font klasörü: $fontDir" -ForegroundColor Cyan
Write-Host "⬇️ DejaVuSans.ttf indirme işlemi başlatılıyor..." -ForegroundColor Yellow

$downloaded = $false

foreach ($url in $fontUrls) {
    try {
        $outPath = Join-Path $fontDir "DejaVuSans_temp"
        Invoke-WebRequest -Uri $url -OutFile $outPath -UseBasicParsing -ErrorAction Stop
        $ext = [IO.Path]::GetExtension($url)

        if ($ext -eq ".zip") {
            Add-Type -AssemblyName System.IO.Compression.FileSystem
            $zip = [IO.Compression.ZipFile]::OpenRead($outPath)
            foreach ($entry in $zip.Entries) {
                if ($entry.FullName -like "*DejaVuSans.ttf") {
                    $entry.ExtractToFile($fontFile, $true)
                }
            }
            $zip.Dispose()
            Remove-Item $outPath -Force
        }
        else {
            Move-Item -Path $outPath -Destination $fontFile -Force
        }

        if (Test-Path $fontFile) {
            $sizeKB = [math]::Round((Get-Item $fontFile).Length / 1KB, 2)
            Write-Host "✅ Font indirildi ($sizeKB KB)" -ForegroundColor Green
            $downloaded = $true
            break
        }
    }
    catch {
        Write-Host "⚠️ Deneme başarısız ($url): $($_.Exception.Message)" -ForegroundColor DarkYellow
    }
}

if (-not $downloaded) {
    if (Test-Path $backupFont) {
        Copy-Item $backupFont -Destination $fontFile -Force
        Write-Host "💾 Yerel Arial Unicode MS fontu kullanıldı (yedek olarak)." -ForegroundColor Cyan
    } else {
        Write-Host "❌ Hiçbir kaynak erişilemedi, font oluşturulamadı." -ForegroundColor Red
    }
}

if (Test-Path $fontFile) {
    Write-Host "`n🎯 Font kurulumu tamamlandı → $fontFile" -ForegroundColor Green
    Write-Host "💡 Şimdi test et: python self_reflection_visualizer.py" -ForegroundColor Yellow
}


