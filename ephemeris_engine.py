# =========================================================
#  SENKRON v5.2.2 — ephemeris_engine.py
#  Dual-Core Ephemeris Engine (Skyfield + SwissEphem + Failsafe)
#  Stable Industrial Release — JSON-safe, bool-fixed
# =========================================================

from __future__ import annotations
import os, json, math
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ---------------------------------------------
#  PATHS
# ---------------------------------------------
ROOT = Path(__file__).resolve().parent
LOGS = ROOT / "logs"; LOGS.mkdir(exist_ok=True)
EPH  = ROOT / "ephemeris"; EPH.mkdir(exist_ok=True)
SNAPSHOT_JSON = ROOT / "ephemeris_snapshot.json"
SUMMARY_TXT   = ROOT / "ephemeris_summary.txt"
GENESIS_LOG   = LOGS / "genesis_log.jsonl"

# ---------------------------------------------
#  LIBRARY CHECKS
# ---------------------------------------------
_HAVE_SKYFIELD = False
_HAVE_SWISS = False

try:
    from skyfield.api import load as sf_load
    from skyfield.framelib import ecliptic_frame
    _HAVE_SKYFIELD = True
except Exception:
    _HAVE_SKYFIELD = False

try:
    import swisseph as swe
    _HAVE_SWISS = True
except Exception:
    _HAVE_SWISS = False

# ---------------------------------------------
#  HELPERS
# ---------------------------------------------
def log(msg: str):
    """Hem konsola hem JSONL log dosyasına yazar."""
    ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    with open(GENESIS_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps({"timestamp": ts, "module": "ephemeris_engine", "message": msg}, ensure_ascii=False) + "\n")
    print(msg, flush=True)

def deg_norm(x: float) -> float:
    v = x % 360.0
    return v if v >= 0 else v + 360.0

def delta_lon(a: float, b: float) -> float:
    """İki boylam arasındaki en küçük fark (−180..180)."""
    d = (b - a) % 360.0
    return d - 360.0 if d > 180.0 else d

# ---------------------------------------------
#  FAILSAFE ENGINE
# ---------------------------------------------
def failsafe_compute(now: datetime):
    """Skyfield/Swiss yoksa deterministik yedek hesaplama yapar."""
    avg = {"Sun":0.9856,"Moon":13.1764,"Mercury":4.0923,"Venus":1.6021,"Mars":0.5240,"Jupiter":0.0831,"Saturn":0.0335}
    epoch = datetime(2025,1,1,tzinfo=timezone.utc)
    days = (now - epoch).total_seconds()/86400
    planets = {}
    for n,r in avg.items():
        base = (hash(n) % 3600) / 10
        lon  = deg_norm(base + r * days)
        lon_y = deg_norm(base + r * (days - 1))
        retro = bool(delta_lon(lon_y, lon) < 0)
        planets[n] = {"lon": round(lon,3), "retro": bool(retro)}
    return {"engine": "failsafe", "timestamp": now.isoformat(), "planets": planets}

# ---------------------------------------------
#  SWISS EPHEMERIS
# ---------------------------------------------
def swiss_compute(now: datetime):
    swe.set_ephe_path(str(EPH))
    jd = swe.julday(now.year, now.month, now.day,
                    now.hour + now.minute/60 + now.second/3600,
                    swe.GREG_CAL)
    jd_y = jd - 1
    flag = swe.FLG_SWIEPH
    bodies = {"Sun":swe.SUN,"Moon":swe.MOON,"Mercury":swe.MERCURY,"Venus":swe.VENUS,
              "Mars":swe.MARS,"Jupiter":swe.JUPITER,"Saturn":swe.SATURN}
    out = {"engine": "swisseph", "timestamp": now.isoformat(), "planets": {}}
    for n,c in bodies.items():
        p,_ = swe.calc_ut(jd, c, flag)
        p_y,_ = swe.calc_ut(jd_y, c, flag)
        lon = deg_norm(p[0]); lon_y = deg_norm(p_y[0])
        retro = bool(delta_lon(lon_y, lon) < 0)
        out["planets"][n] = {"lon": round(lon,3), "retro": bool(retro)}
    return out

# ---------------------------------------------
#  SKYFIELD EPHEMERIS
# ---------------------------------------------
def skyfield_compute(now: datetime):
    ts = sf_load.timescale()
    t = ts.from_datetime(now)
    t_y = ts.from_datetime(now - timedelta(days=1))
    bsp_candidates = [EPH/"de421.bsp", EPH/"de440s.bsp", EPH/"de430t.bsp"]
    eph_path = next((p for p in bsp_candidates if p.exists()), None)
    if eph_path is None:
        raise FileNotFoundError("No BSP found in ephemeris/")
    planets = sf_load(str(eph_path))
    earth = planets["earth"]
    bodies = {"Sun":"sun","Moon":"moon","Mercury":"mercury","Venus":"venus",
              "Mars":"mars","Jupiter":"jupiter barycenter","Saturn":"saturn barycenter"}
    out = {"engine": f"skyfield:{eph_path.name}", "timestamp": now.isoformat(), "planets": {}}
    for n,k in bodies.items():
        ast = planets[k]
        g = earth.at(t).observe(ast).apparent().frame_latlon(ecliptic_frame)
        lon = deg_norm(g[1].degrees)
        g_y = earth.at(t_y).observe(ast).apparent().frame_latlon(ecliptic_frame)
        lon_y = deg_norm(g_y[1].degrees)
        retro = bool(delta_lon(lon_y, lon) < 0)
        out["planets"][n] = {"lon": round(lon,3), "retro": bool(retro)}
    return out

# ---------------------------------------------
#  CROSS VALIDATION (CAI)
# ---------------------------------------------
def compare(sf, sw):
    diffs = {}
    total = 0
    for n in sf["planets"]:
        if n in sw["planets"]:
            d = abs(delta_lon(sf["planets"][n]["lon"], sw["planets"][n]["lon"]))
            diffs[n] = round(d, 4)
            total += d
    mean = total / len(diffs) if diffs else 0
    cai = max(0, 100 - mean)
    return cai, diffs

# ---------------------------------------------
#  MAIN
# ---------------------------------------------
def main():
    now = datetime.now(timezone.utc)
    log("✨ Ephemeris Engine başlatılıyor...")
    sf = sw = None

    # SKYFIELD
    try:
        if _HAVE_SKYFIELD:
            sf = skyfield_compute(now)
            log(f"🛰️ Skyfield OK ({sf['engine']})")
        else:
            log("⚠️ Skyfield yüklü değil.")
    except Exception as e:
        log(f"⚠️ Skyfield failed: {e}")

    # SWISS
    try:
        if _HAVE_SWISS:
            sw = swiss_compute(now)
            log("🛰️ SwissEphem OK")
        else:
            log("⚠️ SwissEphem yüklü değil.")
    except Exception as e:
        log(f"⚠️ SwissEphem failed: {e}")

    # VERİLERİ BİRLEŞTİR
    if sf and sw:
        cai, diff = compare(sf, sw)
        log(f"🔎 Celestial Accuracy Index: {cai:.3f}")
        data = {"timestamp": now.isoformat(), "CAI": cai, "skyfield": sf, "swiss": sw, "diff": diff}
    elif sf:
        data = sf
    elif sw:
        data = sw
    else:
        data = failsafe_compute(now)
        log("🛟 Failsafe engine used.")

    # DOSYALARI YAZ
    with open(SNAPSHOT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    with open(SUMMARY_TXT, "w", encoding="utf-8") as f:
        f.write(f"SENKRON Ephemeris Report — {now.isoformat()}\n")
        f.write(f"Engine: {data.get('engine','multi')}\n")
        if "CAI" in data: f.write(f"Celestial Accuracy Index: {data['CAI']:.3f}\n")
        f.write("-"*60 + "\n")
        planets = data.get("planets") or data.get("skyfield", {}).get("planets", {})
        for n,v in planets.items():
            f.write(f"{n:8s} | λ={v['lon']:9.3f}°  retro={'Yes' if v['retro'] else 'No'}\n")

    log("✅ ephemeris_engine tamamlandı.")
    print("🎯 Göksel veriler başarıyla üretildi.")

# ---------------------------------------------
#  ENTRY POINT
# ---------------------------------------------
if __name__ == "__main__":
    main()
