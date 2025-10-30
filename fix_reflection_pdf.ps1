Write-Host "SENKRON self_reflection_visualizer düzeltici başlatılıyor..." -ForegroundColor Cyan

# 1️⃣ Ortam kontrolü
if (-not (Test-Path ".venv")) {
    Write-Host "Uyarı: .venv bulunamadı, işlem devam ediyor." -ForegroundColor Yellow
}

# 2️⃣ FPDF temizleme ve yeniden kurulum
Write-Host "FPDF temizleme ve yeniden kurulum..." -ForegroundColor Yellow
& .\.venv\Scripts\pip.exe uninstall -y fpdf PyFPDF 2>$null
& .\.venv\Scripts\pip.exe install -U fpdf2==2.7.9 2>$null

# 3️⃣ Hedef dosya
$target = "$PWD\self_reflection_visualizer.py"
if (-not (Test-Path $target)) {
    Write-Host "self_reflection_visualizer.py bulunamadı!" -ForegroundColor Red
    exit
}

# 4️⃣ Font URL düzeltmesi ve emoji fallback ekleme
$content = Get-Content $target -Raw -Encoding UTF8

# Font URL güncelle
$content = $content -replace "raw\.githubusercontent\.com/dejavu-fonts/dejavu-fonts/version_2_37/ttf/DejaVuSans\.ttf",
                             "github.com/dejavu-fonts/dejavu-fonts/releases/download/version_2_37/DejaVuSans.ttf"

# Fallback kod bloğu ekle
if ($content -match "SENKRON Bilinç Raporu") {
    Write-Host "Emoji fallback düzeltmesi uygulanıyor..." -ForegroundColor Yellow
    $fallbackBlock = 'title_text = "SENKRON Bilinç Raporu"
try:
    pdf.cell(200, 10, text=title_text, new_x="LMARGIN", new_y="NEXT", align="C")
except Exception:
    pdf.cell(200, 10, text="SENKRON Bilinç Raporu", new_x="LMARGIN", new_y="NEXT", align="C")'
    $content = $content -replace 'pdf\.cell\(.*SENKRON Bilinç Raporu.*?\)', $fallbackBlock
}

# 5️⃣ Dosyayı kaydet
Set-Content -Path $target -Value $content -Encoding UTF8
Write-Host "self_reflection_visualizer.py başarıyla güncellendi." -ForegroundColor Green

# 6️⃣ Test komutu
Write-Host ""
Write-Host "Şimdi test etmek için çalıştır:" -ForegroundColor Cyan
Write-Host "python self_reflection_visualizer.py" -ForegroundColor Green
