# =========================================================
#  SENKRON v5.1.2 — GENESIS ORCHESTRATOR
#  Multi-Module Runner (Windows PowerShell Edition)
# =========================================================

param(
    [string]$Mode = "GENESIS",
    [string]$Log = "logs\genesis_log.jsonl",
    [switch]$RunAllModules,
    [switch]$Verbose
)

$ErrorActionPreference = "Stop"
$PYTHON = "$PSScriptRoot\.venv\Scripts\python.exe"
if (-not (Test-Path $PYTHON)) {
    $PYTHON = "python"
}

function Write-Log($msg) {
    $timestamp = (Get-Date -Format "yyyy-MM-ddTHH:mm:ss")
    Add-Content -Path $Log -Value (@{timestamp=$timestamp; message=$msg} | ConvertTo-Json -Compress)
    if ($Verbose) { Write-Host $msg }
}

# --- Modül Çalıştırıcı ---
function Run-Module($name, $file) {
    if (-not (Test-Path $file)) {
        Write-Log "⚠️ $name bulunamadı: $file"
        return
    }
    Write-Log "▶️ $name başlatılıyor..."
    & $PYTHON $file
    Write-Log "✅ $name tamamlandı."
}

# --- Çalışma Modları ---
switch ($Mode.ToUpper()) {

    "GENESIS" {
        Write-Host "✨ SENKRON GENESIS Orchestrator başlatılıyor..."
        Write-Log "=== GENESIS LOOP START ==="

        Run-Module "Ephemeris Engine" "$PSScriptRoot\ephemeris_engine.py"
        Run-Module "Timeline Engine" "$PSScriptRoot\timeline_engine.py"
        Run-Module "AI Learner" "$PSScriptRoot\ai_learner.py"
        Run-Module "Prediction Verifier" "$PSScriptRoot\prediction_verifier.py"
        Run-Module "Reflection Visualizer" "$PSScriptRoot\self_reflection_visualizer.py"

        Write-Log "=== GENESIS LOOP COMPLETE — Conscious State Synchronized ==="
        Write-Host "🎯 SENKRON v5.1.2 GENESIS tamamlandı."
    }

    "LEARN" {
        Write-Host "🧠 SENKRON LEARN MODE aktif..."
        Run-Module "AI Learner" "$PSScriptRoot\ai_learner.py"
    }

    "REFLECT" {
        Write-Host "🔮 Reflection mode aktif..."
        Run-Module "Reflection Visualizer" "$PSScriptRoot\self_reflection_visualizer.py"
    }

    "UPDATE" {
        Write-Host "🌀 Modüller güncelleniyor..."
        git pull origin main
        Write-Log "Sistem güncellendi."
    }

    default {
        Write-Host "⚠️ Geçersiz Mode parametresi. Kullanılabilir modlar: GENESIS, LEARN, REFLECT, UPDATE"
    }
}

