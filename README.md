# BioScript Mississauga Housing Packet

Decision packet and static web companion for comparing solo, 2-person, and 3-person housing options near the BioScript Mississauga Ridgeway/Dunwin office cluster.

## What is in this repo

- `index.html`, `styles.css`, `app.js`: static Vercel-ready housing comparison site with an editable rent scenario calculator.
- `housing_packet/BioScript_Housing_Decision_Packet.pdf`: 8-page PDF packet.
- `housing_packet/build_housing_packet.py`: source listing data and image download helper.
- `housing_packet/build_housing_packet_clean.py`: current PDF generator.
- `housing_packet/assets/`: cached real listing images used in the PDF/site.

## Design decisions

- The PDF uses fixed catalog cards, not auto-flowing text boxes. Every card field has a line cap to prevent overflow.
- The site is static on purpose: no backend, no auth, no scraping, and no database. Listing availability changes quickly, so the packet should be treated as a decision aid, not a live MLS clone.
- Real listing photos are cached locally so the PDF and site do not break if listing portals block hotlinking.
- Public repo is acceptable because the content is based on public rental listings and contains no credentials, private phone numbers, or application documents.
- The rent calculator uses synthetic example defaults only. If real property, cash-flow, tax, or lender details are added later, treat the repo/deploy as sensitive and make the GitHub repository private before publishing.
- The calculator separates mortgage interest from principal so it does not imply the whole mortgage payment is automatically deductible. It shows planning math only, not tax, legal, accounting, or lending advice.
- The scenario table is intentionally exploratory instead of prescriptive: it compares rent levels from CAD 0-4,000/month and flags below-market or loss-producing rows for professional review.

## Rent calculator references

- CRA rental losses: https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/rental-income/rental-losses.html
- CRA renting below fair market value: https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/rental-income/renting-below-fair-market-value.html
- CRA rental income guide: https://www.canada.ca/en/revenue-agency/services/forms-publications/publications/t4036/rental-income.html

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

Calculator smoke checks:

- Edit the synthetic assumptions and confirm the summary cards and scenario table update without a page refresh.
- Check rent endpoints at CAD 0/month and CAD 4,000/month.
- Set `B pays H` above the maximum rent and confirm H net cost becomes negative.
- Set fair-market rent above and below the scenario range and confirm the risk flags change.
