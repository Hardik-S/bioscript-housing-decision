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

shortlistOnly.addEventListener("change", render);
document.querySelector("#printBtn").addEventListener("click", () => window.print());
render();
