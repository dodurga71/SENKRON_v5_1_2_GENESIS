# -*- coding: utf-8 -*-
<#
SENKRON AUTO REPORT SCHEDULER
-------------------------------------------------
• Her gün sabah 09:00’da evolution_visualizer.py çalıştırılır.
• Üretilen raporlar /reports klasörüne tarihli olarak kaydedilir.
• Hatalar error.log içine yazılır.
• Rapor başarıyla üretilirse sistem log güncellenir.
#>

$base = "$HOME\SENKRON_v4_1_5_CLEAN"
$venvPython = Join-Path $base ".venv\Scripts\python.exe"
$reportScript = Join-Path $base "evolution_visualizer.py"
$reportDir = Join-Path $base "reports"
$logFile = Join-Path $base "scheduler.log"
$errorFile = Join-Path $base "error.log"

# Klasör oluştur
if (-not (Test-Path $reportDir)) { New-Item -Path $reportDir -ItemType Directory | Out-Null }

# Rapor oluşturma işlemi
function Generate-Report {
    try {
        $timestamp = (Get-Date -Format "yyyy-MM-dd_HH-mm-ss")
        Write-Host "🕒 [$timestamp] Rapor oluşturuluyor..." -ForegroundColor Cyan
        & $venvPython $reportScript 2>> $errorFile
        if ($LASTEXITCODE -eq 0) {
            $srcPdf = Join-Path $base "evolution_report.pdf"
            $destPdf = Join-Path $reportDir "evolution_report_$timestamp.pdf"
            if (Test-Path $srcPdf) {
                Copy-Item $srcPdf $destPdf -Force
                Add-Content -Path $logFile -Value "[$timestamp] ✅ Rapor başarıyla üretildi: $destPdf"
                Write-Host "✅ Günlük rapor başarıyla kaydedildi → $destPdf" -ForegroundColor Green
            }
        } else {
            Add-Content -Path $logFile -Value "[$timestamp] ❌ Hata kodu: $LASTEXITCODE"
        }
    } catch {
        $errMsg = $_.Exception.Message
        Add-Content -Path $errorFile -Value "[$(Get-Date -Format 'u')] $errMsg"
        Write-Host "⚠️ Hata oluştu: $errMsg" -ForegroundColor Yellow
    }
}

# Görev zamanlayıcı kurulumu
$taskName = "SENKRON_DAILY_REPORT"
$action = New-ScheduledTaskAction -Execute "pwsh.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$base\auto_report_scheduler.ps1`""
$trigger = New-ScheduledTaskTrigger -Daily -At 9:00AM
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

if (-not (Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue)) {
    Register-ScheduledTask -Action $action -Trigger $trigger -Settings $settings -TaskName $taskName -Description "SENKRON günlük PDF rapor üretimi" | Out-Null
    Write-Host "🧭 Günlük zamanlayıcı başarıyla oluşturuldu (her gün 09:00)" -ForegroundColor Green
} else {
    Write-Host "ℹ️ Zamanlayıcı zaten mevcut, yalnızca rapor çalıştırılıyor..." -ForegroundColor Cyan
    Generate-Report
}
