param(
  [string]$FilePath = "$HOME\SENKRON_v4_1_5\state_senkron.json",
  [string]$HashFile = "$HOME\SENKRON_v4_1_5\state_hash.txt"
)
if (Test-Path $FilePath) {
    if (Test-Path $HashFile) {
      $old = Get-Content $HashFile -Raw
      $new = (Get-FileHash $FilePath -Algorithm SHA256).Hash
      if ($old -ne $new) {
        Write-Host "⚠️ State hash mismatch detected! Restoring last backup..." -ForegroundColor Yellow
        Copy-Item "$FilePath.bak" $FilePath -Force
      } else {
        Write-Host "✅ State integrity verified ($($new.Substring(0,12)))."
      }
    } else {
      (Get-FileHash $FilePath -Algorithm SHA256).Hash | Out-File $HashFile
      Write-Host "🔐 Initial hash stored."
    }
} else {
    Write-Host "⚠️ State file ($FilePath) not found. Skipping hash check." -ForegroundColor Yellow
}
