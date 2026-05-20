const listings = [
  ["daniels-annex", "Daniels Gateway - Annex", "3-person", "$3,050 est.", "~$1,017 each", "5625 Glen Erin Dr, Central Erin Mills", "Townhouse-style rental, pet-friendly operator, close to parks and errands. Strong shared-home baseline.", "Confirm exact unit, utilities, parking, and cat rules before applying.", "Best shared value", "danielsgateway.com", true],
  ["daniels-rio", "Daniels Erin Centre", "3-person", "$3,050-$3,275", "~$1,017-$1,092 each", "2900 Rio Ct, Central Erin Mills", "3-bed rental community near Erin Mills Town Centre. Better space, predictable management, easy commute.", "Ask which units are cat-friendly and whether outdoor space is private or shared.", "Reliable operator", "danielsgateway.com", true],
  ["creditview-argentia", "Creditview / Argentia Townhouse", "3-person", "$2,950", "~$983 each", "Streetsville / Meadowvale edge", "3 bed, 3 bath, around 1,800 sq ft. Listing marks cats/dogs OK and mentions garden/outdoor space.", "Verify current availability and exact address before touring.", "Cat-friendly", "zumper.com", true],
  ["valcourt", "3211 Valcourt Crescent", "3-person", "$3,600", "$1,200 each", "Erin Mills, near Ridgeway/McMaster", "Detached 4-bed main house with garage and a very short BioScript commute. Strong space-for-money option.", "Pet status not visible. Basement excluded; confirm storage and yard access.", "Closest house feel", "thecanadianhome.com", true],
  ["bidwell", "6035 Bidwell Trail", "3-person", "$3,200", "~$1,067 each", "East Credit", "3-bed townhouse with private deck and backyard access, close to parks and daily errands.", "Dogs allowed but cats listed as not allowed; keep only if cat rules can be solved.", "Backyard", "padmapper.com", false],
  ["lakeshore", "200 Lakeshore Rd W Townhouse", "3-person", "$2,900", "~$967 each", "Southwest Oakville", "3-bed townhouse community with outdoor space and large basement, near lake and park amenities.", "No pets listed and commute is longer; use as backup or price benchmark.", "Price benchmark", "zumper.com", false],
  ["kimbermount", "4600 Kimbermount Ave #89", "3-person", "$3,000", "$1,000 each", "Central Erin Mills", "3-bed townhouse near Erin Mills Town Centre, parks, schools, parking, and major routes.", "Zillow lists no pets; use only if cat rules can be solved.", "Location benchmark", "zillow.com", false],
  ["ridgeway-411", "3401 Ridgeway Dr Unit 411", "2-person", "$2,199", "~$1,100 each", "Ridgeway / Erin Mills", "2-bed condo near the office cluster. Best commute, cleanest simple two-person option.", "Less backyard/greenery. Confirm pet restrictions and utility total.", "Best commute", "zolo.ca", true],
  ["skyview", "3896 Skyview St Basement", "2-person", "$1,850", "~$925 each", "Churchill Meadows", "2-bed basement, park-facing street, very strong price for sharing with brother.", "Apartments.com says no pets. Treat as a price anchor unless cat exception is confirmed.", "Best price", "apartments.com", true],
  ["wheat-boom", "482 Wheat Boom Dr Basement", "2-person", "$1,750", "~$875 each", "Oakville, Dundas / Trafalgar", "2-bed basement with listing page marking cats OK and dogs OK. Good price if commute is acceptable.", "Pet text conflicts on source page; must confirm before viewing.", "Pet note conflict", "zumper.com", false],
  ["sir-johns", "3061 Sir John's Homestead", "2-person", "$2,549-$3,391", "~$1,275-$1,696 each", "Erin Mills / Sheridan", "Townhouse-style rental community with large floor plans and 2-3 bed availability.", "Above clean budget line. Use as quality benchmark.", "Stretch quality", "apartments.com", false],
  ["kellandy", "5644 Kellandy Run Basement", "2-person", "$1,700", "~$850 each", "Churchill Meadows", "2-bed basement in a detached home near Ridgeway Plaza, highways, transit, parks, and schools.", "Pets are contact-manager; confirm cat acceptance and basement quality.", "Cheapest 2-bed", "rew.ca", true],
  ["stardust", "3914 Stardust Drive Basement", "2-person", "$1,800", "~$900 each", "Churchill Meadows", "Nearby 2-bed basement backup from the same REW search cluster.", "Confirm listing status, cat rules, utilities, and layout.", "Backup", "rew.ca", false],
  ["tresca", "5257 Tresca Trail Basement", "2-person", "$1,850", "~$925 each", "Churchill Meadows", "2-bed, 2-bath basement backup in the Churchill Meadows cluster.", "Confirm current availability, cat rules, utilities, and room split.", "Backup", "rew.ca", false],
  ["council-ring", "2475 Council Ring Rd", "solo", "$1,100", "Solo", "Erin Mills", "Best solo fit: green front/back lawn, perennial garden, utilities included, close enough to BioScript.", "Shared kitchen. Ask if one quiet indoor cat is accepted and whether yard access is real.", "Best solo lead", "forestwood.ca", true],
  ["cider-mill", "3371 Cider Mill Place Room C", "solo", "$1,000", "Solo", "Erin Mills, near UTM / Credit River", "Separate-entry basement room, utilities included, green neighbourhood, useful backup under budget.", "Shared kitchen/laundry. Confirm cat rules and light quality.", "Budget fit", "rentcafe.com", true],
  ["trellis", "4253 Trellis Crescent Upper", "solo", "$900 / room", "Solo", "Erin Mills / Folkway", "Furnished room in a house with parks nearby. Useful if the goal is cheap, stable, and close.", "Shared bathroom/kitchen. Cat access to common areas must be agreed in writing.", "Cheapest real lead", "rentcafe.com", true],
  ["strabane", "3366 Strabane Drive", "solo", "$1,200", "Solo", "Erindale", "1-bed lead under the solo cap with a cleaner interior look than many basement-room options.", "Confirm cat acceptance, total utilities, commute, and privacy.", "At cap", "rentcafe.com", false],
  ["harman", "2518 Harman Court Basement", "solo", "$1,200", "Solo", "Clarkson", "1-bed basement lead at the cap; a possible solo backup if commute and cat rules work.", "Confirm cat rules, window/light quality, dampness, and distance.", "Backup solo", "rentcafe.com", false],
  ["sanderling", "3441 Sanderling Cres Bsmt #2", "solo", "$900", "Solo", "Erin Mills", "Lower-cost Erin Mills basement-room lead, useful if keeping monthly burn low matters most.", "Confirm privacy, shared spaces, cat acceptance, and long-term fit.", "Low cost", "rentcafe.com", false],
  ["princelea", "1722 Princelea Place Room B", "solo", "$850", "Solo", "East Credit", "Lowest-cost RentCafe lead; useful as a burn-rate fallback if commute and shared setup work.", "Confirm sharing setup, cat acceptance, and suitability beyond short-term.", "Lowest cost", "rentcafe.com", false],
  ["collegeway", "2079 The Collegeway Unit 6", "solo", "$900", "Solo", "Erin Mills", "Erin Mills lead under budget and close to the target search area.", "Confirm cat acceptance, privacy, utilities, and whether it is a room or full unit.", "Erin Mills", "rentcafe.com", false]
].map(([id, title, scenario, rent, split, area, notes, risk, badge, source, shortlist]) => ({
  id, title, scenario, rent, split, area, notes, risk, badge, source, shortlist,
  image: `./housing_packet/assets/${id}.jpg`
}));

let activeFilter = "all";
const grid = document.querySelector("#listingGrid");
const table = document.querySelector("#listingTable");
const shortlistOnly = document.querySelector("#shortlistOnly");
const rentInputs = [
  "mortgagePayment",
  "mortgageInterest",
  "propertyTax",
  "insurance",
  "maintenanceFees",
  "actualRepairs",
  "repairReserve",
  "capitalRepairs",
  "utilities",
  "otherExpenses",
  "rentalUsePct",
  "availableMonths",
  "ownershipShare",
  "ownerPaysUtilities",
  "bPaysH",
  "fairMarketRent",
  "tenantRelationship",
  "bPaysHPurpose",
  "rentMin",
  "rentMax",
  "rentStep"
];
const rentSummary = document.querySelector("#rentSummary");
const rentWarnings = document.querySelector("#rentWarnings");
const rentScenarioTable = document.querySelector("#rentScenarioTable");
const mortgageSplitNote = document.querySelector("#mortgageSplitNote");
let rentSort = { key: "rent", direction: "asc" };

const currency = new Intl.NumberFormat("en-CA", {
  style: "currency",
  currency: "CAD",
  maximumFractionDigits: 0
});

function money(value) {
  return currency.format(Math.round(value));
}

function numberValue(id) {
  const input = document.querySelector(`#${id}`);
  if (!input) return 0;
  const value = Number(input.value);
  return Number.isFinite(value) ? value : 0;
}

function stringValue(id) {
  const input = document.querySelector(`#${id}`);
  return input ? input.value : "";
}

function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max);
}

function calculatorAssumptions() {
  const assumptions = {
    mortgagePayment: Math.max(0, numberValue("mortgagePayment")),
    mortgageInterest: Math.max(0, numberValue("mortgageInterest")),
    propertyTax: Math.max(0, numberValue("propertyTax")),
    insurance: Math.max(0, numberValue("insurance")),
    maintenanceFees: Math.max(0, numberValue("maintenanceFees")),
    actualRepairs: Math.max(0, numberValue("actualRepairs")),
    repairReserve: Math.max(0, numberValue("repairReserve")),
    capitalRepairs: Math.max(0, numberValue("capitalRepairs")),
    utilities: Math.max(0, numberValue("utilities")),
    otherExpenses: Math.max(0, numberValue("otherExpenses")),
    rentalUsePct: clamp(numberValue("rentalUsePct"), 0, 100),
    availableMonths: clamp(numberValue("availableMonths"), 0, 12),
    ownershipShare: clamp(numberValue("ownershipShare"), 0, 100),
    ownerPaysUtilities: stringValue("ownerPaysUtilities") === "yes",
    bPaysH: Math.max(0, numberValue("bPaysH")),
    fairMarketRent: Math.max(0, numberValue("fairMarketRent")),
    tenantRelationship: stringValue("tenantRelationship") || "unknown",
    bPaysHPurpose: stringValue("bPaysHPurpose") || "unknown",
    rentMin: clamp(numberValue("rentMin"), 0, 4000),
    rentMax: clamp(numberValue("rentMax"), 0, 4000),
    rentStep: clamp(numberValue("rentStep"), 25, 1000)
  };

  if (assumptions.rentMin > assumptions.rentMax) {
    [assumptions.rentMin, assumptions.rentMax] = [assumptions.rentMax, assumptions.rentMin];
  }

  assumptions.derivedPrincipal = Math.max(0, assumptions.mortgagePayment - assumptions.mortgageInterest);
  assumptions.inputErrors = [];
  if (assumptions.mortgageInterest > assumptions.mortgagePayment) {
    assumptions.inputErrors.push("Mortgage interest cannot exceed the total mortgage payment.");
  }

  assumptions.taxScale =
    (assumptions.rentalUsePct / 100) *
    (assumptions.availableMonths / 12) *
    (assumptions.ownershipShare / 100);
  assumptions.eligibleCurrentExpenses =
    assumptions.mortgageInterest +
    assumptions.propertyTax +
    assumptions.insurance +
    assumptions.maintenanceFees +
    assumptions.actualRepairs +
    (assumptions.ownerPaysUtilities ? assumptions.utilities : 0) +
    assumptions.otherExpenses;
  assumptions.taxDeductibleExpenses = assumptions.eligibleCurrentExpenses * assumptions.taxScale;
  assumptions.cashCarryingCosts =
    assumptions.mortgagePayment +
    assumptions.propertyTax +
    assumptions.insurance +
    assumptions.maintenanceFees +
    assumptions.actualRepairs +
    assumptions.repairReserve +
    assumptions.capitalRepairs +
    assumptions.utilities +
    assumptions.otherExpenses;
  return assumptions;
}

function riskModel(row, assumptions) {
  const flags = [];
  let severity = "neutral";
  let rank = 1;
  const addFlag = (level, text) => {
    flags.push(text);
    const levels = { neutral: 1, review: 2, high: 3, critical: 4 };
    if (levels[level] > rank) {
      severity = level;
      rank = levels[level];
    }
  };

  if (assumptions.fairMarketRent <= 0) {
    addFlag("high", "FMV not entered - market risk not assessed");
  } else if (row.rent < assumptions.fairMarketRent) {
    addFlag("high", "Below entered FMV - professional review required");
  } else if (row.rent === assumptions.fairMarketRent) {
    addFlag("review", "At entered FMV, assuming supportable comparables");
  }

  if (assumptions.bPaysH > 0 && assumptions.bPaysH >= row.rent) {
    addFlag("critical", "High-risk circular-flow row");
  }

  if (
    row.taxProfitLoss < 0 &&
    row.rent < assumptions.fairMarketRent &&
    ["known", "related"].includes(assumptions.tenantRelationship)
  ) {
    addFlag("critical", "Known/related tenant + below FMV + loss - review required");
  }

  if (
    row.taxProfitLoss < 0 &&
    row.rent < assumptions.fairMarketRent &&
    assumptions.tenantRelationship === "unknown"
  ) {
    addFlag("high", "Unknown relationship + below FMV + loss - review required");
  }

  if (row.taxProfitLoss < 0) {
    addFlag("review", "Modelled loss - claimability not determined");
  }

  if (assumptions.bPaysHPurpose === "rent-subsidy" || assumptions.bPaysHPurpose === "unknown") {
    addFlag("review", "B-to-H payment purpose needs documentation");
  }

  return {
    severity,
    rank,
    text: flags.length ? flags.join(" + ") : "No automated flag; review still required"
  };
}

function taxModel(rent, assumptions) {
  const monthlyProfitLoss = rent - assumptions.taxDeductibleExpenses;
  return {
    monthlyEligibleExpenses: assumptions.taxDeductibleExpenses,
    monthlyProfitLoss,
    annualProfitLoss: monthlyProfitLoss * 12
  };
}

function cashModel(rent, assumptions) {
  return {
    bCashFlow: rent - assumptions.bPaysH - assumptions.cashCarryingCosts,
    hNetCashFlow: assumptions.bPaysH - rent
  };
}

function lenderIllustration(rent, monthlyTaxProfitLoss) {
  const annualGrossRent = rent * 12;
  return {
    annualGrossRent,
    grossRentAddback50: annualGrossRent * 0.5,
    illustrativeNetRentalIncome: monthlyTaxProfitLoss * 12
  };
}

function buildRentScenarios(assumptions) {
  let rents = [];
  const step = Math.max(assumptions.rentStep, 25);
  for (let rent = assumptions.rentMin; rent <= assumptions.rentMax; rent += step) {
    rents.push(rent);
  }
  if (rents[rents.length - 1] !== assumptions.rentMax) {
    rents.push(assumptions.rentMax);
  }

  return rents.map((rent) => {
    const tax = taxModel(rent, assumptions);
    const cash = cashModel(rent, assumptions);
    const lender = lenderIllustration(rent, tax.monthlyProfitLoss);
    const row = {
      rent,
      annualGrossRent: lender.annualGrossRent,
      taxProfitLoss: tax.monthlyProfitLoss,
      bCashFlow: cash.bCashFlow,
      hNetCashFlow: cash.hNetCashFlow,
      grossRentAddback50: lender.grossRentAddback50,
      illustrativeNetRentalIncome: lender.illustrativeNetRentalIncome
    };
    const risk = riskModel(row, assumptions);
    return {
      ...row,
      risk: risk.text,
      riskSeverity: risk.severity,
      riskRank: risk.rank
    };
  });
}

function scenarioBy(rows, compare) {
  return rows.reduce((best, row) => (compare(row, best) ? row : best), rows[0]);
}

function sortedRows(rows) {
  const direction = rentSort.direction === "asc" ? 1 : -1;
  return [...rows].sort((a, b) => {
    if (a[rentSort.key] < b[rentSort.key]) return -1 * direction;
    if (a[rentSort.key] > b[rentSort.key]) return 1 * direction;
    return a.rent - b.rent;
  });
}

function closestRow(rows, score) {
  return rows.reduce((best, row) => (score(row) < score(best) ? row : best), rows[0]);
}

function renderSummaryCard(label, value, detail, className = "") {
  return `
    <article class="summary-card ${className}">
      <span>${label}</span>
      <strong>${value}</strong>
      <p>${detail}</p>
    </article>
  `;
}

function renderInvalidCalculator(assumptions) {
  mortgageSplitNote.textContent = assumptions.inputErrors.join(" ");
  rentSummary.innerHTML = `
    <article class="summary-card critical-risk">
      <span>Input correction required</span>
      <strong>Blocked</strong>
      <p>${assumptions.inputErrors.join(" ")}</p>
    </article>
  `;
  rentWarnings.innerHTML = `<p>${assumptions.inputErrors.join(" ")}</p>`;
  rentScenarioTable.innerHTML = "";
}

function renderRentCalculator() {
  if (!rentSummary || !rentScenarioTable) return;
  const assumptions = calculatorAssumptions();
  if (assumptions.inputErrors.length) {
    renderInvalidCalculator(assumptions);
    return;
  }

  const rows = buildRentScenarios(assumptions);
  const lossRows = rows.filter((row) => row.taxProfitLoss < 0).length;
  const belowMarketRows = rows.filter((row) => assumptions.fairMarketRent > 0 && row.rent < assumptions.fairMarketRent).length;
  const circularRows = rows.filter((row) => assumptions.bPaysH > 0 && assumptions.bPaysH >= row.rent).length;
  const nearestFmv = assumptions.fairMarketRent > 0
    ? closestRow(rows, (row) => Math.abs(row.rent - assumptions.fairMarketRent))
    : null;
  const lowestNotBelowFmv = assumptions.fairMarketRent > 0
    ? rows.find((row) => row.rent >= assumptions.fairMarketRent)
    : null;
  const cashBreakEven = closestRow(rows, (row) => Math.abs(row.bCashFlow));

  mortgageSplitNote.textContent = `Derived non-deductible principal: ${money(assumptions.derivedPrincipal)}. Only entered interest is used in the tax illustration.`;

  rentSummary.innerHTML = [
    renderSummaryCard("Loss rows requiring review", String(lossRows), `${lossRows} of ${rows.length} rows show a modelled loss; claimability is not determined here.`, lossRows ? "review-risk" : "neutral"),
    nearestFmv
      ? renderSummaryCard("Nearest entered FMV row", money(nearestFmv.rent), `Entered FMV is ${money(assumptions.fairMarketRent)}; comparables still need support.`, "neutral")
      : renderSummaryCard("Nearest entered FMV row", "Missing", "Enter a fair-market rent estimate to assess market-risk rows.", "high-risk"),
    lowestNotBelowFmv
      ? renderSummaryCard("Lowest row not below FMV", money(lowestNotBelowFmv.rent), "This is a reference row, not a recommendation.", "neutral")
      : renderSummaryCard("Lowest row not below FMV", "None", "No row in this range reaches the entered FMV estimate.", "high-risk"),
    cashBreakEven.bCashFlow === 0
      ? renderSummaryCard("B cash break-even row", money(cashBreakEven.rent), "This row is cash-flow neutral before tax.", "neutral")
      : renderSummaryCard("Closest B cash break-even row", money(cashBreakEven.rent), `B cash flow is ${money(cashBreakEven.bCashFlow)}; no exact break-even row in range.`, "review-risk")
  ].join("");

  rentWarnings.innerHTML = [
    `${lossRows} of ${rows.length} rows show a modelled loss before tax; this calculator does not decide whether any loss is claimable.`,
    belowMarketRows
      ? `${belowMarketRows} rows are below the entered FMV and require professional review.`
      : "No row is below the entered FMV; comparables and relationship facts still matter.",
    circularRows
      ? `${circularRows} rows are high-risk circular-flow rows because B pays H at least as much as rent.`
      : "B-to-H payments are shown separately only for arithmetic; documentation still matters.",
    assumptions.ownerPaysUtilities
      ? "Utilities are included in the tax illustration because owner-pays-utilities is set to yes."
      : "Utilities are excluded from the tax illustration because owner-pays-utilities is set to no."
  ].map((warning) => `<p>${warning}</p>`).join("");

  document.querySelectorAll("[data-rent-sort]").forEach((button) => {
    const active = button.dataset.rentSort === rentSort.key;
    button.classList.toggle("sort-active", active);
    button.setAttribute("aria-sort", active ? (rentSort.direction === "asc" ? "ascending" : "descending") : "none");
  });

  rentScenarioTable.innerHTML = sortedRows(rows).map((row) => `
    <tr class="${row.riskSeverity}-row">
      <td><strong>${money(row.rent)}</strong><br><span class="source">scenario</span></td>
      <td>${money(row.annualGrossRent)}<br><span class="source">reported gross only</span></td>
      <td class="${row.taxProfitLoss < 0 ? "negative" : "positive"}">${money(row.taxProfitLoss)}<br><span class="source">${money(row.taxProfitLoss * 12)} / year</span></td>
      <td class="${row.bCashFlow < 0 ? "negative" : "positive"}">${money(row.bCashFlow)}</td>
      <td class="${row.hNetCashFlow > 0 ? "risk-emphasis" : ""}">${money(row.hNetCashFlow)}<br><span class="source">B pays H minus rent</span></td>
      <td>${money(row.grossRentAddback50)}<br><span class="source">illustration only</span></td>
      <td class="${row.illustrativeNetRentalIncome < 0 ? "negative" : "positive"}">${money(row.illustrativeNetRentalIncome)}<br><span class="source">not lender approval</span></td>
      <td><span class="risk-badge ${row.riskSeverity}">${row.riskSeverity}</span><br>${row.risk}</td>
    </tr>
  `).join("");
}

function tagClass(scenario) {
  if (scenario === "2-person") return "two";
  if (scenario === "solo") return "solo";
  return "";
}

function filteredListings() {
  return listings.filter((listing) => {
    const scenarioMatch = activeFilter === "all" || listing.scenario === activeFilter;
    const shortlistMatch = !shortlistOnly.checked || listing.shortlist;
    return scenarioMatch && shortlistMatch;
  });
}

function render() {
  const current = filteredListings();
  grid.innerHTML = current.map((listing) => `
    <article class="listing-card">
      <img src="${listing.image}" alt="${listing.title}" loading="lazy" />
      <div class="card-body">
        <div class="card-top">
          <span class="card-scenario">${listing.scenario}</span>
          <span class="tag ${tagClass(listing.scenario)}">${listing.badge}</span>
        </div>
        <h3>${listing.title}</h3>
        <div class="facts"><span>${listing.rent}</span><span>${listing.split}</span></div>
        <div class="area">${listing.area}</div>
        <p class="notes">${listing.notes}</p>
        <p class="risk">${listing.risk}</p>
        <span class="source">${listing.source}</span>
      </div>
    </article>
  `).join("");

  table.innerHTML = current.map((listing) => `
    <tr>
      <td><strong>${listing.title}</strong><br><span class="source">${listing.source}</span></td>
      <td>${listing.scenario}</td>
      <td>${listing.rent}<br>${listing.split}</td>
      <td>${listing.area}</td>
      <td>${listing.risk}</td>
    </tr>
  `).join("");
}

document.querySelectorAll("[data-filter]").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll("[data-filter]").forEach((b) => b.classList.remove("active"));
    button.classList.add("active");
    activeFilter = button.dataset.filter;
    render();
  });
});

rentInputs.forEach((id) => {
  const input = document.querySelector(`#${id}`);
  if (input) {
    input.addEventListener("input", renderRentCalculator);
    input.addEventListener("change", renderRentCalculator);
  }
});

document.querySelectorAll("[data-rent-sort]").forEach((button) => {
  button.addEventListener("click", () => {
    const key = button.dataset.rentSort;
    rentSort = {
      key,
      direction: rentSort.key === key && rentSort.direction === "asc" ? "desc" : "asc"
    };
    renderRentCalculator();
  });
});

shortlistOnly.addEventListener("change", render);
document.querySelector("#printBtn").addEventListener("click", () => window.print());
renderRentCalculator();
render();
