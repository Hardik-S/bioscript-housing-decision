# BioScript Mississauga Housing Packet

Decision packet and static web companion for comparing solo, 2-person, and 3-person housing options near the BioScript Mississauga Ridgeway/Dunwin office cluster.

## What is in this repo

- `index.html`, `styles.css`, `app.js`: static Vercel-ready housing comparison site.
- `housing_packet/BioScript_Housing_Decision_Packet.pdf`: 8-page PDF packet.
- `housing_packet/build_housing_packet.py`: source listing data and image download helper.
- `housing_packet/build_housing_packet_clean.py`: current PDF generator.
- `housing_packet/assets/`: cached real listing images used in the PDF/site.

## Design decisions

- The PDF uses fixed catalog cards, not auto-flowing text boxes. Every card field has a line cap to prevent overflow.
- The site is static on purpose: no backend, no auth, no scraping, and no database. Listing availability changes quickly, so the packet should be treated as a decision aid, not a live MLS clone.
- Real listing photos are cached locally so the PDF and site do not break if listing portals block hotlinking.
- Public repo is acceptable because the content is based on public rental listings and contains no credentials, private phone numbers, or application documents.

## Verification

Regenerate the PDF:

```powershell
python .\housing_packet\build_housing_packet_clean.py
```

Render PDF pages for visual QA:

```powershell
pdftoppm -png -r 144 .\housing_packet\BioScript_Housing_Decision_Packet.pdf .\housing_packet\qa\dense-page
```

Run the static site locally:

```powershell
python -m http.server 4173
```
