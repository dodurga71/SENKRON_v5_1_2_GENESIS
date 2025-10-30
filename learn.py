import sys
args = sys.argv[1:]
if args and args[0] == "--offline":
    print("[OFFLINE] Offline mod aktif. Arxiv verisi kaynaktan cekilmeyecek.")
    exit()
import arxiv, yaml, datetime, requests, json, pandas as pd

def update_science_registry():
    timestamp = datetime.datetime.now().isoformat()
    registry_path = "docs/science_registry.yaml"
    print(f"[{timestamp}] 🔍 Bilimsel veri taraması başlatıldı...")

    # 1. ArXiv taraması
    search = arxiv.Search(
        query="artificial intelligence OR quantum computing OR time perception",
        max_results=5,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    results = []
    for r in search.results():
        results.append({
            "title": r.title,
            "authors": [a.name for a in r.authors],
            "published": str(r.published),
            "url": r.entry_id
        })

    # 2. GitHub Trending
    gh = requests.get("https://raw.githubusercontent.com/huchenme/github-trending-api/master/sample/github_trending_python.json")
    if gh.ok:
        top_repos = [repo["name"] for repo in gh.json()[:5]]
    else:
        top_repos = []

    # 3. YAML Güncelleme
    registry = {
        "timestamp": timestamp,
        "arxiv_papers": results,
        "top_github_repos": top_repos
    }
    with open(registry_path, "w", encoding="utf-8") as f:
        yaml.dump(registry, f, allow_unicode=True)
    print("✅ science_registry.yaml güncellendi.")

if __name__ == "__main__":
    update_science_registry()

