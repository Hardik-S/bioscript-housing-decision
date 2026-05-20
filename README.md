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
- The calculator derives non-deductible principal from the mortgage payment and entered interest so it does not imply the whole mortgage payment is automatically deductible. It shows planning math only, not tax, legal, accounting, or lending advice.
- The scenario table is intentionally exploratory instead of prescriptive: it compares rent levels from CAD 0-4,000/month and flags below-market, circular-flow, missing-evidence, and loss-producing rows for professional review.
- The calculator does not recommend a rent value. It shows neutral reference rows such as nearest entered fair-market rent, lowest row not below entered fair-market rent, and closest B cash break-even row.

## Rent calculator references

- CRA renting below fair market value: https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/rental-income/renting-below-fair-market-value.html
- CMHC rental income qualification reference: https://assets.cmhc-schl.gc.ca/sf/project/cmhc/pdfs/content/en/rental-income-promo-card-jun28.pdf?rev=963e6041-f383-45e3-96f5-df5e765054c9
- OSFI rental income clarification: https://www.osfi-bsif.gc.ca/en/risks/real-estate-secured-lending/clarifying-osfis-guidance-rental-income-mortgage-classification

## Known limitations

- Repair reserves and capital repairs/improvements are cash-planning inputs only. They are not treated as current deductible expenses merely because they are entered.
- Actual current repairs, utilities, and other expenses are still only illustrations. Real treatment can depend on current-versus-capital classification, rental-use percentage, months available for rent, ownership share, and lease terms.
- Principal repayment is excluded from the tax illustration. Mortgage interest must come from the actual amortization schedule or lender records before relying on the model.
- B-to-H side payments are shown separately only for arithmetic. If a payment offsets rent, subsidizes H, lacks documentation, or is tied to the tenancy, tax professionals or lenders may treat the economics differently.
- Lender columns are non-authoritative illustrations. Actual qualification depends on the lender or broker method, lease evidence, market support, payment history, and relationship review.
- Keep the repo and deploy private before putting real property, family, tax, lender, or personal financial facts into defaults, documentation, screenshots, or source files.

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
- Set `B pays H` above the maximum rent and confirm circular-flow rows are flagged.
- Set fair-market rent above and below the scenario range and confirm the risk severity changes.
- Set repair reserve and capital repairs high and confirm they do not change modelled tax profit/loss.
- Set owner-pays-utilities to `No` and confirm utilities are excluded from the tax illustration.
- Set mortgage interest above the mortgage payment and confirm reference cards/table are blocked.
