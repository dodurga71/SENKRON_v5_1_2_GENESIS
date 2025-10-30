$yamlPath = "$HOME\SENKRON_v4_1_5_CLEAN\docs\science_registry.yaml"
if (!(Test-Path $yamlPath)) {
    Write-Host "science_registry.yaml bulunamadı." -ForegroundColor Red
    exit
}

$content = Get-Content $yamlPath -Raw
if ($content -notmatch "accuracy_score") {
    Write-Host "🧠 science_registry.yaml formatı güncelleniyor..." -ForegroundColor Yellow
    $updated = @"
records:
  - title: "Nazal metformin-kurkumin taşıma çalışması"
    timestamp: "$(Get-Date -Format o)"
    accuracy_score: 88
    novelty_score: 76
    summary: "Farmasötik taşıma ve kombinasyon sinerjisi açısından güçlü potansiyel."
"@
    Set-Content -Path $yamlPath -Value $updated -Encoding UTF8
    Write-Host "✅ science_registry.yaml örnek veriyle güncellendi." -ForegroundColor Green
} else {
    Write-Host "✅ Zaten güncel formatta." -ForegroundColor Green
}
