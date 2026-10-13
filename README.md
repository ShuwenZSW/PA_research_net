# PA Research Net

A shared, self-updating map of research themes, methods and regions across the 13 PA faculty — built to make collaboration opportunities visible.

**Open the app (PA, 13 faculty):** https://shuwenzsw.github.io/PA_research_net/
**Open the app (department-wide, 21 faculty):** https://shuwenzsw.github.io/PA_research_net/dept/

## How it works

- **Similarity view** — who shares research ground with whom (theme / method / region, weighted).
- **Complementarity view** — pairs whose topics barely overlap but whose methods and regions complement each other (Complementarity Index, CI ≥ 5).
- **Edit My Profile tab** — every member keeps their own topics, methods, regions and interests current.

## Two modes

- **Static (GitHub Pages, the link above):** edits are saved in your own browser. To publish them for everyone, click *Download merged data.json* in the Edit tab and send the file to the repo maintainer, who commits it here.
- **Live (LAN):** run `python3 server.py` in this folder and share `http://<machine-ip>:8000` on the department network — edits then sync between everyone automatically (the page detects the server and switches mode by itself).

## Data

`data.json` (PA version) and `dept/data.json` (department-wide version) hold all profiles and the theme/method/region label sets. Coding: 35 fine-grained themes (PA) / 48 (department-wide) / 8 methods / 8 regions; primary (●) vs secondary (○) weights. Source: faculty webpages (2026-10-12 / 2026-10-13), cross-checked against Google Scholar profiles.
