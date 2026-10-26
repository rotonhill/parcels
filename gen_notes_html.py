import json
import sys
import html

try:
    data = json.load(sys.stdin)
except Exception as e:
    sys.stderr.write(f"Error with input: {e}\n")
    sys.exit(1)

features = data.get("features", [])

# Collect entries with notes
entries = []
for feat in features:
    props = feat.get("properties") or {}
    notes = props.get("Notes")
    if notes and str(notes).strip():
        entries.append({
            "id": str(props.get("ParcelID", "")),
            "location": str(props.get("Location", "Unknown Location")),
            "street": str(props.get("StreetName", "Unknown Street")),   
            "street_num": int(props.get("StreetNum", "0")),
            "year": props.get("YearBuilt", "Unknown"),
            "valid_to": props.get("valid_to"),
            "notes": str(notes).strip()
        })

# Sort alphabetically by street address
entries.sort(key=lambda e: (e["street"], e["street_num"]))

# Generate static HTML
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Roton Hill Historical Notes & Directory</title>
  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      line-height: 1.6;
      color: #222;
      background: #fafafa;
      margin: 0;
      padding: 24px 16px;
    }}
    .container {{
      max-width: 720px;
      margin: 0 auto;
      background: #ffffff;
      padding: 32px;
      border-radius: 8px;
      box-shadow: 0 1px 6px rgba(0,0,0,0.08);
    }}
    header {{
      border-bottom: 2px solid #eee;
      padding-bottom: 16px;
      margin-bottom: 24px;
    }}
    h1 {{ margin: 0 0 8px 0; color: #1a4e75; font-size: 24px; }}
    .back-link {{ font-size: 14px; color: #0b5394; text-decoration: none; font-weight: 600; }}
    .back-link:hover {{ text-decoration: underline; }}
    .entry {{
      margin-bottom: 28px;
      padding-bottom: 20px;
      border-bottom: 1px solid #f0f0f0;
    }}
    .entry:last-child {{ border-bottom: none; }}
    .entry h2 {{
      font-size: 18px;
      margin: 0 0 4px 0;
      color: #333;
    }}
    .meta {{
      font-size: 13px;
      color: #666;
      margin-bottom: 10px;
    }}
    .entry p {{ margin: 0 0 10px 0; }}
    .map-btn {{
      display: inline-block;
      font-size: 12px;
      color: #1a4e75;
      background: #eef4f9;
      padding: 4px 10px;
      border-radius: 4px;
      text-decoration: none;
      font-weight: 600;
    }}
    .map-btn:hover {{ background: #dceaf5; }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <a href="index.html" class="back-link">&larr; Back to Interactive Map</a>
      <h1>Roton Hill Historical Notes & Records</h1>
      <p>A directory of historical notes, resident histories, and parcel records documented across Roton Hill.</p>
    </header>

    <main>
"""

for item in entries:
    loc = html.escape(item["location"])
    yr = html.escape(str(item["year"]))
    notes = item["notes"]
    pid = html.escape(item["id"])
    # If there's a valid_to attribute, it will be the link year. If not, use 2026 as the default
    valid_to = item.get("valid_to")
    if valid_to:
        valid_to = int(valid_to) - 1
    else:
        valid_to = "2026"

    # URL pointing back to the map with the year & parcel preloaded
    map_link = f"index.html?parcel={pid}&year={valid_to}"

    html_content += f"""      <article class="entry" id="{pid}">
        <h2>{loc}</h2>
        <div class="meta">Year Built: {yr} | Parcel: {pid}</div>
        <p>{notes}</p>
        <a href="{map_link}" class="map-btn">View on Map &rarr;</a>
      </article>\n"""

html_content += """    </main>
  </div>
</body>
</html>
"""
sys.stdout.write(html_content)

sys.stderr.write(f"Generated HTML with {len(entries)} historical entries.\n")