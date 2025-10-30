Write-Host "🔧 SENKRON PDF Unicode düzeltmesi başlatılıyor..." -ForegroundColor Cyan

# 1️⃣ Font yolu
$fontDir = "$PWD\fonts"
$fontPath = "$fontDir\DejaVuSans.ttf"

# 2️⃣ Font dizini oluştur
if (-not (Test-Path $fontDir)) {
    New-Item -ItemType Directory -Path $fontDir | Out-Null
}

# 3️⃣ Font indir (varsa geç)
if (-not (Test-Path $fontPath)) {
    Write-Host "⬇️ DejaVuSans.ttf indiriliyor..." -ForegroundColor Yellow
    $url = "https://github.com/dejavu-fonts/dejavu-fonts/raw/version_2_37/ttf/DejaVuSans.ttf"
    try {
        Invoke-WebRequest -Uri $url -OutFile $fontPath -ErrorAction Stop
        Write-Host "✅ Font indirildi: $fontPath" -ForegroundColor Green
    } catch {
        Write-Host "⚠️ Font indirilemedi, sistem Arial Unicode MS kullanılacak." -ForegroundColor Red
    }
}

# 4️⃣ Hedef dosya
$target = "$PWD\self_reflection_visualizer.py"
if (-not (Test-Path $target)) {
    Write-Host "❌ Hedef dosya bulunamadı!" -ForegroundColor Red
    exit
}

# 5️⃣ Dosya içeriğini oku
$content = Get-Content $target -Raw -Encoding UTF8

# 6️⃣ Font ekleme bloğu
if ($content -notmatch "add_font") {
    Write-Host "🧩 Unicode font ekleniyor..." -ForegroundColor Yellow
    $insertBlock = @'
try:
    pdf.add_font("DejaVu", "", "fonts/DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", size=12)
except Exception as e:
    print("⚠️ Unicode font yüklenemedi:", e)
    pdf.set_font("Arial", size=12)
'@
    $content = $content -replace 'pdf\.set_font\("Arial".*?\)', $insertBlock
}

# 7️⃣ Dosyayı kaydet
Set-Content -Path $target -Value $content -Encoding UTF8
Write-Host "✅ self_reflection_visualizer.py başarıyla güncellendi." -ForegroundColor Green

# 8️⃣ Test önerisi
Write-Host ""
Write-Host "Şimdi test et:" -ForegroundColor Cyan
Write-Host "python self_reflection_visualizer.py" -ForegroundColor Green
