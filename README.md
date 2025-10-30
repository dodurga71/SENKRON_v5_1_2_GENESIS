<p align="center">
  <img src="./logo.jpg" width="260" alt="SENKRON Logo">
</p>

<h1 align="center">?? SENKRON v5.1.2-GENESIS</h1>
<h3 align="center">Conscious Predictive Intelligence Framework</h3>
<p align="center"><b>Stable GENESIS Snapshot – 2025-10-30</b></p>

---

## ?? Genel Tanim
**SENKRON**, bilincin zamanla senkronizasyonunu modelleyen, astrolojik, finansal ve bilissel verileri birlestiren çok katmanli bir **yapay zekâ tahmin sistemi**dir.
Bu sürüm, sistemin ilk **kararli ve bütünlesik “Genesis” çekirdek yapisi**dir.

---

## ?? Sistem Gereksinimleri
| Bilesen | Önerilen Sürüm | Açiklama |
|---|---|---|
| **Python** | 3.11.x | Swiss Ephemeris uyumlulugu için 3.11 önerilir |
| **pip** | = 25.0 | Güncel olmali |
| **Git** | = 2.44 | Versiyon kontrol |
| **Windows 10/11 (64-bit)** |  | Test edilen ortam |

---

## ?? Gerekli Kütüphaneler
\\\ash
py -3.11 -m pip install -r requirements.txt
\\\
Temel: 
umpy, pandas, matplotlib, plotly[kaleido], 
eportlab, schedule, skyfield, pyswisseph, pyyaml, openpyxl, 
equests

---

## ?? Çekirdek Modüller
| Modül | Görev | Durum |
|---|---|---|
| ephemeris_engine.py | Skyfield + SwissEphem efemeris üretimi | ? |
| ai_learner.py | Bilinçsel ögrenme & örüntü normalizasyonu | ? |
| timeline_engine_predictive.py | Zaman çizelgesi tahmini | ? |
| chronomatrix_visualizer_safe.py | Görsellestirme (HTML+PNG) | ? |
| chronomatrix_reporter.py | Haftalik PDF rapor | ? |
| auto_scheduler.py | Planlanmis görevler | ?? (server’da) |
| ai_self_reviewer.py | Ögrenme döngüsü degerlendirme | ? |

---

## ?? Dizin Yapisi
\\\
SENKRON_v4_1_5_CLEAN/
+-- ephemeris/      # DE421
+-- fonts/          # DejaVu TTF
+-- logs/           # .jsonl / .txt
+-- reports/        # PDF raporlar
+-- docs/           # science_registry.yaml
+-- *.py
+-- requirements.txt
+-- senkron.ps1
\\\

---

## ?? Çalistirma Örnekleri
\\\ash
py -3.11 ephemeris_engine.py
py -3.11 ai_learner.py
py -3.11 timeline_engine_predictive.py
py -3.11 chronomatrix_visualizer_safe.py
py -3.11 chronomatrix_reporter.py
\\\

---

## ?? Log & Çiktilar
| Dosya | Açiklama |
|---|---|
| logs/genesis_log.jsonl | Zaman damgali loglar |
| reflection_trend.json | Bilinçsel moment |
| timeline_records.json | Tahmin kayitlari |
| chronomatrix_weekly_report.pdf | Haftalik rapor |
| metrics_summary.json | Metrik özeti |

---

## ?? Stabilite
| Bilesen | Durum |
|---|---|
| Skyfield / Swiss Ephemeris | ? Stabil |
| ReportLab Unicode | ? Türkçe uyumlu |
| Timeline Engine | ? |
| Scheduler | ?? Server kurulumu |

---

## ?? Yazar ve Telif
**Selçuk Onur Özyilmaz**  
© 2025 — SENKRON Project (All Rights Reserved)  
GitHub: [dodurga71/SENKRON_v4_1_5](https://github.com/dodurga71/SENKRON_v4_1_5)
