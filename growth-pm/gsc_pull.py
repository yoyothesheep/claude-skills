"""
Pull GSC index status + traffic data. Updates AEO_Content.md (Google Status column).
Writes traffic metrics only (no index status) to Data_Insights.md (GSC Baseline table).

Place this script anywhere in your project. Pass --root to set the project root
(defaults to the directory you run from). Credentials are read from scripts/ under root.

Flags:
  --root            Project root directory (default: cwd)
  --tracker         Path to AEO_Content.md (default: docs/tracker/AEO_Content.md)
  --client-secret   Path to OAuth client secret JSON (default: scripts/client_secret.json under root)
  --token           Path to OAuth token JSON (default: scripts/token.json under root)
"""
import os
import re
import sys
from datetime import date, timedelta

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]

def _flag(argv, name, default=None):
    return argv[argv.index(name) + 1] if name in argv else default

_argv = sys.argv[1:]
ROOT = os.path.abspath(_flag(_argv, "--root", os.getcwd()))
SECRET_FILE = os.path.abspath(_flag(_argv, "--client-secret", os.path.join(ROOT, "scripts/client_secret.json")))
TOKEN_FILE  = os.path.abspath(_flag(_argv, "--token",         os.path.join(ROOT, "scripts/token.json")))

SITE_URL = "sc-domain:ai-proof-careers.com"
SITE_BASE = "https://www.ai-proof-careers.com"
DATE_RANGE_DAYS = 30
TOP_QUERIES = 5
_TRACKER_DEFAULT = "docs/tracker/AEO_Content.md"
DATA_INSIGHTS = os.path.join(ROOT, "docs/tracker/Data_Insights.md")

# coverage_state → (google_status_label, is_indexed, notes_reason)
_COVERAGE = {
    "Submitted and indexed":                  ("Indexed",     True,  ""),
    "Indexed, not submitted in sitemap":       ("Indexed",     True,  ""),
    "Crawled - currently not indexed":         ("Not Indexed", False, "Google crawled but chose not to index — check thin/duplicate content or missing canonical"),
    "Discovered - currently not indexed":      ("Not Indexed", False, "URL discovered but not yet crawled — crawl budget delay; resubmit sitemap"),
    "URL is unknown to Google":                ("Not Indexed", False, "URL unknown to Google — request indexing via GSC"),
    "Excluded by 'noindex' tag":               ("Not Indexed", False, "noindex tag present — remove to allow indexing"),
    "Redirect error":                          ("Not Indexed", False, "Redirect error — fix redirect chain"),
    "Soft 404":                                ("Not Indexed", False, "Soft 404 — page returns 200 but looks like a 404"),
    "Not found (404)":                         ("Not Indexed", False, "Returns 404 — check deployment"),
    "Blocked by robots.txt":                   ("Not Indexed", False, "Blocked by robots.txt — check public/robots.txt"),
}


def parse_pages_from_tracker(tracker_path: str) -> list[tuple[str, str]]:
    """Extract (slug, title) for all Published rows from AEO_Content.md."""
    with open(tracker_path, encoding="utf-8") as f:
        content = f.read()
    pages = []
    for line in content.splitlines():
        m = re.search(r"\|\s*([^|]+?)\s*\|\s*\w+\s*\|\s*Published[^|]*\|[^|]*\|\s*`?(/[^`|]+)`?", line)
        if m:
            pages.append((m.group(2).strip(), m.group(1).strip()))
    return pages


def get_credentials():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
    return creds


def inspect_url(service, page_path: str) -> dict:
    """Return index status dict for a URL via URL Inspection API."""
    full_url = f"{SITE_BASE}{page_path}"
    try:
        resp = service.urlInspection().index().inspect(
            body={"inspectionUrl": full_url, "siteUrl": SITE_URL}
        ).execute()
        idx = resp.get("inspectionResult", {}).get("indexStatusResult", {})
        state = idx.get("coverageState", "URL is unknown to Google")
        label, is_indexed, reason = _COVERAGE.get(state, ("Not Indexed", False, state))
        return {"state": state, "label": label, "is_indexed": is_indexed, "reason": reason,
                "last_crawl": idx.get("lastCrawlTime", "")}
    except Exception as e:
        return {"state": "error", "label": "Not Indexed", "is_indexed": False,
                "reason": f"inspection error: {e}", "last_crawl": ""}


def fetch_page_stats(service, page_path, date_from, date_to):
    full_url = f"{SITE_BASE}{page_path}"

    resp = service.searchanalytics().query(
        siteUrl=SITE_URL,
        body={
            "startDate": date_from,
            "endDate": date_to,
            "dimensions": ["page"],
            "dimensionFilterGroups": [{
                "filters": [{"dimension": "page", "operator": "equals", "expression": full_url}]
            }],
        }
    ).execute()

    rows = resp.get("rows", [])
    if not rows:
        return None

    row = rows[0]
    qresp = service.searchanalytics().query(
        siteUrl=SITE_URL,
        body={
            "startDate": date_from,
            "endDate": date_to,
            "dimensions": ["query"],
            "dimensionFilterGroups": [{
                "filters": [{"dimension": "page", "operator": "equals", "expression": full_url}]
            }],
            "rowLimit": TOP_QUERIES,
        }
    ).execute()

    return {
        "clicks": int(row["clicks"]),
        "impressions": int(row["impressions"]),
        "position": round(row["position"], 1),
        "queries": [r["keys"][0] for r in qresp.get("rows", [])],
    }


def update_aeo_content(tracker_path: str, index_map: dict):
    """
    Update Google Status column and Notes in AEO_Content.md Content Status tables.
    index_map: {slug: {"label": str, "is_indexed": bool, "reason": str}}
    Table schema: Title | Type | Status | Priority | Slug | Google Status | Notes
    """
    with open(tracker_path, encoding="utf-8") as f:
        lines = f.readlines()

    out = []
    in_content_status = False
    col_count = None  # number of columns in current table header

    for line in lines:
        s = line.rstrip("\n")

        if s.strip().startswith("## Content Status"):
            in_content_status = True
            col_count = None
            out.append(line)
            continue
        elif s.strip().startswith("## ") and in_content_status:
            in_content_status = False
            col_count = None

        if not in_content_status or not s.strip().startswith("|"):
            out.append(line)
            continue

        # Split into columns (strip leading/trailing empty from |...|)
        parts = s.split("|")
        cols = [c.strip() for c in parts[1:-1]]  # drop empty first and last

        # Header row
        if "Title" in cols and "Slug" in cols:
            col_count = len(cols)
            out.append(line)
            continue

        # Separator row — normalise to match col_count
        if cols and all(re.match(r"-+$", c) or c == "" for c in cols):
            if col_count:
                out.append("|" + "---|" * col_count + "\n")
            else:
                out.append(line)
            continue

        # Data row — update Google Status and Notes for Published rows with known slugs
        if col_count and len(cols) >= 6:
            # Schema: 0=Title 1=Type 2=Status 3=Priority 4=Slug 5=Google Status 6=Notes
            slug_raw = cols[4].strip("`").strip()
            if slug_raw in index_map and "Published" in cols[2]:
                info = index_map[slug_raw]
                cols[5] = info["label"]
                # Append reason to Notes if not indexed and reason not already present
                if not info["is_indexed"] and info["reason"]:
                    existing = cols[6] if len(cols) > 6 else ""
                    reason = info["reason"]
                    # Remove stale "URL unknown" notes before re-adding
                    existing = re.sub(r";?\s*URL unknown to Google[^;|]*", "", existing).strip().strip(";").strip()
                    existing = re.sub(r";?\s*Google crawled but[^;|]*", "", existing).strip().strip(";").strip()
                    existing = re.sub(r";?\s*URL discovered[^;|]*", "", existing).strip().strip(";").strip()
                    existing = re.sub(r";?\s*noindex tag[^;|]*", "", existing).strip().strip(";").strip()
                    existing = re.sub(r";?\s*Redirect error[^;|]*", "", existing).strip().strip(";").strip()
                    existing = re.sub(r";?\s*Soft 404[^;|]*", "", existing).strip().strip(";").strip()
                    existing = re.sub(r";?\s*Returns 404[^;|]*", "", existing).strip().strip(";").strip()
                    existing = re.sub(r";?\s*Blocked by robots[^;|]*", "", existing).strip().strip(";").strip()
                    existing = re.sub(r";?\s*inspection error[^;|]*", "", existing).strip().strip(";").strip()
                    cols[6] = f"{existing}; {reason}".lstrip("; ") if existing else reason
                elif info["is_indexed"] and len(cols) > 6:
                    # Remove stale not-indexed notes
                    existing = cols[6]
                    existing = re.sub(r";?\s*URL unknown to Google[^;|]*", "", existing).strip().strip(";").strip()
                    existing = re.sub(r";?\s*request indexing via GSC[^;|]*", "", existing, flags=re.IGNORECASE).strip().strip(";").strip()
                    cols[6] = existing

            out.append("| " + " | ".join(cols) + " |\n")
            continue

        out.append(line)

    with open(tracker_path, "w", encoding="utf-8") as f:
        f.writelines(out)


_TRAFFIC_HEADER = "| Date | Page | URL | GSC Impressions | GSC Clicks | Avg Position | Top Queries |"
_TRAFFIC_SEP    = "|---|---|---|---|---|---|---|"


def append_gsc_rows(results, pulled_date):
    """Append one dated row per page-with-traffic to the GSC Baseline table."""
    new_rows = []
    for page_path, label, _, stats in results:
        if stats:
            queries_str = ", ".join(stats["queries"]) if stats["queries"] else "—"
            new_rows.append(
                f"| {pulled_date} | {label} | {page_path} | {stats['impressions']:,} | {stats['clicks']:,} | {stats['position']} | {queries_str} |"
            )

    with open(DATA_INSIGHTS) as f:
        content = f.read()

    # Migrate old 6-column header to 7-column dated header on first run
    old_header = "| Page | URL | GSC Impressions | GSC Clicks | Avg Position | Top Queries |"
    old_sep    = "|---|---|---|---|---|---|"
    if old_header in content and _TRAFFIC_HEADER not in content:
        content = content.replace(old_header, _TRAFFIC_HEADER, 1)
        content = content.replace(old_sep, _TRAFFIC_SEP, 1)
        # Prefix existing data rows with the pulled_date so they aren't orphaned
        def prefix_old_row(m):
            row = m.group(0)
            # Only prefix rows that don't already have a date in the first cell
            first_cell = row.split("|")[1].strip()
            if re.match(r"\d{4}-\d{2}-\d{2}", first_cell):
                return row
            return f"| {pulled_date} {row}"
        content = re.sub(r"^\| (?!Date )(?!---|  ).*\|$", prefix_old_row, content, flags=re.MULTILINE)

    # Append new rows before the _Last pulled sentinel
    def replacer(m):
        existing = m.group(1)
        rows_to_add = [r for r in new_rows if r not in existing]
        appended = existing.rstrip("\n") + "\n" + "\n".join(rows_to_add) + "\n" if rows_to_add else existing
        return appended + f"_Last pulled: {pulled_date}_"

    pattern = r"(\| Date \| Page \|[^\n]*\n\|[-|]+\n(?:(?:\|[^\n]+\n)*))_Last pulled:[^\n]*"
    new_content, n = re.subn(pattern, replacer, content, flags=re.DOTALL)
    if n == 0:
        print("WARNING: Could not locate GSC Baseline table to append rows — check Data_Insights.md header.")
        return

    with open(DATA_INSIGHTS, "w") as f:
        f.write(new_content)

    if new_rows:
        print(f"  Appended {len(new_rows)} traffic row(s) for {pulled_date}.")
    else:
        print("  No traffic data to append.")


def main():
    raw = sys.argv[1:]
    tracker_path = os.path.join(ROOT, raw[raw.index("--tracker") + 1] if "--tracker" in raw else _TRACKER_DEFAULT)

    print(f"Reading pages from {os.path.relpath(tracker_path, ROOT)}...")
    pages = parse_pages_from_tracker(tracker_path)
    if not pages:
        print("ERROR: No published pages found. Check AEO_Content.md format.")
        sys.exit(1)
    print(f"Found {len(pages)} published pages.\n")

    print("Authenticating...")
    creds = get_credentials()
    service = build("searchconsole", "v1", credentials=creds)

    # Step 1: Index status
    print("Checking index status...\n")
    index_map = {}
    for page_path, label in pages:
        info = inspect_url(service, page_path)
        index_map[page_path] = info
        icon = "✅" if info["is_indexed"] else "❌"
        print(f"  {icon} {info['label']:<12} {page_path}")

    # Step 2: Traffic
    date_to = date.today()
    date_from = date_to - timedelta(days=DATE_RANGE_DAYS)
    print(f"\nPulling traffic data ({date_from} to {date_to})...\n")

    results = []
    for page_path, label in pages:
        stats = fetch_page_stats(service, page_path, str(date_from), str(date_to))
        if stats:
            print(f"  {label}: {stats['impressions']:,} impressions, {stats['clicks']:,} clicks, pos {stats['position']}")
        else:
            print(f"  {label}: no traffic data")
        results.append((page_path, label, index_map[page_path], stats))

    # Step 3: Write files
    print(f"\nUpdating {os.path.relpath(tracker_path, ROOT)}...")
    update_aeo_content(tracker_path, index_map)
    print("Updating Data_Insights.md...")
    append_gsc_rows(results, date_to.strftime("%Y-%m-%d"))

    # Step 4: Summary
    indexed = sum(1 for v in index_map.values() if v["is_indexed"])
    not_indexed = len(index_map) - indexed
    has_traffic = sum(1 for _, _, _, s in results if s)
    print(f"\n{'='*50}")
    print(f"Summary — {date_to}")
    print(f"  Indexed:     {indexed}/{len(pages)}")
    print(f"  Not Indexed: {not_indexed}/{len(pages)}")
    print(f"  Has traffic: {has_traffic}/{len(pages)}")
    if not_indexed:
        print(f"\n  Not indexed — action needed:")
        for page_path, label in pages:
            if not index_map[page_path]["is_indexed"]:
                print(f"    {page_path}  ({index_map[page_path]['reason']})")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
