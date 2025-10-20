"""
publish_to_substack.py
Auto-publishes the latest FMRC analysis to Substack as a Markdown post.
Author: Kayleighy Mackintosh
"""

import os, json, requests, nbconvert, nbformat

# --- CONFIGURATION ---
NOTEBOOK_PATH = "notebooks/FMRC_Analysis.ipynb"
EXPORT_PATH   = "docs/paper_draft_auto.md"
SUBSTACK_URL  = "https://api.substack.com/publish"
SUBSTACK_API_KEY = os.getenv("SUBSTACK_API_KEY")  # store securely in repo Settings → Secrets

# --- CONVERT NOTEBOOK TO MARKDOWN ---
print("Converting notebook → Markdown…")
nb = nbformat.read(NOTEBOOK_PATH, as_version=4)
exporter = nbconvert.MarkdownExporter()
body, _ = exporter.from_notebook_node(nb)
os.makedirs(os.path.dirname(EXPORT_PATH), exist_ok=True)
with open(EXPORT_PATH, "w", encoding="utf-8") as f:
    f.write(body)

# --- PREPARE PAYLOAD ---
title = "FMRC Auto-Update — Fungal mTOR Regenerative Circuit Results"
payload = {
    "title": title,
    "body_markdown": body,
    "canonical_url": "https://kayleighymackintosh.substack.com",
    "publish": True,
}

# --- PUBLISH TO SUBSTACK ---
headers = {"Authorization": f"Bearer {SUBSTACK_API_KEY}", "Content-Type": "application/json"}
print("Uploading to Substack…")
response = requests.post(SUBSTACK_URL, headers=headers, data=json.dumps(payload))

if response.status_code == 200:
    print("✅ Published successfully to Substack!")
else:
    print(f"⚠️ Failed to publish ({response.status_code}): {response.text}")
